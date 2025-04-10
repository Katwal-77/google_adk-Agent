import os
import json
import asyncio
import uuid
import base64
from io import BytesIO
from typing import List, Optional

from pathlib import Path
from dotenv import load_dotenv

from google.genai.types import (
    Part,
    Content,
    FileData,
)

from google.adk.runners import Runner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from fastapi import FastAPI, WebSocket, UploadFile, File, Form, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google_search_agent.agent import root_agent

#
# ADK Streaming
#

# Environment setup
env_file = Path(".env")
env_example_file = Path(".env.example")

# Try to load environment variables from .env file
if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment variables from {env_file}")
else:
    if env_example_file.exists():
        print(f"Warning: .env file not found. Please create one based on {env_example_file}")
    else:
        print("Warning: Neither .env nor .env.example files found.")
    print("You need to set GOOGLE_API_KEY environment variable to use this application.")

# Check if API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("\033[91mError: GOOGLE_API_KEY environment variable is not set.\033[0m")
    print("Please set it in the .env file or as an environment variable.")
    print("The application will start but the agent may not work properly.")

APP_NAME = "Advanced AI Assistant"
session_service = InMemorySessionService()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)
print(f"Uploads directory: {UPLOADS_DIR.absolute()}")


class MessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class FileUploadRequest(BaseModel):
    file_data: str
    file_name: str
    file_type: str
    session_id: Optional[str] = None


def start_agent_session(session_id: str):
    """Starts an agent session"""

    # Create a Session
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=session_id,
        session_id=session_id,
    )

    # Create a Runner
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Set response modality = TEXT
    run_config = RunConfig(response_modalities=["TEXT"])

    # Create a LiveRequestQueue for this session
    live_request_queue = LiveRequestQueue()

    # Start agent session
    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    return live_events, live_request_queue


async def agent_to_client_messaging(websocket, live_events):
    """Agent to client communication"""
    while True:
        async for event in live_events:
            # turn_complete
            if event.turn_complete:
                await websocket.send_text(json.dumps({"turn_complete": True}))
                print("[TURN COMPLETE]")

            if event.interrupted:
                await websocket.send_text(json.dumps({"interrupted": True}))
                print("[INTERRUPTED]")

            # Read the Content and its first Part
            part: Part = (
                event.content and event.content.parts and event.content.parts[0]
            )
            if not part or not event.partial:
                continue

            # Get the text
            text = event.content and event.content.parts and event.content.parts[0].text
            if not text:
                continue

            # Send the text to the client
            await websocket.send_text(json.dumps({"message": text}))
            print(f"[AGENT TO CLIENT]: {text}")
            await asyncio.sleep(0)


async def client_to_agent_messaging(websocket, live_request_queue):
    """Client to agent communication"""
    while True:
        try:
            data = await websocket.receive_text()

            # Check if it's a file message
            if data.startswith("[File Attachment]"):
                # Handle file attachment message
                # In a real implementation, you would process the file here
                # For now, we'll just send a text message acknowledging the file
                content = Content(role="user", parts=[Part.from_text(text="I've uploaded a file. Please analyze it.")])
            else:
                # Regular text message
                content = Content(role="user", parts=[Part.from_text(text=data)])

            live_request_queue.send_content(content=content)
            print(f"[CLIENT TO AGENT]: {data}")
            await asyncio.sleep(0)
        except Exception as e:
            print(f"Error in client_to_agent_messaging: {e}")
            break


# Function to save uploaded files
def save_uploaded_file(file_data: bytes, file_name: str) -> str:
    """Save an uploaded file and return its path"""
    # Generate a unique filename to prevent collisions
    unique_filename = f"{uuid.uuid4()}_{file_name}"
    file_path = UPLOADS_DIR / unique_filename

    # Save the file
    with open(file_path, "wb") as f:
        f.write(file_data)

    return str(file_path)


#
# FastAPI web app
#

app = FastAPI(title="Advanced AI Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))
print(f"Static directory path: {STATIC_DIR}")
if not STATIC_DIR.exists():
    print(f"Warning: Static directory does not exist: {STATIC_DIR}")
else:
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serves the index.html"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    try:
        # Read file content
        file_content = await file.read()

        # Save the file
        file_path = save_uploaded_file(file_content, file.filename)

        return JSONResponse({
            "success": True,
            "file_path": file_path,
            "file_name": file.filename,
            "file_size": len(file_content)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-base64")
async def upload_base64_file(request: FileUploadRequest):
    """Handle base64 encoded file uploads"""
    try:
        # Decode base64 data
        file_data = base64.b64decode(request.file_data)

        # Save the file
        file_path = save_uploaded_file(file_data, request.file_name)

        return JSONResponse({
            "success": True,
            "file_path": file_path,
            "file_name": request.file_name,
            "file_size": len(file_data)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """Client websocket endpoint"""

    # Wait for client connection
    await websocket.accept()
    print(f"Client #{session_id} connected")

    # Start agent session
    live_events, live_request_queue = start_agent_session(session_id)

    try:
        # Start tasks
        agent_to_client_task = asyncio.create_task(
            agent_to_client_messaging(websocket, live_events)
        )
        client_to_agent_task = asyncio.create_task(
            client_to_agent_messaging(websocket, live_request_queue)
        )

        # Wait for both tasks to complete
        await asyncio.gather(agent_to_client_task, client_to_agent_task)
    except Exception as e:
        print(f"Error in websocket connection: {e}")
    finally:
        # Disconnected
        print(f"Client #{session_id} disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
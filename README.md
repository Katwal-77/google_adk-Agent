# Advanced AI Assistant with Streaming Capabilities

This project implements an advanced AI assistant with real-time streaming capabilities, file upload, voice recording, and camera integration. It uses FastAPI for the backend and WebSockets for real-time communication.

## Features

- **Real-time streaming responses** from the AI assistant
- **File upload** functionality for document analysis
- **Voice recording** for audio-based interaction
- **Camera integration** for image capture and analysis
- **Beautiful, responsive UI** with distinct styling for questions and answers
- **Multiple interaction modes** (text, voice, file)

## Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/Katwal-77/google_adk-Agent.git
cd google_adk-Agent
```

2. **Create and activate a virtual environment**:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install the required packages**:

```bash
pip install -r requirements.txt
```

4. **Run the setup script** (optional but recommended):

```bash
python setup.py
```

This script will create necessary directories and prompt you to enter your Gemini API key.

### Configuration

1. **Set up your Gemini API key**:
   - Create a new file named `.env` in the `app` directory (copy from `.env.example`)
   - Add your Gemini API key:
   ```
   GOOGLE_GENAI_USE_VERTEXAI="False"
   GOOGLE_API_KEY=your_api_key_here
   ```
   - **Important**: The `.env` file is gitignored to prevent exposing your API key

### Running the Application

1. **Navigate to the app directory**:

```bash
cd app
```

2. **Start the FastAPI server**:

```bash
python main.py
```

3. **Access the web interface**:
   - Open your browser and go to: http://localhost:8000

### Using the Advanced Features

#### Text Chat
- Simply type your message in the input field and press Enter or click Send

#### File Upload
1. Click the paperclip icon (📎) in the input area
2. Select a file from your device
3. Add an optional message and click Send
4. Alternatively, drag and drop files directly into the chat area

#### Voice Recording
1. Click the microphone icon (🎤) in the input area
2. Speak your message
3. Click the microphone icon again to stop recording and send

#### Camera Capture
1. Click the camera icon (📷) in the input area
2. Grant camera permissions if prompted
3. The image will be captured automatically and prepared for sending

## Troubleshooting

### Common Issues

1. **Server won't start**:
   - Ensure you're in the correct directory (`adk-streaming/app`)
   - Check that all dependencies are installed
   - Verify your API key in the `.env` file

2. **WebSocket connection issues**:
   - Ensure no other application is using port 8000
   - Check browser console for error messages

3. **File upload not working**:
   - Ensure the `uploads` directory exists in the app folder
   - Check file size (limit is 10MB)

4. **Microphone or camera not working**:
   - Grant the necessary browser permissions
   - Try using a different browser (Chrome recommended)

## Project Structure

```
adk-streaming/
├── app/
│   ├── google_search_agent/  # Agent definition
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── static/               # Static files
│   │   └── index.html        # Web interface
│   ├── uploads/              # Uploaded files storage
│   ├── .env                  # Environment variables
│   └── main.py               # FastAPI application
└── README.md                 # This file
```

## Advanced Configuration

For advanced users who want to customize the application:

1. **Modify the agent behavior**:
   - Edit `app/google_search_agent/agent.py`

2. **Customize the UI**:
   - Edit `app/static/index.html`

3. **Add new API endpoints**:
   - Edit `app/main.py`

## License

This project is for educational purposes only.

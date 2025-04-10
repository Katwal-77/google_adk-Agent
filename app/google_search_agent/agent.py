import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Try to load environment variables from .env file
env_file = Path(__file__).parents[1] / ".env"
env_example_file = Path(__file__).parents[1] / ".env.example"

if env_file.exists():
    load_dotenv(env_file)
    print(f"Loaded environment variables from {env_file}")
else:
    if env_example_file.exists():
        print(f"Warning: .env file not found. Please create one based on {env_example_file}")
    else:
        print("Warning: Neither .env nor .env.example files found.")
    print("You need to set GOOGLE_API_KEY environment variable to use this agent.")

# Check if API key is set
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY environment variable is not set.")
    print("Please set it in the .env file or as an environment variable.")
    print("The agent will be initialized but may not work properly.")

from google.adk.agents import Agent
from google.adk.tools import google_search  # Import the tool

# Define the agent with enhanced capabilities
root_agent = Agent(
    # A unique name for the agent
    name="advanced_search_agent",
    # The Large Language Model (LLM) that agent will use
    model="gemini-2.0-flash-exp",
    # A short description of the agent's purpose
    description="Advanced agent to answer questions using Google Search with file and voice capabilities.",
    # Instructions to set the agent's behavior
    instruction="""You are an expert researcher and assistant.
    You always stick to the facts and provide helpful, accurate information.
    When users upload files, analyze them thoroughly and provide insights.
    When users send voice messages, respond in a conversational manner.
    Always be respectful, helpful, and concise in your responses.
    """,
    # Add google_search tool to perform grounding with Google search
    tools=[google_search]
)

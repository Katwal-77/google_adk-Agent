#!/usr/bin/env python
import os
import sys
import shutil
from pathlib import Path

def setup_project():
    """Set up the project by creating necessary directories and files."""
    print("Setting up Advanced AI Assistant project...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    app_dir = project_root / "app"
    
    # Check if app directory exists
    if not app_dir.exists():
        print(f"Error: App directory not found at {app_dir}")
        return False
    
    # Create uploads directory if it doesn't exist
    uploads_dir = app_dir / "uploads"
    if not uploads_dir.exists():
        uploads_dir.mkdir(exist_ok=True)
        print(f"Created uploads directory at {uploads_dir}")
    
    # Create .env.example file if it doesn't exist
    env_example_file = app_dir / ".env.example"
    if not env_example_file.exists():
        with open(env_example_file, "w") as f:
            f.write("# If using Gemini via Google AI Studio\n")
            f.write("GOOGLE_GENAI_USE_VERTEXAI=\"False\"\n")
            f.write("GOOGLE_API_KEY=your_api_key_here\n\n")
            f.write("# If using Gemini via Vertex AI on Google Cloud\n")
            f.write("# GOOGLE_CLOUD_PROJECT=\"your-project-id\"\n")
            f.write("# GOOGLE_CLOUD_LOCATION=\"your-location\" #e.g. us-central1\n")
            f.write("# GOOGLE_GENAI_USE_VERTEXAI=\"True\"\n")
        print(f"Created .env.example file at {env_example_file}")
    
    # Prompt user to create .env file
    env_file = app_dir / ".env"
    if not env_file.exists():
        create_env = input("Would you like to create a .env file now? (y/n): ")
        if create_env.lower() == "y":
            api_key = input("Enter your Gemini API key: ")
            with open(env_file, "w") as f:
                f.write("GOOGLE_GENAI_USE_VERTEXAI=\"False\"\n")
                f.write(f"GOOGLE_API_KEY={api_key}\n")
            print(f"Created .env file at {env_file}")
        else:
            print("Skipping .env file creation. You'll need to create it manually before running the app.")
    
    print("\nSetup complete! You can now run the application with:")
    print("cd app")
    print("python main.py")
    return True

if __name__ == "__main__":
    setup_project()

# Quick Start Guide for Advanced AI Assistant

This guide provides the fastest way to get the Advanced AI Assistant up and running.

## 1. Prerequisites

- Python 3.8+
- Gemini API key (from Google AI Studio)

## 2. One-Time Setup

Run these commands in your terminal:

```bash
# Clone the repository
git clone https://github.com/Katwal-77/google_adk-Agent.git
cd google_adk-Agent

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install required packages
pip install -r requirements.txt

# Run the setup script (creates directories and prompts for API key)
python setup.py
```

## 3. Configure API Key

1. Create a new file named `.env` in the `app` directory
2. Copy the structure from `.env.example`
3. Add your Gemini API key:

```
GOOGLE_GENAI_USE_VERTEXAI="False"
GOOGLE_API_KEY=your_api_key_here
```

**Note**: The `.env` file is excluded from Git to protect your API key

## 4. Run the Application

```bash
# Navigate to the app directory
cd app

# Start the server
python main.py
```

## 5. Use the Application

1. Open your browser and go to: http://localhost:8000
2. Interact with the AI assistant using:
   - Text chat: Type in the input field
   - File upload: Click the paperclip icon (📎)
   - Voice recording: Click the microphone icon (🎤)
   - Camera capture: Click the camera icon (📷)

## 6. Stopping the Application

Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

If you encounter issues:
- Ensure you're in the correct directory (google_adk-Agent/app)
- Verify your API key is correct
- Check that all required packages are installed
- Ensure no other application is using port 8000

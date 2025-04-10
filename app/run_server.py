import os
import sys
import uvicorn

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {current_dir}")

# Add the current directory to the Python path
sys.path.insert(0, current_dir)

# Check if the static directory exists
static_dir = os.path.join(current_dir, "static")
if os.path.exists(static_dir):
    print(f"Static directory exists: {static_dir}")
else:
    print(f"Static directory does not exist: {static_dir}")
    
# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

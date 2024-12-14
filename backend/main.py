from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React app to connect
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the log structure
class LogEntry:
    def __init__(self, timestamp: str, severity: str, node: str, message: str):
        self.timestamp = timestamp
        self.severity = severity
        self.node = node
        self.message = message

# Function to parse ROS log file
def parse_log_file(file_content: str):
    logs = []
    # Regex to match the log format [timestamp] [severity] [node_name] message
    log_pattern = r"\[(?P<timestamp>[^\]]+)\] \[(?P<severity>[^\]]+)\] \[(?P<node>[^\]]+)\] (?P<message>.*)"
    
    for line in file_content.splitlines():
        if not line.strip():
            continue
        # Match the log line using regex
        match = re.match(log_pattern, line.strip())
        if match:
            timestamp = match.group('timestamp')
            severity = match.group('severity')
            node = match.group('node')
            message = match.group('message')
            
            # Create a LogEntry object and append to the logs list
            log_entry = LogEntry(timestamp, severity, node, message)
            logs.append(log_entry.__dict__)  # Convert to dictionary
            
    return logs

@app.get("/api/logs")
async def get_logs():
    try:
        # Read the fake log file
        with open('fake_ros_logs.log', 'r') as f:
            file_content = f.read()
        
        # Parse the file content
        logs = parse_log_file(file_content)

        # Return the parsed logs as a JSON response
        return JSONResponse(content={"logs": logs})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error reading the log file"})

# To run the app manually if needed:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

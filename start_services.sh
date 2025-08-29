#!/bin/bash
# Start MCP server in the background
python server.py &
# Start FastAPI chatbot (will keep container running)
uvicorn chatbot_app:app --host 0.0.0.0 --port 8000

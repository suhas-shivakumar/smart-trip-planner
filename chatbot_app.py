from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Import the travel planner agent
from smart_trip_agent.agent import SmartTripAgent

app = FastAPI()

# Serve static files (for CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Initialize the smart trip agent
smart_trip = SmartTripAgent()


@app.get("/", response_class=HTMLResponse)
async def chat_ui(request: Request):
    """Render the chat UI from index.html."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    session_id = data.get("session_id")  # Can be None for a new conversation
    try:
        # Directly call the travel planner agent
        agent_response_data = await smart_trip.get_response(user_message, session_id)
        return JSONResponse(agent_response_data)
    except Exception as e:
        return JSONResponse({"response": f"Error: {str(e)}", "session_id": session_id})

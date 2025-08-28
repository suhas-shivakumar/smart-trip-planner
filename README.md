# Smart Trip Planner

## Chatbot Interaction Demo
![Chatbot Interaction Demo](static/chatbot_interaction.gif)

## ADK Agent Interaction Demo
![Agent Interaction Demo](static/adk_agent_interaction.gif)

**Python ADK as MCP Client using Gemini LLM as travel planning assistant**

A modular travel agent system built with Python, designed to orchestrate flight search, airport infomation, trip inspiration, and trip purpose using multiple agents and services. The project integrates with Amadeus APIs and supports MCP (Model Context Protocol) server and ADK (Agent Development Kit) workflows.

## Cloud Environment
This project is primarily developed to run directly in **Google Cloud** for seamless integration with Google Cloud resources. Usage of a Google API key or Google APIs in other environments is not supported by default. If you wish to run the project outside GCP and require Google API integration, you must implement those changes and update the environment variables yourself.

**Note:** The repository does not provide built-in support for Google API key usage. Any such integration must be added by the user as needed.

## Features
- Modular agent architecture (airport, inspiration, search, trip purpose)
- Amadeus API integration for flight and airport data
- MCP server support for context-driven agent orchestration
- ADK support for agent development and testing
- Pydantic models for data validation
- Environment-based configuration

## Project Structure
```
smart-trip-planner-agent/
├── agents/
│   ├── airport_agent/
│   ├── inspiration_agent/
│   ├── search_agent/
│   ├── trip_purpose_agent/
├── models/
│   └── schemas.py
├── services/
│   ├── amadeus_api_client.py
│   ├── service_orchestrator.py
├── smart_trip_agent/
│   ├── agent.py
│   ├── sub_agents/
│   │   ├── airport/
│   │   ├── flight_search/
│   │   ├── inspiration/
│   │   ├── trip_purpose/
├── utils/
├── static/
├── templates/
├── chatbot_app.py
├── server.py
├── requirements.txt
├── .env.example
├── .gitignore
```

## Setup
1. **Clone the repository**
   ```sh
   git clone https://github.com/suhas-shivakumar/smart-trip-planner.git
   cd smart-trip-planner
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Copy `.env.example` to `.env` and fill in your Amadeus and MCP credentials.

## Running the MCP Server
The MCP server orchestrates agent interactions and context management. Run it separately from the ADK agent runner.

```sh
python server.py
```
- Ensure your `.env` is configured for MCP and Amadeus API access.
- The server will expose endpoints for agent orchestration and API integration.

## Running the FastAPI Chatbot
The FastAPI chatbot provides a web-based chat UI for interacting with the Smart Trip Agent.

1. **Install FastAPI and Uvicorn (if not already installed):**
   ```sh
   pip install fastapi uvicorn jinja2
   ```
2. **Start the FastAPI server:**
   ```sh
   uvicorn chatbot_app:app --reload --port 9000
   ```
3. **Open your browser and go to:**
   [http://localhost:9000](http://localhost:9000)

You can now interact with the travel planner agent via the web chat interface.

**Note:**
- The chat UI is served from `templates/index.html` and uses static assets from the `static/` folder.
- The backend uses `smart_trip_agent.agent.SmartTripAgent` for agent orchestration.

## Running ADK Agents Separately
ADK (Agent Development Kit) is used for developing and testing agents independently of the MCP server.

1. **Install ADK (if not already installed):**
   ```sh
   pip install google-adk
   ```
2. **Run the agent using ADK:**
   From the root directory run:
   ```sh
   adk web
   ```
   Or for individual agents go to agents folder and run:
   ```sh
   adk web
   ```
- You can run agents in isolation for development and debugging.
- MCP server and ADK agent runners do not interfere with each other.

## Environment Variables
See `.env.example` for all required variables:
- `GOOGLE_CLOUD_PROJECT`, `AMADEUS_CLIENT_ID`, `AMADEUS_CLIENT_SECRET`
- MCP server configuration

## Notes
- Make sure to run the MCP server and ADK agents in separate terminals.
- All agents and services are modular and can be extended.
- For production, ensure proper environment variable management and secure credentials.


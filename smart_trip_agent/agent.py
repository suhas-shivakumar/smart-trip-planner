from google.adk import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
from dotenv import load_dotenv
import uuid

load_dotenv()

from smart_trip_agent import prompt
from smart_trip_agent.sub_agents.airport import airport_agent
from smart_trip_agent.sub_agents.flight_search import flight_search_agent
from smart_trip_agent.sub_agents.inspiration import inspiration_agent
from smart_trip_agent.sub_agents.trip_purpose import trip_purpose_agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="travel_agent",
    instruction=prompt.ROOT_AGENT_PROMPT_V1,
    sub_agents=[
        airport_agent,
        flight_search_agent,
        inspiration_agent,
        trip_purpose_agent,
    ],
)


class SmartTripAgent:
    def __init__(self):
        self.agent = root_agent
        # The runner should be initialized once and reused.
        self.runner = InMemoryRunner(agent=self.agent, app_name="smart-trip-planner")

    async def get_response(self, message: str, session_id: str | None = None):
        """Get a response from the travel planner agent asynchronously."""
        # If no session_id is provided, create a new one for a new conversation.
        if not session_id:
            session_id = str(uuid.uuid4())

        user_id = session_id  # For simplicity, use the same ID for the user.

        # Ensure the session exists. This is important for in-memory services
        # that might lose state on server restart.
        session = await self.runner.session_service.get_session(
            app_name=self.runner.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        if not session:
            await self.runner.session_service.create_session(
                app_name=self.runner.app_name,
                user_id=user_id,
                session_id=session_id,
            )

        # Create the message content for the ADK.
        content = types.Content(role="user", parts=[types.Part.from_text(text=message)])

        response_parts = []
        # The runner's run_async method is an async generator that yields events.
        async for event in self.runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # We collect the text from the content parts of each event.
            if event.content and event.content.parts:
                response_parts.extend(
                    part.text for part in event.content.parts if part.text
                )

        full_response = "".join(response_parts)
        return {
            "response": full_response or "I'm sorry, I couldn't process that request.",
            "session_id": session_id,
        }

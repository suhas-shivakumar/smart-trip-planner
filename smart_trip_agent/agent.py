from google.adk import Agent
from google.adk.tools import google_search
from google.adk.agents import LlmAgent
from dotenv import load_dotenv

load_dotenv()

from smart_trip_agent import prompt
from smart_trip_agent.sub_agents.airport import airport_agent
from smart_trip_agent.sub_agents.flight_search import flight_search_agent
from smart_trip_agent.sub_agents.inspiration import inspiration_agent
from smart_trip_agent.sub_agents.trip_purpose import trip_purpose_agent

root_agent = LlmAgent(
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

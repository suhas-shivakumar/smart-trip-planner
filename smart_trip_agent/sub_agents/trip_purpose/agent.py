from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)
from google.adk.agents import LlmAgent
from dotenv import load_dotenv

load_dotenv()


from . import prompt

trip_purpose_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="trip_purpose_agent",
    instruction=prompt.TRIP_PURPOSE_PROMPT_V1,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://0.0.0.0:8082/trip-purpose",
            ),
        )
    ],
)

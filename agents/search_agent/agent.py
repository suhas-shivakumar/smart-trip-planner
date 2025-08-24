from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)
from google.adk.agents import LlmAgent
from dotenv import load_dotenv

load_dotenv()

from search_agent import prompt

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="airport_agent",
    instruction=prompt.FLIGHT_SEARCH_PROMPT_V1,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://0.0.0.0:8082/flights",
            ),
        )
    ],
)

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.agents import LlmAgent
from dotenv import load_dotenv
load_dotenv()

from . import prompt

airport_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="airport_agent",
    instruction=prompt.AIRPORT_INFO_PROMPT_V1,
    tools=[MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://0.0.0.0:8082/airport",
        ),
    )]
)
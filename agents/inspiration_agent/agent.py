from google.adk.tools.mcp_tool.mcp_toolset import (
    MCPToolset,
    StreamableHTTPConnectionParams,
)
from google.adk.agents import LlmAgent
from google.adk import Agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv

load_dotenv()

from . import prompt


place_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="place_agent",
    instruction=prompt.PLACE_AGENT_PROMPT_V1,
    description="This agent suggests a few destination given some user preferences",
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
    tools=[
        MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://0.0.0.0:8082/inspiration",
            ),
        )
    ],
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="inspiration_agent",
    description="A travel inspiration agent who inspire users, and discover their next vacations; Provide information about places, activities, interests,",
    instruction=prompt.INSPIRATION_AGENT_PROMPT_V1,
    tools=[AgentTool(agent=place_agent)],
)

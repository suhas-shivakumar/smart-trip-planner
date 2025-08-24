import logging
import contextlib

from typing import Any, Tuple
from collections.abc import AsyncIterator

import mcp.types as types
from starlette.routing import Mount
from mcp.server.lowlevel import Server
from starlette.applications import Starlette
from starlette.types import Receive, Scope, Send
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

from dotenv import load_dotenv

load_dotenv()

from services.service_orchestrator import TravelAgentService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

travel_agent_service = TravelAgentService()


def create_airport_mcp_server(server_name: str):
    app = Server(server_name)

    @app.call_tool()
    async def airport_info_tool(
        name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        """
        Get information about an airport using Amadeus API.

        Args:
            airport_code: 3-letter IATA airport code (e.g., 'LAX', 'JFK')

        Returns:
            JSON string containing airport information
        """
        airport_code = arguments.get("airport_code")
        logger.info(f"Getting airport info for: {airport_code}")
        return travel_agent_service.get_airport_info(name, arguments)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="get_airport_info",
                description="Get information about an airport using Amadeus API.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "airport_code": {
                            "type": "string",
                            "description": "3-letter IATA airport code (e.g., LAX, JFK)",
                        }
                    },
                    "required": ["airport_code"],
                },
            )
        ]

    return app


def create_flight_mcp_server(server_name: str):
    """Create and configure the MCP server."""
    app = Server(server_name)

    @app.call_tool()
    async def search_flights_tool(
        name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        """
        Search for flights using Amadeus Search API.

        This MCP tool allows AI models to search for flight information by specifying
        departure and arrival airports and travel dates.

        Args:
            origin: Departure airport code (e.g., ATL, JFK)
            destination: Arrival airport code (e.g., LAX, ORD)
            departure_date: Departure date (YYYY-MM-DD)
            return_date: Return date for round trips (YYYY-MM-DD)

        Returns:
            A list of available flights with details
        """
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        logger.info(f"Getting flight search results for: {origin} - {destination}")
        return travel_agent_service.search_flights(name, arguments)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="flight_search_assistant",
                description="An intelligent agent that helps travelers find and recommend flights based on their itinerary, including origin, destination, and travel dates.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "Departure airport code (e.g., ATL, JFK)",
                        },
                        "destination": {
                            "type": "string",
                            "description": "Destination airport code (e.g., LAX, ORD)",
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "Departure date (YYYY-MM-DD)",
                        },
                        "return_date": {
                            "type": "string",
                            "description": "Return date (YYYY-MM-DD)",
                        },
                    },
                    "required": ["origin", "destination", "departure_date"],
                },
                outputSchema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "airline": {
                                "type": "string",
                                "description": "Name of the airline operating the flight.",
                            },
                            "price": {
                                "type": "string",
                                "description": "Total price for the flight, including currency.",
                            },
                            "duration": {
                                "type": "string",
                                "description": "Total duration of the flight.",
                            },
                            "stops": {
                                "type": "string",
                                "description": "Number of stops (e.g., Nonstop, 1 stop(s)).",
                            },
                            "departure": {
                                "type": "string",
                                "description": "Departure airport and time.",
                            },
                            "arrival": {
                                "type": "string",
                                "description": "Arrival airport and time.",
                            },
                            "travel_class": {
                                "type": "string",
                                "description": "Cabin class for the flight (e.g., Economy, Business).",
                            },
                        },
                    },
                },
            ),
        ]

    return app


def create_flight_inspiration_mcp_server(server_name: str):
    """Create and configure the MCP server."""
    app = Server(server_name)

    @app.call_tool()
    async def get_inspiration(
        name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        """
        Handle inspiration tool call
        """
        origin_airport_code = arguments.get("origin_airport_code")
        logger.info(f"Getting inspiration for: {origin_airport_code}")
        return travel_agent_service.get_travel_inspiration(name, arguments)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="get_inspiration",
                description="Help travelers discover their next destination by finding the cheapest flight destinations from a specific city",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin_airport_code": {
                            "type": "string",
                            "description": "3-letter IATA airport code (e.g., LAX, JFK)",
                        }
                    },
                    "required": ["origin_airport_code"],
                },
                outputSchema={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "origin": {
                                "type": "string",
                                "description": "Name and IATA code of the origin airport.",
                            },
                            "destination": {
                                "type": "string",
                                "description": "Name and IATA code of the destination airport.",
                            },
                            "departureDate": {
                                "type": "string",
                                "description": "Departure date in YYYY-MM-DD format.",
                            },
                            "returnDate": {
                                "type": "string",
                                "description": "Return date in YYYY-MM-DD format.",
                            },
                            "price": {
                                "type": "string",
                                "description": "Total price for the flight.",
                            },
                        },
                    },
                },
            ),
        ]

    return app


def create_trip_purpose_mcp_server(server_name: str):
    """Create and configure the MCP server."""
    app = Server(server_name)

    @app.call_tool()
    async def get_trip_purpose(
        name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        """
        Handle trip purpose tool call
        """
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        logger.info(f"Getting trip purpose for: {origin} to {destination}")
        return travel_agent_service.get_trip_purpose(name, arguments)

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List available tools."""
        return [
            types.Tool(
                name="get_trip_purpose",
                description="Predict the purpose of a trip (business or leisure)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "origin": {
                            "type": "string",
                            "description": "3-letter IATA code for the origin airport (e.g., 'LAX')",
                        },
                        "destination": {
                            "type": "string",
                            "description": "3-letter IATA code for the destination airport (e.g., 'JFK')",
                        },
                        "departure_date": {
                            "type": "string",
                            "description": "Departure date in YYYY-MM-DD format",
                        },
                        "return_date": {
                            "type": "string",
                            "description": "Return date in YYYY-MM-DD format",
                        },
                        "adults": {
                            "type": "integer",
                            "description": "Number of adult passengers",
                        },
                    },
                    "required": [
                        "origin",
                        "destination",
                        "departure_date",
                        "return_date",
                    ],
                },
            ),
        ]

    return app


def main(port: int = 8080, json_response: bool = False):
    """Main server function."""
    logging.basicConfig(level=logging.INFO)

    app = create_airport_mcp_server("airport_mcp_server")

    # Create session manager with stateless mode for scalability
    airport_session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=None,
        json_response=json_response,
        stateless=True,  # Important for Cloud Run scalability
    )

    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await airport_session_manager.handle_request(scope, receive, send)

    flight_app = create_flight_mcp_server("flight_mcp_server")

    # Create session manager with stateless mode for scalability
    flight_session_manager = StreamableHTTPSessionManager(
        app=flight_app,
        event_store=None,
        json_response=json_response,
        stateless=True,  # Important for Cloud Run scalability
    )

    async def handle_streamable_http_flight(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await flight_session_manager.handle_request(scope, receive, send)

    inspiration_app = create_flight_inspiration_mcp_server(
        "flight_inspiration_mcp_server"
    )
    # Create session manager with stateless mode for scalability
    inspiration_session_manager = StreamableHTTPSessionManager(
        app=inspiration_app,
        event_store=None,
        json_response=json_response,
        stateless=True,  # Important for Cloud Run scalability
    )

    async def handle_streamable_http_inspiration(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await inspiration_session_manager.handle_request(scope, receive, send)

    trip_purpose_app = create_trip_purpose_mcp_server("trip_purpose_mcp_server")
    # Create session manager with stateless mode for scalability
    trip_purpose_session_manager = StreamableHTTPSessionManager(
        app=trip_purpose_app,
        event_store=None,
        json_response=json_response,
        stateless=True,  # Important for Cloud Run scalability
    )

    async def handle_streamable_http_trip_purpose(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await trip_purpose_session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Manage session manager lifecycle."""
        # async with session_manager.run():
        async with contextlib.AsyncExitStack() as stack:
            await stack.enter_async_context(trip_purpose_session_manager.run())
            await stack.enter_async_context(inspiration_session_manager.run())
            await stack.enter_async_context(flight_session_manager.run())
            await stack.enter_async_context(airport_session_manager.run())
            logger.info("MCP Streamable HTTP server started!")
            try:
                yield
            finally:
                logger.info("MCP server shutting down...")

    starlette_app = Starlette(
        debug=False,  # Set to False for production
        routes=[
            Mount("/airport", app=handle_streamable_http),
            Mount("/flights", app=handle_streamable_http_flight),
            Mount("/inspiration", app=handle_streamable_http_inspiration),
            Mount("/trip-purpose", app=handle_streamable_http_trip_purpose),
        ],
        lifespan=lifespan,
    )

    import uvicorn

    uvicorn.run(starlette_app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main(port=8082)

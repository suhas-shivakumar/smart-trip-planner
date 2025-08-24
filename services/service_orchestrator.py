from typing import List, Dict, Optional, Any, Tuple
import logging
from amadeus import Client, ResponseError
from utils.custom_formatter import format_flight_results
import mcp.types as types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from services.amadeus_api_client import AmadeusAPI
from utils.custom_formatter import (
    format_airport_info_response,
    format_flight_results,
    format_inspiration_flights_response,
    format_trip_purpose_response,
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TravelAgentService:
    """Service class for orchestrating travel-related operations using Amadeus APIs.

    This class provides methods to:
    - Retrieve airport information based on IATA codes.
    - Search for flights between specified origins and destinations.
    - Predict the purpose of a trip (business or leisure).
    - Fetch inspirational flight destinations from a given origin.

    Attributes:
        logger: Logger instance for logging service activity.
        amadeus_api: Instance for interacting with Amadeus REST API endpoints.
        amadeus_client: Amadeus SDK client for advanced flight search operations.

    Methods:
        get_airport_info(name, arguments):
            Retrieves airport information for a given 3-letter airport code.

        search_flights(name, arguments):
            Searches for available flights based on origin, destination, and travel dates.

        prepare_flight_search_params(origin, destination, departure_date, return_date, passengers, class_preference):
            Prepares and returns parameters for flight search queries.

        get_trip_purpose(originLocationCode, destinationLocationCode, departureDate, adults):
            Predicts the purpose of a trip (business or leisure) using Amadeus API.

        get_inspiration_service(name, arguments):
            Fetches inspirational flight destinations from a specified origin airport.

    Exceptions:
        Raises McpError for invalid parameters or internal errors."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.amadeus_api = AmadeusAPI()
        self.amadeus_client = Client()

    def get_airport_info(
        self, name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        try:
            airport_code = arguments.get("airport_code")
            self.logger.info(f"Getting airport info for: {airport_code}")
            if not airport_code or len(airport_code.strip()) != 3:
                raise McpError(
                    ErrorData(
                        code=INVALID_PARAMS,
                        message="Valid 3-letter airport code is required (e.g., LAX, JFK)",
                    )
                )
            airport_code = airport_code.strip().upper()
            params = {"keyword": airport_code, "subType": "AIRPORT,CITY"}
            result = self.amadeus_client.reference_data.locations.get(**params).result
            return format_airport_info_response(result, airport_code)
        except McpError:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error getting airport info: {str(e)}")
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to get airport information: {str(e)}",
                )
            ) from e

    def search_flights(
        self, name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:
        origin = arguments.get("origin")
        destination = arguments.get("destination")
        departure_date = arguments.get("departure_date")
        return_date = arguments.get("return_date", "")
        self.logger.info(
            f"Searching flights: {origin} to {destination}, dates: {departure_date} - {return_date}"
        )
        params = self.prepare_flight_search_params(
            origin, destination, departure_date, return_date
        )
        self.logger.info("Executing Amadeus API search...")
        search_results = self.amadeus_client.shopping.flight_offers_search.get(
            **params
        ).result
        if "error" in search_results:
            self.logger.error(f"Amadeus API search error: {search_results['error']}")
            return [{"error": search_results["error"]}]
        return format_flight_results(search_results)

    def prepare_flight_search_params(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        return_date: Optional[str] = None,
        passengers: int = 1,
        class_preference: str = "ECONOMY",
    ) -> Dict[str, Any]:
        params = {
            "originLocationCode": origin.upper(),
            "destinationLocationCode": destination.upper(),
            "departureDate": departure_date,
            "adults": passengers,
            "travelClass": class_preference.upper(),
            "nonStop": "false",
            "max": 5,
        }
        if return_date:
            params["returnDate"] = return_date
        return params

    def get_trip_purpose(self, name: str, arguments: dict[str, Any]) -> Dict[str, Any]:
        """
        Predicts the purpose of a trip (e.g., BUSINESS or LEISURE).

        Args:
            originLocationCode: IATA code for the origin airport (e.g., 'MAD').
            destinationLocationCode: IATA code for the destination airport (e.g., 'NYC').
            departureDate: The departure date in YYYY-MM-DD format.
            adults: The number of adult passengers.

        Returns:
            A dictionary containing the predicted trip purpose.
        """
        try:
            origin = arguments.get("origin")
            destination = arguments.get("destination")
            departure_date = arguments.get("departure_date")
            return_date = arguments.get("return_date")
            adults = arguments.get("adults", 1)

            params = {
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDate": departure_date,
                "returnDate": return_date,
                "adults": str(adults),
            }
            # Make the API call to Amadeus
            self.logger.info("Executing Amadeus API...")
            trip_purpose_response = (
                self.amadeus_client.travel.predictions.trip_purpose.get(**params).result
            )
            return format_trip_purpose_response(trip_purpose_response, arguments)

        except ResponseError as e:
            return {"error": f"Tripo purpose API Error: {str(e)}", "details": e.args}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}

    def get_travel_inspiration(
        self, name: str, arguments: dict[str, Any]
    ) -> Tuple[list[types.ContentBlock], dict[str, Any]]:

        try:
            # Validate input
            origin_airport_code = arguments.get("origin_airport_code")
            logger.info(f"Getting inspiration for: {origin_airport_code}")
            if not origin_airport_code or len(origin_airport_code.strip()) != 3:
                raise McpError(
                    ErrorData(
                        code=INVALID_PARAMS,
                        message="Valid 3-letter airport code is required (e.g., LAX, JFK)",
                    )
                )

            origin_airport_code = origin_airport_code.strip().upper()
            logger.info(f"Getting inspiration for: {origin_airport_code}")

            result = self.amadeus_client.shopping.flight_destinations.get(
                origin=origin_airport_code
            ).result

            return format_inspiration_flights_response(result, origin_airport_code)

        except McpError:
            # Re-raise MCP errors
            raise
        except Exception as e:
            logger.error(f"Unexpected error for inspiration: {str(e)}")
            raise McpError(
                ErrorData(
                    code=INTERNAL_ERROR,
                    message=f"Failed to fetch inspiration: {str(e)}",
                )
            ) from e

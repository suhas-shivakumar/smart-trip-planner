import mcp.types as types
import json
from typing import Any, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def format_flight_results(flight_data: Dict[str, Any]) -> List[Dict[str, str]]:
    if "error" in flight_data:
        logger.error(f"Flight search error in formatter: {flight_data['error']}")
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "status": "error",
                        "message": flight_data["error"],
                        "raw_result": flight_data,
                    },
                    indent=2,
                ),
            )
        ], flight_data

    if not flight_data.get("data"):
        logger.info("No flight offers found in the Amadeus response.")
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "status": "not_found",
                        "message": "No flight offers found.",
                        "raw_result": flight_data,
                    },
                    indent=2,
                ),
            )
        ], flight_data

    flight_offers = flight_data.get("data", [])
    dictionaries = flight_data.get("dictionaries", {})
    carriers = dictionaries.get("carriers", {})

    formatted_flights = []
    for offer in flight_offers:
        try:
            itinerary = offer["itineraries"][0]
            first_segment = itinerary["segments"][0]
            last_segment = itinerary["segments"][-1]
            carrier_code = first_segment["carrierCode"]
            airline = carriers.get(carrier_code, "Unknown Airline")
            price = offer["price"]["total"]
            currency = offer["price"]["currency"]
            dep_info = f"{first_segment['departure']['iataCode']} at {first_segment['departure']['at']}"
            arr_info = f"{last_segment['arrival']['iataCode']} at {last_segment['arrival']['at']}"
            traveler_pricing = offer["travelerPricings"][0]
            fare_details = traveler_pricing["fareDetailsBySegment"][0]
            travel_class = fare_details.get("cabin", "Economy")
            stops = len(itinerary["segments"]) - 1
            stops_str = "Nonstop" if stops == 0 else f"{stops} stop(s)"
            formatted_flights.append(
                {
                    "airline": airline,
                    "price": f"{price} {currency}",
                    "duration": itinerary["duration"],
                    "stops": stops_str,
                    "departure": dep_info,
                    "arrival": arr_info,
                    "travel_class": travel_class,
                }
            )
        except (KeyError, IndexError) as e:
            logger.error(f"Could not parse a flight offer due to missing data: {e}")
            continue

    logger.info(f"Returning {len(formatted_flights)} formatted flights")
    return [
        types.TextContent(
            type="text",
            text=json.dumps({"status": "success", "data": formatted_flights}, indent=2),
        )
    ], flight_data


def format_airport_info_response(result, airport_code):
    """Format the response for airport info tool."""

    if not isinstance(result, dict) or "data" not in result:
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "airport_code": airport_code,
                        "status": "error",
                        "raw_result": result,
                    },
                    indent=2,
                ),
            )
        ]
    # Find exact matches
    data = result.get("data", [])
    airport_info = [
        loc
        for loc in data
        if loc.get("iataCode") == airport_code
        or airport_code in loc.get("name", "").upper()
    ]
    if airport_info:
        logger.info(f"Returning airport information {airport_info}")
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "airport_code": airport_code,
                        "status": "success",
                        "data": airport_info,
                    },
                    indent=2,
                ),
            )
        ]
    return [
        types.TextContent(
            type="text",
            text=json.dumps(
                {
                    "airport_code": airport_code,
                    "status": "not_found",
                    "message": f"No airport found for code: {airport_code}",
                    "all_results": data,
                },
                indent=2,
            ),
        )
    ]


def format_inspiration_flights_response(result, origin_airport_code):
    if isinstance(result, dict) and "data" in result:
        locations = result.get("dictionaries", {}).get("locations", {})
        output = []
        for data in result["data"]:
            output.append(
                {
                    "origin": f"{locations.get(data.get('origin', '')).get('detailedName', '')} ({data.get('origin', '')})",
                    "destination": f"{locations.get(data.get('destination', '')).get('detailedName', '')} ({data.get('destination', '')})",
                    "departureDate": f"{data.get('departureDate', '')}",
                    "returnDate": f"{data.get('returnDate', '')}",
                    "price": f"{data.get('price', '').get('total', '')}",
                }
            )

        if output:
            logger.info(f"Returning {len(output)} flight inspiration information ")
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "origin_airport_code": origin_airport_code,
                            "status": "success",
                            "data": output,
                        },
                        indent=2,
                    ),
                )
            ], result

        else:
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "origin_airport_code": origin_airport_code,
                            "status": "not_found",
                            "message": f"No inspiration found: {origin_airport_code}",
                            "all_results": result.get("data", []),
                        },
                        indent=2,
                    ),
                )
            ], result

    else:
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "origin_airport_code": origin_airport_code,
                        "status": "error",
                        "raw_result": result,
                    },
                    indent=2,
                ),
            )
        ], result


def format_trip_purpose_response(result, arguments):
    """Format the response for trip purpose tool."""
    origin = arguments.get("origin")
    destination = arguments.get("destination")
    departure_date = arguments.get("departure_date")
    return_date = arguments.get("return_date")

    if not isinstance(result, dict) or "data" not in result:
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "origin": origin,
                        "destination": destination,
                        "status": "error",
                        "raw_result": result,
                    },
                    indent=2,
                ),
            )
        ]

    data = result.get("data")
    purpose = data.get("result", None)
    if purpose:
        logger.info(f"Returning trip purpose information {purpose}")
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date,
                        "return_date": return_date,
                        "trip_purpose": purpose,
                        "status": "success",
                    },
                    indent=2,
                ),
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    {
                        "status": "not_found",
                        "message": f"No trip purpose found for the itinerary: {origin} to {destination}",
                        "raw_results": data,
                    },
                    indent=2,
                ),
            )
        ]

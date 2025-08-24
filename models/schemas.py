from pydantic import BaseModel, Field
from typing import Optional


# Airport Info Model
class AirportInfo(BaseModel):
    iataCode: str = Field(..., description="3-letter IATA airport code")
    name: str = Field(..., description="Airport name")
    cityName: Optional[str] = Field(None, description="City name")
    countryName: Optional[str] = Field(None, description="Country name")
    detailedName: Optional[str] = Field(None, description="Detailed airport name")


# Flight Search Model
class FlightSearch(BaseModel):
    airline: str = Field(..., description="Name of the airline operating the flight")
    price: str = Field(
        ..., description="Total price for the flight, including currency"
    )
    duration: str = Field(..., description="Total duration of the flight")
    stops: str = Field(..., description="Number of stops (e.g., Nonstop, 1 stop(s))")
    departure: str = Field(..., description="Departure airport and time")
    arrival: str = Field(..., description="Arrival airport and time")
    travel_class: str = Field(
        ..., description="Cabin class for the flight (e.g., Economy, Business)"
    )


# Inspiration Flight Model
class InspirationFlight(BaseModel):
    origin: str = Field(..., description="Name and IATA code of the origin airport")
    destination: str = Field(
        ..., description="Name and IATA code of the destination airport"
    )
    departureDate: str = Field(..., description="Departure date in YYYY-MM-DD format")
    returnDate: str = Field(..., description="Return date in YYYY-MM-DD format")
    price: str = Field(..., description="Total price for the flight")


# Trip Purpose Model
class TripPurpose(BaseModel):
    origin: str = Field(..., description="Name or IATA code of the origin airport")
    destination: str = Field(
        ..., description="Name or IATA code of the destination airport"
    )
    departureDate: str = Field(..., description="Departure date in YYYY-MM-DD format")
    returnDate: str = Field(..., description="Return date in YYYY-MM-DD format")
    purpose: str = Field(
        ..., description="Predicted purpose of the trip (e.g., Business, Leisure)"
    )


# Request Models (for input validation)
class AirportInfoRequest(BaseModel):
    airport_code: str = Field(..., description="3-letter IATA airport code")


class FlightSearchRequest(BaseModel):
    origin: str = Field(..., description="Departure airport code")
    destination: str = Field(..., description="Arrival airport code")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date (YYYY-MM-DD)")


class InspirationFlightRequest(BaseModel):
    origin: str = Field(..., description="Departure airport code")
    destination: Optional[str] = Field(None, description="Destination airport code")
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: Optional[str] = Field(None, description="Return date (YYYY-MM-DD)")


class TripPurposeRequest(BaseModel):
    origin: str = Field(..., description="Name or IATA code of the origin airport")
    destination: str = Field(
        ..., description="Name or IATA code of the destination airport"
    )
    departure_date: str = Field(..., description="Departure date (YYYY-MM-DD)")
    return_date: str = Field(..., description="Return date (YYYY-MM-DD)")

import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Departure(BaseModel):
    at: Optional[datetime]
    airport: Optional[str]


class Arrival(BaseModel):
    at: Optional[datetime]
    airport: Optional[str]


class Segment(BaseModel):
    operating_airline: Optional[str]
    marketing_airline: Optional[str]
    flight_number: Optional[int]
    equipment: Optional[str]
    dep: Optional[Departure]
    arr: Optional[Arrival]
    baggage: Optional[str]


class Flight(BaseModel):
    duration: Optional[int]
    segments: Optional[List[Segment]]


class Pricing(BaseModel):
    total: Optional[float]
    base: Optional[float]
    taxes: Optional[float]
    currency: Optional[str]


class Flights(BaseModel):
    flights: List[Flight]
    refundable: Optional[bool]
    validating_airline: Optional[str]
    pricing: Optional[Pricing]


class Search(BaseModel):
    search_id: uuid.UUID
    status: str
    items: Optional[List[Flights]] = []

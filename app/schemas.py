from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Request-এ যা আসবে
class FlightCreate(BaseModel):
    flight_number: str = Field(..., min_length=3, max_length=10)
    origin: str = Field(..., min_length=3, max_length=3)
    destination: str = Field(..., min_length=3, max_length=3)
    departure_time: datetime
    status: Optional[str] = "Scheduled"


# Response-এ যা যাবে
class FlightResponse(BaseModel):
    id: int
    flight_number: str
    origin: str
    destination: str
    departure_time: datetime
    status: str
    created_at: datetime

    class Config:
        from_attributes = True   # SQLAlchemy object → Pydantic
        
# app/schemas.py
class StatusUpdate(BaseModel):
    status: str = Field(..., min_length=3, max_length=20)
    
# app/schemas.py

class PassengerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    passport_number: str = Field(..., min_length=6, max_length=20)
    seat_number: Optional[str] = None
    flight_id: int


class PassengerResponse(BaseModel):
    id: int
    name: str
    passport_number: str
    seat_number: Optional[str]
    flight_id: int
    created_at: datetime

    class Config:
        from_attributes = True
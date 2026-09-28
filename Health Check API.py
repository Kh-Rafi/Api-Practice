from fastapi import FastAPI, HTTPException
from datetime import datetime
from pydantic import BaseModel
from typing import List

# Initialize the FastAPI application
app = FastAPI(title="Airport Backend API")

# 1. Fixed the 'clss' typo to 'class'
class Flight(BaseModel):
    flight_number: str
    origin: str
    destination: str
    departure_time: str
    status: str
    
flights_db = [
    {"flight_number": "BG101", "origin": "DAC", "destination": "CXB", 
     "departure_time": "2024-01-15T10:00", "status": "On Time"},
    {"flight_number": "BG102", "origin": "DAC", "destination": "JFK",
     "departure_time": "2024-01-15T14:30", "status": "Delayed"},
]

@app.get("/")
async def read_root():
    """Root endpoint to handle baseline traffic."""
    return {
        "message": "Welcome to the Airport Backend API!",
        "documentation": "/docs",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint to monitor service availability."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "airport-backend"
    }

# 2. Fixed order/logic: Changed this route to return ALL flights. 
# Removed the duplicate 'flight_number' parameter that conflicted with the path route.
@app.get("/flights", response_model=List[Flight])
async def get_all_flights():
    return flights_db

# 3. Fixed the parameter typo '{fkight_number}' to '{flight_number}'
# 4. Fixed the indentation error before 'async def'
@app.get("/flights/{flight_number}", response_model=Flight)
async def get_flight_by_number(flight_number: str):
    for flight in flights_db:
        if flight["flight_number"] == flight_number:
            return flight 
    raise HTTPException(status_code=404, detail="Flight Not Found")

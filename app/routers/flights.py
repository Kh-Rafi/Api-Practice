from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session                      # ✅ uppercase
from typing import List, Optional
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/flights", tags=["Flights"])  # ✅ "s" যোগ


@router.post("/", response_model=schemas.FlightResponse,
             status_code=status.HTTP_201_CREATED)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):   # ✅
    existing = db.query(models.Flight).filter(
        models.Flight.flight_number == flight.flight_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Flight {flight.flight_number} already exists"
        )

    new_flight = models.Flight(**flight.model_dump())
    db.add(new_flight)
    db.commit()
    db.refresh(new_flight)
    return new_flight


@router.get("/", response_model=List[schemas.FlightResponse])
def get_flights(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Flight)

    if status:
        query = query.filter(models.Flight.status == status)

    flights = query.offset(skip).limit(limit).all()
    return flights


@router.patch("/{flight_id}/status", response_model=schemas.FlightResponse)
def update_flight_status(
    flight_id: int,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(get_db)
):
    flight = db.query(models.Flight).filter(
        models.Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail=f"Flight with id {flight_id} not found"
        )

    flight.status = status_update.status

    db.commit()
    db.refresh(flight)

    return flight


@router.delete("/{flight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flight(
    flight_id: int,
    db: Session = Depends(get_db)
):
    flight = db.query(models.Flight).filter(
        models.Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail=f"Flight with id {flight_id} not found"
        )

    db.delete(flight)
    db.commit()

    return None
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.security import require_role

router = APIRouter(prefix="/passengers", tags=["Passengers"])


# ═══════════════════════════════════════════
# CREATE Passenger (admin, staff only)
# ═══════════════════════════════════════════
@router.post("/", response_model=schemas.PassengerResponse,
             status_code=status.HTTP_201_CREATED)
def create_passenger(
    passenger: schemas.PassengerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "staff"))
):
    # Step 1: Flight exist করে কিনা check করো
    flight = db.query(models.Flight).filter(
        models.Flight.id == passenger.flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail=f"Flight with id {passenger.flight_id} not found"
        )

    # Step 2: Passport duplicate check
    existing = db.query(models.Passenger).filter(
        models.Passenger.passport_number == passenger.passport_number
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Passport {passenger.passport_number} already registered"
        )

    # Step 3: নতুন passenger বানাও
    new_passenger = models.Passenger(**passenger.model_dump())
    db.add(new_passenger)
    db.commit()
    db.refresh(new_passenger)
    return new_passenger
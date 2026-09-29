from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    status = Column(String, default="Scheduled")
    created_at = Column(DateTime, server_default=func.now())

    # ⭐ NEW: One-to-Many relationship
    passengers = relationship("Passenger", back_populates="flight")


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    passport_number = Column(String, unique=True, index=True, nullable=False)
    seat_number = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # ⭐ NEW: Foreign Key to Flight
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)

    # ⭐ NEW: Reverse relationship
    flight = relationship("Flight", back_populates="passengers")
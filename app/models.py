from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


# ═══════════════════════════════════════════
# FLIGHT
# ═══════════════════════════════════════════
class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String, unique=True, index=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    status = Column(String, default="Scheduled")
    created_at = Column(DateTime, server_default=func.now())

    # One-to-Many: এক Flight → অনেক Passenger
    passengers = relationship("Passenger", back_populates="flight")


# ═══════════════════════════════════════════
# PASSENGER
# ═══════════════════════════════════════════
class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    passport_number = Column(String, unique=True, index=True, nullable=False)
    seat_number = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Foreign Key → Flight
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)

    # Reverse relationship
    flight = relationship("Flight", back_populates="passengers")


# ═══════════════════════════════════════════
# USER (Day 5 — Authentication)
# ═══════════════════════════════════════════
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="passenger")   # "admin", "staff", "passenger"
    is_active = Column(String, default="true")
    created_at = Column(DateTime, server_default=func.now())
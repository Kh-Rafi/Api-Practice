from fastapi import FastAPI
from app.database import engine, Base
from app.routers import flights ,passengers

# Table create (পরে Alembic migration এ নিয়ে যাবো)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Airport Backend API",
    description="Flight management system for airport operations",
    version="1.0.0"
)

app.include_router(flights.router)
app.include_router(passengers.router)


@app.get("/health")
def health():
    return {"status": "healthy"}
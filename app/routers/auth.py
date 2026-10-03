from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, security
from app.database import get_db
from app.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ═══════════════════════════════════════════
# REGISTER
# ═══════════════════════════════════════════
@router.post("/register", response_model=schemas.UserResponse,
             status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Step 1: Email duplicate check
    existing = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Step 2: Password hash করো
    hashed = security.hash_password(user.password)

    # Step 3: User বানাও
    new_user = models.User(
        email=user.email,
        hashed_password=hashed,
        full_name=user.full_name,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ═══════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════
@router.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Step 1: User খুঁজো
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    # Step 2: Email বা password ভুল
    if not user or not security.verify_password(
        credentials.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Step 3: JWT token বানাও
    token = security.create_access_token(data={"sub": user.email})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Token verify করে current user return করে"""
    return current_user
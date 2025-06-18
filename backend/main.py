# backend/main.py

from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI TaskMaster API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ─── EVENTS ROUTER ───────────────────────────────────────────────────────────────

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    """Get all events"""
    return db.query(models.Event).all()

@router.get("/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event by ID"""
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(get_db)):
    """Update an existing event"""
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event"""
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted successfully"}


# Register the events router with the main app
app.include_router(router)


# ─── HOSTS ENDPOINT ─────────────────────────────────────────────────────────────

@app.get("/hosts", response_model=List[schemas.Host])
def get_hosts(db: Session = Depends(get_db)):
    """Get all hosts (and seed sample data if empty)"""
    hosts = db.query(models.Host).all()
    if not hosts:
        sample_hosts = [
            models.Host(gpn="43746091", name="MUHAMMAD AZLAN BIN HASSAN"),
            models.Host(gpn="43746115", name="CHEW SHI DA, ERIC")
        ]
        for host in sample_hosts:
            db.add(host)
        db.commit()
        hosts = db.query(models.Host).all()
    return hosts


# ─── RUN UVCORN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

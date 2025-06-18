from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_date = Column(String, nullable=False)
    status = Column(Integer, default=0)  # 0 = open, 1 = fully booked, 2 = completed
    rsvp_by = Column(String, nullable=False)
    event_title = Column(String, nullable=False)
    event_host = Column(String, nullable=False)
    event_location = Column(String, nullable=False)
    pax = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Host(Base):
    __tablename__ = "hosts"
    
    id = Column(Integer, primary_key=True, index=True)
    gpn = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

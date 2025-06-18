from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    event_date: str
    status: int = 0
    rsvp_by: str
    event_title: str
    event_host: str
    event_location: str
    pax: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    event_date: Optional[str] = None
    status: Optional[int] = None
    rsvp_by: Optional[str] = None
    event_title: Optional[str] = None
    event_host: Optional[str] = None
    event_location: Optional[str] = None
    pax: Optional[str] = None

class Event(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True #ADDITION
        from_attributes = True

class HostBase(BaseModel):
    gpn: str
    name: str

class Host(HostBase):
    id: int
    
    class Config:
        from_attributes = True

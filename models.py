# file: models.py

from pydantic import BaseModel, EmailStr
from datetime import datetime

class Email(BaseModel):
    """A Pydantic model to represent a processed email."""
    id: str
    sender: str  # We'll keep it simple as a string for now
    subject: str
    body: str
    received_at: datetime
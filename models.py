from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Email(BaseModel):
    """A Pydantic model to represent a processed email."""
    id: str
    sender: str 
    subject: str
    body: str
    received_at: datetime
    category: Optional[str] = None
    summary: Optional[str] = None
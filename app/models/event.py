from pydantic import BaseModel
from datetime import datetime

# Define the keywords as a constant
KEYWORDS = ["checkpoint", "avanan", "email", "security"]

class Event(BaseModel):
    sentence: str
    timestamp: datetime = datetime.now()

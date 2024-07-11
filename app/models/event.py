from pydantic import BaseModel

# Define the keywords as a constant
KEYWORDS = ["checkpoint", "avanan", "email", "security"]

class Event(BaseModel):
    sentence: str

from fastapi import APIRouter, Depends
from app.models.event import Event
from app.models.event_service import EventService

router = APIRouter()
event_service: EventService = None


def set_event_service(service: EventService):
    global event_service
    event_service = service


def get_event_service() -> EventService:
    return event_service


@router.post("/events")
async def create_event(event: Event, event_service: EventService = Depends(get_event_service)):
    event_service.process_event(event.sentence)
    # Retrieve the last event's elapsed time
    elapsed_time = event_service.get_stats_time()[-1][0]
    return {
        "message": "Your sentence was received",
        "elapsed_time": elapsed_time
    }

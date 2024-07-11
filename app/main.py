from fastapi import FastAPI
from app.api import events, stats
from app.models.event_service import EventService
from app.models.stats_service import StatsService
import uvicorn
import time

app = FastAPI()

# Initialize EventService and StatsService
event_service = EventService()
stats_service = StatsService(event_service)

@app.on_event("startup")
async def startup_event():
    # Pass the initialized services to the routers
    events.set_event_service(event_service)
    stats.set_stats_service(stats_service)

@app.get("/")
async def read_root():
    elapsed_time = int(time.time() - event_service.start_time)
    current_counts = event_service.get_keyword_counts()
    return {
        "message": "Welcome to the event service! Here in root directory, you can see the current keyword counts and "
                   "TIME since the service started.",
        "elapsed_time": elapsed_time,
        "keyword_counts": current_counts
    }

app.include_router(events.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

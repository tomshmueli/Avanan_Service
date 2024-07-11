from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Dict, Optional
from app.models.stats_service import StatsService

router = APIRouter()
stats_service: StatsService = None


def set_stats_service(service: StatsService):
    global stats_service
    stats_service = service


def get_stats_service() -> StatsService:
    return stats_service


@router.get("/stats")
async def get_stats(
        start: Optional[int] = Query(None),
        end: Optional[int] = Query(None),
        stats_service: StatsService = Depends(get_stats_service)  # Dependency Injection
) -> Dict[str, int]:
    try:
        return stats_service.get_stats(start, end)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

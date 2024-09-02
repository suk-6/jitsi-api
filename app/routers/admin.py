from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.services.admin import get_rooms, get_video


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@router.get("/rooms")
async def get():
    rooms = await get_rooms()
    return rooms


@router.get("/video", response_class=FileResponse)
async def get(room_id: str):
    path = await get_video(room_id)
    return path

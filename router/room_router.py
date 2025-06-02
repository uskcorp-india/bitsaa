from fastapi import APIRouter, Request
from handler.room_handler import get_rooms

router = APIRouter()

@router.get("/rooms")
async def get_all_rooms():
    return await get_rooms()
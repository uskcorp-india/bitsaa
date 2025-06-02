from fastapi import APIRouter, Request
from handler.booking_handler import create_booking

router = APIRouter()

@router.post("/book")
async def book_room(request: Request):
    data = await request.json()
    return await create_booking(data)
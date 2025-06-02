from fastapi import APIRouter, HTTPException, Request
import handler.booking_handler as booking_handler
from utils.logger_factory import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/user/booking", tags=['booking'])

@router.get("/")
async def get(request: Request):
    request_body = await request.json()
    booking = booking_handler.find(request_body.get('booking_id'))
    if booking:
        return booking
    raise HTTPException(status_code=404, detail="booking s not found")

@router.post("/")
async def create(request: Request):
    body = await request.json()
    created_booking = booking_handler.create(body)
    logger.info(created_booking)
    if created_booking:
        return created_booking
    raise HTTPException(status_code=400, detail="Failed to create booking")

@router.put("/")
async def update(request: Request):
    body = await request.json()
    updated_booking = booking_handler.update( body)
    if updated_booking:
        return updated_booking
    raise HTTPException(status_code=400, detail="Failed to update booking")

@router.delete("/")
async def delete(request: Request):
    request_body = await request.json()
    deleted_booking = booking_handler.delete(request_body.get('booking_id'))
    if deleted_booking:
        return deleted_booking
    raise HTTPException(status_code=400, detail="Failed to delete booking")
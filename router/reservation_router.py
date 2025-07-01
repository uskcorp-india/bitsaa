from fastapi import APIRouter,HTTPException,Request
import handler.reservation_handler as reservation_handler
from utils.logger_factory import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/reservation", tags=['reservation'])

@router.get("/{reservation_id}")
async def find(reservation_id):
    reservation = reservation_handler.find(reservation_id)
    if reservation:
        return reservation
    raise HTTPException(status_code=404, detail="reservation not found")

@router.post("")
async def create(request: Request):
    request_body = await request.json()
    created_reservation = reservation_handler.create(request_body)
    logger.info(created_reservation)
    if created_reservation:
        return created_reservation
    raise HTTPException(status_code=400, detail="Failed to create reservation")

@router.put("/{reservation_id}")
async def update(reservation_id,request: Request):
    request_body = await request.json()
    updated_reservation = reservation_handler.update(reservation_id,request_body)
    if updated_reservation:
        return updated_reservation
    raise HTTPException(status_code=400, detail="Failed to update reservation")

@router.delete("")
async def delete(request: Request):
    request_body = await request.json()
    deleted_reservation = reservation_handler.delete(request_body.get('reservation_id'))
    if deleted_reservation:
        return deleted_reservation
    raise HTTPException(status_code=400, detail="Failed to delete ")
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
import handler.confirm_handler as confirm_handler
from utils.logger_factory import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/reservation", tags=['confirm'])


@router.post("/{reservation_id}/confirm")
async def create(reservation_id:str, request: Request):
    request_body = await request.json()
    create_confirm = confirm_handler.create(reservation_id,request_body)
    logger.info(create_confirm)
    if create_confirm:
        return create_confirm
    raise HTTPException(status_code=400, detail="Failed to create registration")
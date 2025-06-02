from fastapi import APIRouter, HTTPException, Request
import handler.registration_handler as registration_handler
from utils.logger_factory import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/registration", tags=['registration'])

@router.get("/")
async def find(request: Request):
    request_body = await request.json()
    registration = registration_handler.find(request_body.get('registration_id'))
    if registration:
        return registration
    raise HTTPException(status_code=404, detail="registration s not found")

@router.post("/")
async def create(request: Request):
    request_body = await request.json()
    create_registration = registration_handler.create(request_body)
    logger.info(create_registration)
    if create_registration:
        return create_registration
    raise HTTPException(status_code=400, detail="Failed to create registration")

@router.put("/")
async def update(request: Request):
    request_body = await request.json()
    updated_registration = registration_handler.update(request_body)
    if updated_registration:
        return registration_handler
    raise HTTPException(status_code=400, detail="Failed to update registration")

@router.delete("/")
async def delete(request: Request):
    request_body = await request.json()
    deleted_registration = registration_handler.delete(request_body.get('registration_id'))
    if deleted_registration:
        return deleted_registration
    raise HTTPException(status_code=400, detail="Failed to delete registration")
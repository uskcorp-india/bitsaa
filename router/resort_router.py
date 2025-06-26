from fastapi import APIRouter, HTTPException, Request
import handler.resort_handler as resort_handler
from utils.logger_factory import get_logger
logger = get_logger(__name__)

router = APIRouter(prefix="/resort", tags=['resort'])

@router.get("")
async def find():
    resort = resort_handler.find_all()
    if resort:
        resort[0].append({"message": "Resorts fetched successfully"})
        return resort[0]
    raise HTTPException(status_code=404, detail="resort s not found")

@router.post("")
async def create(request: Request):
    request_body = await request.json()
    created_resort = resort_handler.create(request_body)
    logger.info(created_resort)
    if created_resort:
        return created_resort
    raise HTTPException(status_code=400, detail="Failed to create resort")

@router.put("/{resort_id}")
async def update(resort_id, request: Request):
    request_body = await request.json()
    updated_resort = resort_handler.update(resort_id,request_body)
    if updated_resort:
        return updated_resort
    raise HTTPException(status_code=400, detail="Failed to update resort")

@router.delete("")
async def delete(request: Request):
    request_body = await request.json()
    deleted_resort = resort_handler.delete(request_body.get('resort_id'))
    if deleted_resort:
        return deleted_resort
    raise HTTPException(status_code=400, detail="Failed to  delete the resort ")
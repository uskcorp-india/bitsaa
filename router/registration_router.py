from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.requests import Request
import handler.registration_handler as registration_handler
from utils.email_utils import send_welcome_email
from utils.logger_factory import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/registration", tags=['registration'])

@router.get("/{registration_id}")
async def find(registration_id):
    registration = registration_handler.find(registration_id)
    if registration:
        return registration
    raise HTTPException(status_code=404, detail="registration s not found")

@router.post("")
async def create(request: Request, background_tasks: BackgroundTasks):
    request_body = await request.json()
    logger.info(f"request_body++: {request_body}")
    object_type = request_body.get("objectType")
    if object_type == "ticket":
        request_body['registration_no'] = request_body.get("ticketId")
        create_registration = registration_handler.create(request_body)
        logger.info(create_registration)

        if create_registration:
            return create_registration
        raise HTTPException(status_code=400, detail="Failed to create registration")
    elif object_type == "transaction":
        first_name = request_body.get("userName", "Guest").split()[0]
        recipient_email = request_body.get("userEmail")
        order_id = request_body.get("orderId")
        ticket_count = request_body.get("ticketCount", 1)
        background_tasks.add_task(
            send_welcome_email, recipient_email, first_name, order_id, ticket_count
        )
        return {
            "status": True,
            "message": "Email is being sent",
            "status_code": 200,
            "data": None
        }

    else:
        raise HTTPException(status_code=400, detail="Invalid objectType")

@router.put("/{registration_id}")
async def update(registration_id,request: Request):
    request_body = await request.json()
    updated_registration = registration_handler.update(registration_id,request_body)
    if updated_registration:
        return updated_registration
    raise HTTPException(status_code=400, detail="Failed to update registration")

@router.delete("")
async def delete(request: Request):
    request_body = await request.json()
    deleted_registration = registration_handler.delete(request_body.get('registration_id'))
    if deleted_registration:
        return deleted_registration
    raise HTTPException(status_code=400, detail="Failed to delete registration")
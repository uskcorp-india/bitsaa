from fastapi import APIRouter, Request
from handler.registration_handler import register_user

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    return await register_user(data)
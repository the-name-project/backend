from fastapi import APIRouter
from app.user.router import router as user

router = APIRouter()

router.include_router(user, prefix="/users", tags=["users"])
from app.api.endpoints import auth, bot
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(bot.router)

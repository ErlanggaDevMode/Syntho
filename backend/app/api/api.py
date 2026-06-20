from app.api.endpoints import auth, bot, notes, transactions
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(bot.router)
api_router.include_router(transactions.router)
api_router.include_router(notes.router)

import logging
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Setup structured logging before any logger instantiation
setup_logging()
logger = logging.getLogger("syntho-backend")


from app.core.scheduler import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Syntho Backend...")
    import sys
    if "pytest" not in sys.modules:
        start_scheduler()
    yield
    logger.info("Shutting down Syntho Backend...")
    if "pytest" not in sys.modules:
        shutdown_scheduler()


app = FastAPI(
    title="Syntho API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.TELEGRAM_BOT_MODE == "polling" else None,
    redoc_url=None,
)

# CORS configuration - strict, trusted origins only
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; frame-ancestors 'none';"
        )
        return response


app.add_middleware(SecurityHeadersMiddleware)


# Database Error Handler to prevent leaking internal queries/details to clients
@app.exception_handler(SQLAlchemyError)
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.exception("SQLAlchemy query execution failed")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred during database access."},
    )


# Include all v1 routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

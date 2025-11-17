"""
CollectFlowAPI - Main Application Entry Point
============================================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: FastAPI application for managing practices, movements, emails, and SMS
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module initializes the FastAPI application with all middleware, routers,
and global exception handlers.
"""

import logging
from logging.handlers import TimedRotatingFileHandler
import sys
from datetime import datetime
import os

# Import config first
from app.config import LOG_PATH, LOG_LEVEL, LOG_TO_STDOUT

# 1) Configura il formatter "elegante"
formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-5s [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Create logger first
logger = logging.getLogger(__name__)

# 2) Handler per il file con rotazione giornaliera (solo se LOG_TO_STDOUT=False)
file_handler = None
if not LOG_TO_STDOUT:
    try:
        # Ensure log directory exists
        log_dir = os.path.dirname(LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = TimedRotatingFileHandler(
            filename=LOG_PATH,
            when="midnight",
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))
        logger.info(f"File logging enabled: {LOG_PATH}")
    except Exception as e:
        logger.warning(f"Could not create file handler: {e}")
        file_handler = None
else:
    logger.info("Logging to stdout/stderr enabled")

# 3) Handler per la console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(getattr(logging, LOG_LEVEL.upper()))

# 4) Handler per errori (stderr)
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

# 4) Imposta il root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Remove any existing handlers to avoid duplicates
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add our handlers
root_logger.addHandler(console_handler)
root_logger.addHandler(error_handler)

# Add file handler only if it exists
if file_handler:
    root_logger.addHandler(file_handler)

# Log application startup
logger.info("Starting CollectFlowAPI application")

# Configure uvicorn logging to use our configuration
import uvicorn.config
uvicorn.config.LOGGING_CONFIG["disable_existing_loggers"] = True

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.middleware import LoggingMiddleware
from app.routers.pratiche import router as pratiche_router
from app.routers.movimenti import router as movimenti_router
from app.routers.email import router as email_router
from app.routers.sms import router as sms_router

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(
    title="CollectFlowAPI", 
    version="1.0.0",
    description="API per la gestione di pratiche, movimenti, email e SMS",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Root",
            "description": "Endpoint di base e informazioni API"
        },
        {
            "name": "Health",
            "description": "Endpoint per il monitoraggio dello stato dell'API"
        },
        {
            "name": "API Info",
            "description": "Informazioni sulle versioni API supportate"
        },
        {
            "name": "v1 - Pratiche",
            "description": "Operazioni per la gestione delle pratiche di recupero crediti"
        },
        {
            "name": "v1 - Movimenti", 
            "description": "Operazioni per il tracking dei movimenti delle pratiche"
        },
        {
            "name": "v1 - Email",
            "description": "Operazioni per la gestione delle comunicazioni email"
        },
        {
            "name": "v1 - SMS",
            "description": "Operazioni per la gestione delle comunicazioni SMS"
        }
    ]
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Configure for your frontend
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Add custom logging middleware
app.add_middleware(LoggingMiddleware)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions globally"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors globally"""
    logger.warning(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "status_code": 422,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions globally"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url)
        }
    )

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint che fornisce informazioni sull'API.
    
    Returns:
        dict: Informazioni sull'API e i link utili
    """
    return {
        "message": "CollectFlowAPI - API per la gestione di pratiche, movimenti, email e SMS",
        "version": "v1.0.0",
        "api_version": "v1",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "version_info": "/api/versions",
        "endpoints": {
            "pratiche": "/api/v1/pratiche",
            "movimenti": "/api/v1/movimenti", 
            "email": "/api/v1/email",
            "sms": "/api/v1/sms"
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint per verificare lo stato dell'API.
    
    Returns:
        dict: Stato dell'API e timestamp
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "CollectFlowAPI",
        "version": "1.0.0"
    }

# Version info endpoint
@app.get("/api/versions", tags=["API Info"])
async def get_versions():
    """
    Get information about all supported API versions.
    
    Returns:
        dict: Information about all API versions
    """
    return {
        "current_version": "v1",
        "supported_versions": ["v1"],
        "versions": {
            "v1": {
                "prefix": "/api/v1",
                "description": "CollectFlowAPI v1 - Initial release",
                "deprecated": False,
                "end_of_life": None,
                "features": {
                    "pratiche": True,
                    "movimenti": True,
                    "email": True,
                    "sms": True,
                    "status_update": True,
                }
            }
        }
    }



# Include routers with proper API versioning - Resource-based groups
app.include_router(pratiche_router,  prefix="/api/v1/pratiche")
app.include_router(movimenti_router, prefix="/api/v1/movimenti")
app.include_router(email_router,     prefix="/api/v1/email")
app.include_router(sms_router,       prefix="/api/v1/sms")

# Log successful startup
logger.info("CollectFlowAPI application started successfully")
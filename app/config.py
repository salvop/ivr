"""
Configuration Management
=======================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Environment variables and configuration management
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module handles all configuration settings including database connection,
API keys, and other environment-specific variables.
"""

import os
from dotenv import load_dotenv
from fastapi import HTTPException, status

load_dotenv()

# Database configuration
SQLSERVER_DSN = os.getenv("SQLSERVER_DSN")

# API Key configuration
API_KEYS_RAW = os.getenv("API_KEYS", "")
API_KEYS = [key.strip() for key in API_KEYS_RAW.split(",") if key.strip()] if API_KEYS_RAW else []
API_KEY_HEADER = "X-API-Key"

# Create global API key header instance
from fastapi.security.api_key import APIKeyHeader
api_key_header = APIKeyHeader(name=API_KEY_HEADER, auto_error=False)

# Database connection pool configuration
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))  # Default 10 connections

# Logging configuration
LOG_TO_STDOUT = os.getenv("LOG_TO_STDOUT", "true").lower() == "true"  # Default to stdout
LOG_PATH = os.getenv("LOG_PATH", "logs/app.log")  # Fallback file path
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")  # Default log level

def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided API key.
    
    Args:
        api_key: The API key to validate (can be None if header is missing)
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    # Production-safe logging
    import logging
    logger = logging.getLogger(__name__)
    logger.debug("API key validation requested")
    
    # Check if API key is missing first
    if not api_key:
        logger.warning("API key is missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required"
        )
    
    # Check environment for debug logging
    import os
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "development":
        logger.debug(f"Validating API key: '{api_key[:8]}...'")
        logger.debug(f"Configured API keys count: {len(API_KEYS)}")
    else:
        logger.debug("API key validation in production mode")
    
    if not API_KEYS:
        logger.error("No API keys configured in environment")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API keys not configured"
        )
    
    if api_key not in API_KEYS:
        logger.warning(f"Invalid API key provided: '{api_key}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    logger.info("API key validation successful")
    return True

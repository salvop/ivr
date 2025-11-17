"""
Custom Middleware
================

Author: Salvatore Privitera
Company: FIDES S.p.A.
Description: Custom logging middleware for request/response tracking
Version: 1.0.0
License: Proprietary - FIDES S.p.A.

This module provides custom middleware for logging all HTTP requests and responses,
including processing time and error handling.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

# Remove duplicate logging configuration - use the one from main.py
logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log request start
        start_time = time.time()
        
        # Get request details
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log request
        logger.info(f"Request: {method} {url} from {client_ip} - User-Agent: {user_agent}")
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(f"Response: {method} {url} - Status: {response.status_code} - Time: {process_time:.3f}s")
            
            # Add processing time to response headers
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log error
            process_time = time.time() - start_time
            logger.error(f"Error: {method} {url} - Exception: {str(e)} - Time: {process_time:.3f}s")
            raise

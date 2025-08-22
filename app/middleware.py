
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import json

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Log request details
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        
        # Skip health checks in production to reduce log noise
        if request.url.path == "/health":
            return await call_next(request)
        
        logger.info(f"Request: {request.method} {request.url.path} "
                   f"from {client_ip}")
        
        # Log query parameters
        if request.query_params:
            logger.debug(f"Query params: {dict(request.query_params)}")
        
        # Log body for non-GET requests
        if request.method not in ["GET", "HEAD"]:
            try:
                body = await request.body()
                if body:
                    # Truncate long bodies to prevent log flooding
                    body_str = body.decode()[:500] + "..." if len(body) > 500 else body.decode()
                    logger.debug(f"Request body: {body_str}")
            except Exception as e:
                logger.warning(f"Failed to read request body: {str(e)}")
        
        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            # Log exceptions with traceback
            logger.error(f"Request error: {str(e)}", exc_info=True)
            raise
        
        # Calculate processing time
        process_time = (time.time() - start_time) * 1000
        formatted_time = f"{process_time:.2f}ms"
        
        # Log response details
        logger.info(f"Response: {response.status_code} (Time: {formatted_time})")
        return response

# If you want to keep the function-based approach
def log_requests(app):
    """Add logging middleware to the application"""
    app.add_middleware(LoggingMiddleware)
    return app
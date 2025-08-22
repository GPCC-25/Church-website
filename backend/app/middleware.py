import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses"""
    
    async def dispatch(self, request: Request, call_next):
        # Log request details
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        
        logger.info(f"Request: {request.method} {request.url.path} "
                   f"from {client_ip}")
        
        # Log query parameters
        if request.query_params:
            logger.debug(f"Query params: {dict(request.query_params)}")
        
        # Log body for non-GET requests
        if request.method not in ["GET", "HEAD"]:
            body = await request.body()
            if body:
                # Truncate long bodies to prevent log flooding
                body_str = body.decode()[:500] + "..." if len(body) > 500 else body.decode()
                logger.debug(f"Request body: {body_str}")
        
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

def log_requests(app):
    """Add logging middleware to the application"""
    return LoggingMiddleware(app)
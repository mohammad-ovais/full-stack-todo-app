from fastapi import FastAPI
from fastapi.security import HTTPBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

def setup_security_headers(app: FastAPI):
    """
    Add security headers to the application
    """
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import Response
    from starlette.requests import Request

    class SecurityHeadersMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            response: Response = await call_next(request)

            # Add security headers
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
            response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none';"

            return response

    app.add_middleware(SecurityHeadersMiddleware)

def setup_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the application
    """
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address

    # Initialize limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Example: Limit auth endpoints to 10 requests per minute
    # @limiter.limit("10/minute")
    # def auth_endpoint(...):
    #     ...
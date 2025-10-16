from functools import wraps
from flask import request, jsonify
import time
from collections import defaultdict
from threading import Lock

class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if request is allowed
        
        Args:
            key: Unique identifier (usually IP address)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            
            # Remove old entries outside the time window
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if current_time - req_time < window_seconds
            ]
            
            # Check if limit exceeded
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Add current request
            self.requests[key].append(current_time)
            return True

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(max_requests: int = 10, window_seconds: int = 60):
    """
    Rate limiting decorator
    
    Args:
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use IP address as key
            key = request.remote_addr
            
            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                return jsonify({
                    'success': False,
                    'error': f'Rate limit exceeded. Maximum {max_requests} requests per {window_seconds} seconds.'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

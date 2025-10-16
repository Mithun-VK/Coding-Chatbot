import logging
from datetime import datetime
from flask import request


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger(__name__)


def log_request(req):
    """Log incoming API requests"""
    logger.info(f"""
    Request Details:
    - Method: {req.method}
    - Path: {req.path}
    - IP: {req.remote_addr}
    - User-Agent: {req.headers.get('User-Agent', 'Unknown')}
    - Timestamp: {datetime.now().isoformat()}
    """)


def format_response(data: dict, status_code: int = 200):
    """Format API response consistently"""
    response = {
        'timestamp': datetime.now().isoformat(),
        **data
    }
    return response, status_code


def sanitize_code(code: str) -> str:
    """Remove markdown code blocks if present"""
    # Remove ```
    code = code.strip()
    if code.startswith("```"):
        lines = code.split('\n')
        if lines[-1].strip() == "```":
            code = '\n'.join(lines[1:-1])
        else:
            code = '\n'.join(lines[1:])
    return code.strip()



def estimate_tokens(text: str) -> int:
    """Rough estimate of token count"""
    # Approximation: 1 token ≈ 4 characters
    return len(text) // 4

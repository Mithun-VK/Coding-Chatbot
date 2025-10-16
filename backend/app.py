import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path of the backend directory
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / '.env'

# Load environment variables with absolute path
load_dotenv(dotenv_path=ENV_PATH)

# Verify critical environment variables
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("\n" + "="*60)
    print("❌ ERROR: GEMINI_API_KEY not found in environment!")
    print("="*60)
    print(f"\nEnvironment file path: {ENV_PATH}")
    print(f"File exists: {ENV_PATH.exists()}")
    if ENV_PATH.exists():
        print("\n.env file contents:")
        print(ENV_PATH.read_text())
    print("\nGet your API key from: https://aistudio.google.com/apikey")
    print("="*60 + "\n")
    sys.exit(1)

print(f"✓ Environment loaded from: {ENV_PATH}")
print(f"✓ API Key found (first 10 chars): {api_key[:10]}...")

# Now import everything else
from flask import Flask, jsonify
from flask_cors import CORS
from routes.api import api_blueprint
from utils.config import Config
import logging

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


def create_app(config_class=Config):
    """
    Application factory pattern for Flask
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Log application startup
    logger.info("Starting Coding Chatbot API...")
    logger.info(f"Environment: {os.getenv('FLASK_ENV', 'production')}")
    logger.info(f"Model: {os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
    
    # Enable CORS for frontend communication
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    CORS(app, resources={
        r"/api/*": {
            "origins": [frontend_url, "http://localhost:3000"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    logger.info(f"CORS enabled for: {frontend_url}")
    
    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    logger.info("API routes registered")
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'service': 'Coding Chatbot API',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': '/health',
                'api': '/api',
                'generate': '/api/generate',
                'chat': '/api/chat',
                'explain': '/api/explain',
                'improve': '/api/improve',
                'models': '/api/models'
            }
        }), 200
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'coding-chatbot-api'
        }), 200
    
    # Error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'success': False, 'error': 'Bad request', 'message': str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'error': 'Resource not found'}), 404
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({'success': False, 'error': 'Rate limit exceeded'}), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify({'success': False, 'error': 'Internal server error'}), 500
    
    return app


if __name__ == '__main__':
    # Create app instance
    app = create_app()
    
    # Get configuration
    port = int(os.getenv('PORT', 5000))
    host = '0.0.0.0'
    debug = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Display startup banner
    print("\n" + "="*60)
    print("🚀 CODING CHATBOT API")
    print("="*60)
    print(f"Server:      http://localhost:{port}")
    print(f"Health:      http://localhost:{port}/health")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Model:       {os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')}")
    print("="*60)
    print("\n✨ Server is ready to accept requests!")
    print("Press CTRL+C to stop\n")
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Server shutting down...")
    except Exception as e:
        logger.error(f"Failed to start: {e}", exc_info=True)
        sys.exit(1)

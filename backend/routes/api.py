import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env with absolute path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

from flask import Blueprint, request, jsonify
from services.gemini_service import GeminiService
from utils.validators import validate_prompt
from utils.rate_limiter import rate_limit
from utils.helpers import format_response, log_request
import time
api_blueprint = Blueprint('api', __name__)
gemini_service = GeminiService()

@api_blueprint.route('/generate', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=60)  # 10 requests per minute
def generate_code():
    """
    Generate code based on user prompt
    
    Request Body:
        {
            "prompt": "string",
            "language": "string (optional)",
            "temperature": "float (optional, 0.0-1.0)"
        }
    
    Response:
        {
            "success": bool,
            "code": "string",
            "language": "string",
            "execution_time": float
        }
    """
    try:
        start_time = time.time()
        
        # Log incoming request
        log_request(request)
        
        # Validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        prompt = data.get('prompt', '').strip()
        language = data.get('language', 'auto')
        temperature = float(data.get('temperature', 0.2))
        
        # Validate inputs
        validation_error = validate_prompt(prompt, temperature)
        if validation_error:
            return jsonify({
                'success': False,
                'error': validation_error
            }), 400
        
        # Generate code using Gemini API
        result = gemini_service.generate_code(
            prompt=prompt,
            language=language,
            temperature=temperature
        )
        
        execution_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'code': result['code'],
            'language': result['language'],
            'execution_time': round(execution_time, 2)
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': f'Invalid input: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Code generation failed: {str(e)}'
        }), 500


@api_blueprint.route('/chat', methods=['POST'])
@rate_limit(max_requests=15, window_seconds=60)
def chat():
    """
    Multi-turn conversation endpoint with chat history
    
    Request Body:
        {
            "message": "string",
            "history": [{"role": "user"|"model", "content": "string"}],
            "language": "string (optional)"
        }
    """
    try:
        start_time = time.time()
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        message = data.get('message', '').strip()
        history = data.get('history', [])
        language = data.get('language', 'auto')
        
        if not message:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Continue conversation
        result = gemini_service.continue_chat(
            message=message,
            history=history,
            language=language
        )
        
        execution_time = time.time() - start_time
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'history': result['history'],
            'execution_time': round(execution_time, 2)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Chat failed: {str(e)}'
        }), 500


@api_blueprint.route('/explain', methods=['POST'])
@rate_limit(max_requests=10, window_seconds=60)
def explain_code():
    """
    Explain existing code
    
    Request Body:
        {
            "code": "string",
            "language": "string (optional)"
        }
    """
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'auto')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code cannot be empty'
            }), 400
        
        explanation = gemini_service.explain_code(code, language)
        
        return jsonify({
            'success': True,
            'explanation': explanation
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Explanation failed: {str(e)}'
        }), 500


@api_blueprint.route('/improve', methods=['POST'])
@rate_limit(max_requests=8, window_seconds=60)
def improve_code():
    """
    Improve and optimize existing code
    
    Request Body:
        {
            "code": "string",
            "language": "string (optional)",
            "focus": "string (optional: performance|readability|security)"
        }
    """
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'auto')
        focus = data.get('focus', 'general')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Code cannot be empty'
            }), 400
        
        result = gemini_service.improve_code(code, language, focus)
        
        return jsonify({
            'success': True,
            'improved_code': result['improved_code'],
            'suggestions': result['suggestions']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Code improvement failed: {str(e)}'
        }), 500


@api_blueprint.route('/models', methods=['GET'])
def get_available_models():
    """Get list of available Gemini models"""
    try:
        models = gemini_service.list_models()
        return jsonify({
            'success': True,
            'models': models
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

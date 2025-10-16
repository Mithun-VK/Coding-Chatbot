
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env with absolute path
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env')

import google.generativeai as genai
import time
from typing import Dict, List, Optional


class GeminiService:
    """Service class for Gemini API interactions"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        if not api_key.strip():
            raise ValueError("GEMINI_API_KEY is empty")
        
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        self.max_output_tokens = int(os.getenv('MAX_OUTPUT_TOKENS', 4096))
        
        print(f"[GeminiService] Initialized with model: {self.model_name}")
    
    def _retry_with_backoff(self, func, max_retries=3):
        """Simple retry logic with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                wait_time = (2 ** attempt)
                print(f"[GeminiService] Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
    
    def generate_code(
        self, 
        prompt: str, 
        language: str = 'auto',
        temperature: float = 0.2
    ) -> Dict[str, str]:
        """Generate code based on user prompt"""
        try:
            formatted_prompt = f"""You are an expert software engineer. Generate high-quality, production-ready code for:

{prompt}

{"Programming language: " + language if language != 'auto' else ""}

Requirements:
- Write clean, well-structured code
- Include helpful comments
- Follow best practices and coding standards
- Add proper error handling where appropriate
- Make the code maintainable and readable

Provide ONLY the code with inline comments. Do not include explanations outside the code."""

            def generate():
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(
                    formatted_prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=temperature,
                        max_output_tokens=self.max_output_tokens,
                        top_p=0.95,
                        top_k=40
                    )
                )
                return response.text.strip()
            
            code = self._retry_with_backoff(generate)
            detected_language = language if language != 'auto' else self._detect_language(code)
            
            return {
                'code': code,
                'language': detected_language
            }
            
        except Exception as e:
            error_msg = str(e)
            if '429' in error_msg:
                raise Exception("Rate limit exceeded. Please try again in a moment.")
            elif '400' in error_msg:
                raise Exception("Invalid request. Please check your prompt.")
            else:
                raise Exception(f"Code generation error: {error_msg}")
    
    def continue_chat(
        self,
        message: str,
        history: List[Dict[str, str]],
        language: str = 'auto'
    ) -> Dict:
        """Continue multi-turn conversation"""
        try:
            system_instruction = f"""You are an expert coding assistant. Help users with:
- Writing clean, efficient code
- Debugging and fixing errors
- Explaining programming concepts
- Code optimization and best practices

{'Prefer ' + language + ' when generating code.' if language != 'auto' else ''}

Be concise but thorough. Provide code examples when helpful."""

            model = genai.GenerativeModel(
                self.model_name,
                system_instruction=system_instruction
            )
            
            chat = model.start_chat(history=[])
            
            def send():
                return chat.send_message(message)
            
            response = self._retry_with_backoff(send)
            
            updated_history = history + [
                {'role': 'user', 'content': message},
                {'role': 'model', 'content': response.text}
            ]
            
            return {
                'response': response.text,
                'history': updated_history
            }
            
        except Exception as e:
            raise Exception(f"Chat error: {str(e)}")
    
    def explain_code(self, code: str, language: str = 'auto') -> str:
        """Explain existing code"""
        try:
            prompt = f"""Analyze and explain the following code in detail:


Provide:
1. High-level overview of what the code does
2. Step-by-step explanation of the logic
3. Any potential issues or improvements
4. Time/space complexity if applicable

Keep explanations clear and beginner-friendly."""

            def generate():
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.3,
                        max_output_tokens=2048
                    )
                )
                return response.text
            
            return self._retry_with_backoff(generate)
            
        except Exception as e:
            raise Exception(f"Code explanation error: {str(e)}")
    
    def improve_code(
        self,
        code: str,
        language: str = 'auto',
        focus: str = 'general'
    ) -> Dict[str, str]:
        """Improve and optimize existing code"""
        try:
            focus_instructions = {
                'performance': 'Focus on performance optimization and efficiency',
                'readability': 'Focus on code readability and maintainability',
                'security': 'Focus on security best practices and vulnerability fixes',
                'general': 'Provide overall improvements across all aspects'
            }
            
            prompt = f"""Improve the following code:



{focus_instructions.get(focus, focus_instructions['general'])}

Provide:
1. The improved version of the code
2. List of specific changes made and why
3. Best practices applied

Format:
IMPROVED CODE:
[improved code here]

CHANGES:
[list of improvements]"""

            def generate():
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        temperature=0.2,
                        max_output_tokens=3072
                    )
                )
                return response.text
            
            full_response = self._retry_with_backoff(generate)
            
            # Parse response
            parts = full_response.split('CHANGES:', 1)
            improved_code = parts[0].replace('IMPROVED CODE:', '').strip()
            suggestions = parts[1].strip() if len(parts) > 1 else 'See improved code above'
            
            return {
                'improved_code': improved_code,
                'suggestions': suggestions
            }
            
        except Exception as e:
            raise Exception(f"Code improvement error: {str(e)}")
    
    def _detect_language(self, code: str) -> str:
        """Simple language detection based on code patterns"""
        code_lower = code.lower()
        
        patterns = {
            'python': ['def ', 'import ', 'print(', 'class ', '__init__'],
            'javascript': ['const ', 'let ', 'function ', '=>', 'console.log'],
            'typescript': [': string', ': number', 'interface ', 'type '],
            'java': ['public class', 'public static', 'void main', 'System.out'],
            'cpp': ['#include', 'std::', 'cout', 'int main'],
            'c': ['#include', 'printf', 'int main', 'void '],
            'go': ['package main', 'func main', 'fmt.Print'],
            'rust': ['fn main', 'let mut', 'println!'],
            'php': ['<?php', 'function ', '$'],
            'ruby': ['def ', 'end', 'puts '],
        }
        
        for lang, keywords in patterns.items():
            if any(keyword in code_lower for keyword in keywords):
                return lang
        
        return 'text'
    
    def list_models(self) -> List[str]:
        """List available Gemini models"""
        try:
            models = genai.list_models()
            return [model.name for model in models if 'gemini' in model.name.lower()]
        except Exception:
            return [self.model_name]

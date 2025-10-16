import re

def validate_prompt(prompt: str, temperature: float) -> str:
    """
    Validate user input
    
    Args:
        prompt: User's code generation prompt
        temperature: Model temperature
    
    Returns:
        Error message if validation fails, None otherwise
    """
    if not prompt:
        return "Prompt cannot be empty"
    
    if len(prompt) < 5:
        return "Prompt is too short. Please provide more details."
    
    if len(prompt) > 5000:
        return "Prompt is too long. Maximum 5000 characters allowed."
    
    if temperature < 0.0 or temperature > 1.0:
        return "Temperature must be between 0.0 and 1.0"
    
    # Check for potentially malicious patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'on\w+\s*=',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            return "Invalid characters detected in prompt"
    
    return None


def validate_code(code: str) -> str:
    """Validate code input"""
    if not code:
        return "Code cannot be empty"
    
    if len(code) > 10000:
        return "Code is too long. Maximum 10000 characters allowed."
    
    return None

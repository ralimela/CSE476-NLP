import os, re
import requests

API_KEY  = os.getenv("OPENAI_API_KEY", "cse476")
API_BASE = os.getenv("API_BASE", "http://10.4.58.53:41701/v1")  
MODEL    = os.getenv("MODEL_NAME", "bens_model")              

def call_model(prompt, system="You are a helpful assistant.", temperature=0.0, max_tokens=256):
    """
    Calls the LLM API with customizable system message.
    Returns the text response or empty string on failure.
    """
    url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            print(f"API Error: {resp.status_code}")
            return ""
    except Exception as e:
        print(f"Request failed: {e}")
        return ""


def extract_final_answer(text, domain="math"):
    """
    Attempts to pull out the final answer depending on the domain.
    I added separate cases because each task type formats answers differently.
    """
    text = text.strip()
    
    if domain == "math":
        # Here it looks for \boxed{} format
        boxed = re.findall(r'\\boxed\{([^}]+)\}', text)
        if boxed:
            return boxed[-1].strip()
        
        # Here it looks for "answer is X" pattern
        answer_pattern = re.search(r'answer is[:\s]*(-?\d+)', text, re.IGNORECASE)
        if answer_pattern:
            return answer_pattern.group(1)
        
        numbers = re.findall(r'-?\d+', text)
        if numbers:
            return numbers[-1]
        
        return text
    
    elif domain == "coding":
        # Looks for code block first
        code_match = re.search(r'```python\n(.*?)```', text, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        return text
    
    elif domain == "planning":
        # Extract lines that look like actions
        lines = text.strip().split('\n')
        actions = [l.strip() for l in lines if l.strip().startswith('(')]
        if actions:
            return '\n'.join(actions)
        return text
    
    elif domain == "common_sense":
        # Takes the last non-empty line as the answer
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        return lines[-1] if lines else text
    
    elif domain == "future_prediction":
        # Looks for boxed format first
        boxed = re.findall(r'\\boxed\{([^}]+)\}', text)
        if boxed:
            return boxed[-1].strip()
        return text
    
    return text
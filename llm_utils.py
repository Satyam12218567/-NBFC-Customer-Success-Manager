import os
import re
from datetime import datetime, timedelta
import streamlit as st

def extract_tasks_fallback(text):
    """Rule-based fallback for task extraction."""
    tasks = []
    
    # Split by periods or newlines
    lines = re.split(r'[.\n]', text)
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue
            
        lower_line = line.lower()
        
        # Check for complaints/bugs
        if any(word in lower_line for word in ['bug', 'issue', 'error', 'broken', 'fail', 'complained', 'delay', 'down', 'fix']):
            tasks.append({
                "title": f"Investigate: {line[:50]}...",
                "category": "Bug" if any(w in lower_line for w in ['bug', 'error', 'broken', 'down']) else "Complaint",
                "priority": "High",
                "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            })
            
        # Check for feature requests
        elif any(word in lower_line for word in ['feature', 'request', 'want', 'need', 'add', 'build', 'module', 'quote']):
            tasks.append({
                "title": f"Feature/Proposal: {line[:50]}...",
                "category": "Proposal" if 'quote' in lower_line else "Feature Request",
                "priority": "Medium",
                "due_date": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
            })
            
        # Check for training/support
        elif any(word in lower_line for word in ['train', 'help', 'support', 'how to', 'question']):
            tasks.append({
                "title": f"Support/Training: {line[:50]}...",
                "category": "Training" if 'train' in lower_line else "Support",
                "priority": "Medium",
                "due_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
            })
            
    # Fallback: if no keywords matched but they typed a decent amount of text, create a generic review task
    if not tasks and len(text.strip()) > 15:
        tasks.append({
            "title": f"Review Item: {text[:40].strip()}...",
            "category": "Support",
            "priority": "Low",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        })
            
    return tasks

def generate_tasks_from_text(text):
    """
    Attempts to use Gemini API to extract tasks. 
    Falls back to rule-based extraction if API key is missing or call fails.
    """
    api_key = None
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
        
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY")

    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Analyze the following meeting notes or email text and extract actionable tasks.
            For each task, provide:
            - title: A short, descriptive title.
            - category: Must be one of [Bug, Feature Request, Complaint, Proposal, Training, Support]
            - priority: Must be one of [High, Medium, Low]
            - due_date: YYYY-MM-DD format (assume today is {datetime.now().strftime('%Y-%m-%d')})
            
            Return the output strictly as a JSON list of objects, without any markdown formatting block, like this:
            [
              {{"title": "...", "category": "...", "priority": "...", "due_date": "..."}}
            ]
            
            Text:
            {text}
            """
            
            response = model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean up potential markdown formatting
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
                
            import json
            tasks = json.loads(response_text)
            return tasks
            
        except Exception as e:
            print(f"Gemini API failed: {e}. Falling back to rule-based.")
            return extract_tasks_fallback(text)
    else:
        return extract_tasks_fallback(text)

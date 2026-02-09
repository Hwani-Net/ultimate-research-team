
import os
import re
from crewai import LLM

def run_critique(css_snippet):
    # Fixed model for review
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "Error: Missing ANTHROPIC_API_KEY for review."
        
    model = LLM(model="anthropic/claude-3-5-sonnet-20241022", api_key=api_key)
    
    prompt = f"""
    [ROLE: HIGH-AESTHETIC UI/UX DESIGNER (CLAUDE 4.6)]
    
    Review the following CSS/UI logic for a premium AI Research platform. 
    The target audience is MBB-level strategy consultants and VC investors.
    
    [CSS EXCERPT]:
    {css_snippet[:3000]}
    
    [CRITERIA]
    1. Professionalism: Is it too 'gamer-like' or 'toy-like'? (Reject if so)
    2. Readability: High-contrast but low eye-strain.
    3. WOW Factor: Does it feel like a futuristic, expensive tool?
    
    [YOUR TASK]
    - Provide a concise critique.
    - If you approve, end your response with 'DESIGN APPROVED'.
    - If not, provide specific CSS fixes.
    """
    
    response = model.call([{"role": "user", "content": prompt}])
    return response

if __name__ == "__main__":
    from pathlib import Path
    app_path = Path("app.py")
    if app_path.exists():
        content = app_path.read_text(encoding="utf-8")
        # Extract <style> blocks
        css_blocks = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
        full_css = "\n".join(css_blocks)
        
        print("🎨 Analyzing UI Architecture...")
        feedback = run_critique(full_css)
        print("\n=== DESIGNER FEEDBACK ===")
        print(feedback)

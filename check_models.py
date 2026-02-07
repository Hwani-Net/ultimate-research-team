import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("=" * 60)
print("📋 Available Gemini Models (Google AI Studio)")
print("=" * 60)

# List all available models
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Display Name: {model.display_name}")
        print(f"   Description: {model.description[:100]}...")
        print()

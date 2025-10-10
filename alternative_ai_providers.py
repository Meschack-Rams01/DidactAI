#!/usr/bin/env python
"""
Alternative AI providers configuration
"""

ALTERNATIVE_PROVIDERS = {
    "huggingface": {
        "name": "Hugging Face Transformers",
        "cost": "Free",
        "setup_time": "2 minutes",
        "api_key_required": False,
        "description": "Run AI models locally - no internet quota limits",
        "pros": ["Unlimited usage", "Works offline", "Fast setup"],
        "cons": ["Requires more CPU/RAM", "Slightly lower quality"]
    },
    
    "openai_free": {
        "name": "OpenAI Free Tier", 
        "cost": "Free $5 credit",
        "setup_time": "1 minute",
        "api_key_required": True,
        "description": "OpenAI ChatGPT API with free credits",
        "pros": ["High quality", "Fast", "$5 free credit"],
        "cons": ["Requires phone verification", "Credit expires"]
    },
    
    "anthropic": {
        "name": "Anthropic Claude",
        "cost": "Free $5 credit",
        "setup_time": "1 minute", 
        "api_key_required": True,
        "description": "Claude AI with generous free tier",
        "pros": ["Excellent quality", "Large context", "Free credits"],
        "cons": ["Requires signup", "US/UK primarily"]
    },
    
    "ollama": {
        "name": "Ollama (Local AI)",
        "cost": "Free",
        "setup_time": "5 minutes",
        "api_key_required": False,
        "description": "Run AI models completely offline on your computer",
        "pros": ["100% free", "Unlimited usage", "Privacy", "No internet required"],
        "cons": ["Initial download ~4GB", "Requires decent hardware"]
    }
}

print("🤖 ALTERNATIVE AI PROVIDERS (When Gemini quota is full):\n")

for key, provider in ALTERNATIVE_PROVIDERS.items():
    print(f"ðŸ“Š {provider['name']}")
    print(f"   ðŸ’° Cost: {provider['cost']}")
    print(f"     Setup: {provider['setup_time']}")
    print(f"   ðŸ”‘ API Key: {'Required' if provider['api_key_required'] else 'Not required'}")
    print(f"   ðŸ“ {provider['description']}")
    print(f"   ✅ Pros: {', '.join(provider['pros'])}")
    print(f"   ⚠ Cons: {', '.join(provider['cons'])}")
    print()

print("""
🚀 QUICKEST SOLUTION FOR TODAY:

OPTION A: New Google Project (2 minutes)
1. Open: https://console.cloud.google.com/
2. Click "Select a project" ←’ "New Project" 
3. Name it "DidactAI-2" ←’ Create
4. Enable "Generative AI API"
5. Create API key ←’ Copy it
6. Replace GEMINI_API_KEY in your settings

OPTION B: Ollama (Local AI - 5 minutes)
1. Download: https://ollama.ai/
2. Install Ollama
3. Run: ollama pull llama3.2:3b
4. Modify your Django settings to use local AI

OPTION C: Enhanced Fallback (0 minutes)
Make the fallback system even better with more realistic questions

Which option would you like me to implement?
""")

# Check current settings
import os
import sys
sys.path.append('.')

try:
    from DidactAI import settings
    if hasattr(settings, 'GEMINI_API_KEY'):
        print(f"ðŸ“„ Current Gemini key found: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-4:]}")
    else:
        print("⚠No GEMINI_API_KEY found in settings")
except:
    print("⚠Could not load Django settings")

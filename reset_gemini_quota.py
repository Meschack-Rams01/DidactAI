#!/usr/bin/env python
"""
Guide to reset Google Gemini API quota
"""

print("""
🔧 METHODS TO RESET GOOGLE GEMINI API QUOTA:

METHOD 1: Create New Google Cloud Project (Recommended)
1. Go to: https://console.cloud.google.com/
2. Create a NEW Google Cloud Project
3. Enable the Generative AI API for the new project
4. Create a NEW API key in the new project
5. Update your .env file with the new GEMINI_API_KEY

METHOD 2: Use Different Google Account
1. Create a new Google account
2. Set up Google Cloud Console with new account  
3. Create project and enable Generative AI API
4. Generate new API key
5. Update GEMINI_API_KEY in .env

METHOD 3: Wait for Reset (24 hours)
- Quota resets every 24 hours
- Current time: Check Google Console for exact reset time

METHOD 4: Upgrade to Paid Tier (Instant)
- Go to Google Cloud Console
- Enable billing for your project
- Quota increases significantly with paid tier

🎯 QUICKEST SOLUTION: Method 1 (New Project)
This will give you a fresh 50 requests/day quota immediately.
""")

# Show current API key (masked for security)
import os
from pathlib import Path

env_file = Path('.env')
if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
        for line in content.split('\n'):
            if 'GEMINI_API_KEY' in line and '=' in line:
                key = line.split('=')[1].strip()
                masked_key = key[:10] + '*' * (len(key) - 20) + key[-10:] if len(key) > 20 else '*' * len(key)
                print(f"\n📄 Current API Key: {masked_key}")
                break
    print("\n💡 After getting new key, update it in the .env file above.")
else:
    print("\n⚠️  No .env file found. Create one with GEMINI_API_KEY=your_new_key")
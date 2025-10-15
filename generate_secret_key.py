#!/usr/bin/env python3
"""
Generate a secure Django SECRET_KEY
"""

import secrets
import string

def generate_django_secret_key(length=50):
    """Generate a secure Django SECRET_KEY"""
    
    # Characters allowed in Django SECRET_KEY
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Generate random secret key
    secret_key = ''.join(secrets.choice(chars) for _ in range(length))
    
    return secret_key

if __name__ == '__main__':
    print("🔐 Generating Django SECRET_KEY...")
    secret_key = generate_django_secret_key()
    
    print(f"\n✅ Your Django SECRET_KEY:")
    print(f"SECRET_KEY={secret_key}")
    
    print(f"\n📝 Add this to your Render environment variables:")
    print(f"Key: SECRET_KEY")
    print(f"Value: {secret_key}")
    
    print(f"\n⚠️  IMPORTANT: Keep this secret key secure and never share it publicly!")
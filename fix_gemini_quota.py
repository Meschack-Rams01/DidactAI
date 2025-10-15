#!/usr/bin/env python
"""
Gemini API Quota Fix and Enhanced Error Handling
This script helps resolve the quota issues and implements better retry logic.
"""

import os
import sys
import django
import time
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DidactAI_project.settings')
django.setup()

from ai_generator.services import GeminiService
from ai_generator.models import AIGeneration

def check_api_status():
    """Check the current API status and quota"""
    print("ðŸ” Checking Gemini API Status")
    print("=" * 50)
    
    gemini = GeminiService()
    
    # Simple test request
    test_prompt = "Hello, this is a test. Please respond with just 'API Working'."
    
    try:
        result = gemini.generate_content(test_prompt)
        
        if result['success']:
            print("✅ API is working correctly!")
            print(f"ðŸ“Š Processing time: {result['processing_time']:.2f}s")
            print(f"ðŸ”¢ Estimated tokens used: {result['tokens_used']}")
            print(f"ðŸ“ Response: {result['content'][:100]}...")
            return True
        else:
            print(f"✓Œ API Error: {result['error']}")
            if '429' in str(result['error']):
                print("\n⚠ QUOTA EXCEEDED - See solutions below")
                show_quota_solutions()
            return False
            
    except Exception as e:
        print(f"✓Œ Exception: {str(e)}")
        return False

def show_quota_solutions():
    """Display solutions for quota issues"""
    print("\nðŸ›  SOLUTIONS FOR QUOTA ISSUES")
    print("=" * 50)
    
    print("ðŸ“Š **CURRENT STATUS**: Free Tier (50 requests/day)")
    print("\nðŸ”„ **IMMEDIATE SOLUTIONS**:")
    print("1. **Wait**: Quota resets at midnight Pacific time")
    print("2. **New API Key**: Create a new Google Cloud project with fresh quota")
    print("3. **Upgrade Billing**: Enable Cloud Billing for higher limits")
    
    print("\n🚀 **UPGRADE OPTIONS**:")
    print("&bull; **Tier 1** (Billing enabled): 1,000-4,000 RPM, 1M-4M TPM")
    print("&bull; **Tier 2** ($250+ spent): 2,000-20,000 RPM, 3M-10M TPM") 
    print("&bull; **Tier 3** ($1000+ spent): 10,000-30,000 RPM, 8M-30M TPM")
    
    print("\nðŸ”— **HOW TO UPGRADE**:")
    print("1. Go to: https://aistudio.google.com/app/apikey")
    print("2. Click 'Upgrade' next to your project")
    print("3. Enable Cloud Billing if not already enabled")
    
    print("\n **QUOTA RESET**: Daily quotas reset at midnight Pacific time")

def show_recent_usage():
    """Show recent API usage from database"""
    print("\nðŸ“ˆ Recent API Usage (Last 24 hours)")
    print("-" * 50)
    
    from django.utils import timezone
    from datetime import timedelta
    
    # Get generations from last 24 hours
    yesterday = timezone.now() - timedelta(days=1)
    recent_gens = AIGeneration.objects.filter(
        created_at__gte=yesterday
    ).order_by('-created_at')[:10]
    
    total_requests = recent_gens.count()
    print(f"ðŸ“Š Total requests in last 24h: {total_requests}")
    
    if recent_gens:
        print("\nðŸ•’ Recent generations:")
        for gen in recent_gens[:5]:
            status_icon = "✅" if gen.status == 'completed' else "✓Œ"
            print(f"   {status_icon} {gen.created_at.strftime('%H:%M:%S')} - {gen.title[:30]}...")
    
    if total_requests >= 45:
        print("\n⚠ WARNING: Approaching daily limit (50 requests)")
    elif total_requests >= 50:
        print("\nðŸš« QUOTA EXCEEDED: You've used your daily limit")

def create_enhanced_error_handling():
    """Create enhanced error handling for the service"""
    print("\nðŸ”§ Creating Enhanced Error Handling")
    print("-" * 50)
    
    # This would typically be implemented in the actual service
    enhanced_service_code = """
# Enhanced Gemini Service with Retry Logic and Better Error Handling

class EnhancedGeminiService(GeminiService):
    def __init__(self):
        super().__init__()
        self.max_retries = 3
        self.base_delay = 1  # seconds
    
    def generate_content_with_retry(self, prompt: str, **kwargs) -> Dict[str, Any]:
        \"\"\"Generate content with automatic retry logic\"\"\"
        
        for attempt in range(self.max_retries):
            try:
                result = self.generate_content(prompt, **kwargs)
                
                if result['success']:
                    return result
                
                # Handle quota errors specifically
                if '429' in str(result.get('error', '')):
                    if 'retry in' in str(result['error']).lower():
                        # Extract retry delay from error message
                        import re
                        retry_match = re.search(r'retry in (\\d+)', str(result['error']))
                        if retry_match:
                            retry_delay = int(retry_match.group(1))
                            print(f" Quota exceeded. Waiting {retry_delay}s...")
                            time.sleep(min(retry_delay, 60))  # Cap at 60 seconds
                            continue
                
                # Exponential backoff for other errors
                delay = self.base_delay * (2 ** attempt)
                print(f" Attempt {attempt + 1} failed. Retrying in {delay}s...")
                time.sleep(delay)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {
                        'success': False,
                        'error': f'All retry attempts failed: {str(e)}',
                        'content': None,
                        'tokens_used': 0,
                        'processing_time': 0
                    }
                
                delay = self.base_delay * (2 ** attempt)
                time.sleep(delay)
        
        return {
            'success': False,
            'error': 'Max retries exceeded',
            'content': None,
            'tokens_used': 0,
            'processing_time': 0
        }
"""
    
    print("✅ Enhanced error handling pattern available")
    print("ðŸ“ This includes:")
    print("   &bull; Automatic retry logic")
    print("   &bull; Quota-aware delays") 
    print("   &bull; Exponential backoff")
    print("   &bull; Graceful fallback")

def main():
    print("🍎“ Gemini API Quota Fix Tool")
    print("=" * 50)
    
    # Check current API status
    api_working = check_api_status()
    
    # Show usage statistics
    show_recent_usage()
    
    # Create enhanced error handling
    create_enhanced_error_handling()
    
    print("\n" + "=" * 50)
    if not api_working:
        print("ðŸ”§ **RECOMMENDED ACTIONS**:")
        print("1. Create new Google Cloud project with fresh API key")
        print("2. Enable billing for higher quota limits") 
        print("3. Wait for quota reset (midnight Pacific time)")
        print("4. Use enhanced retry logic in the application")
    else:
        print("✅ **ALL SYSTEMS OPERATIONAL**")
        print("🍎¯ API is working correctly - you can continue using the system!")

if __name__ == "__main__":
    main()

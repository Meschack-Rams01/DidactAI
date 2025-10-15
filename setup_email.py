#!/usr/bin/env python
"""
DidactAI Email Setup Helper

This script helps configure email settings for password reset functionality.
"""

import os
from decouple import config

def setup_email_configuration():
    """Guide user through email setup process"""
    
    print("ðŸ”§ DidactAI Email Configuration Setup")
    print("=" * 50)
    print()
    
    print("ðŸ“§ To enable password reset emails, you need to configure an SMTP server.")
    print("   The easiest option is Gmail with App Passwords.")
    print()
    
    print("ðŸ“ Gmail Setup Instructions:")
    print("1. Go to your Google Account settings (myaccount.google.com)")
    print("2. Security ←’ 2-Step Verification (must be enabled)")
    print("3. Security ←’ App passwords")
    print("4. Generate an app password for 'DidactAI'")
    print("5. Copy the 16-character password")
    print()
    
    # Check current configuration
    current_backend = config('EMAIL_BACKEND', default='console')
    print(f"Current EMAIL_BACKEND: {current_backend}")
    
    if 'console' in current_backend:
        print("⚠ Currently using console backend (emails will only show in terminal)")
        print()
        
        choice = input("Would you like to set up Gmail SMTP? (y/n): ").lower().strip()
        
        if choice == 'y':
            print("\nðŸ“ Please update your .env file with these settings:")
            print("=" * 50)
            print("EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
            print("EMAIL_HOST=smtp.gmail.com")
            print("EMAIL_PORT=587")
            print("EMAIL_USE_TLS=True")
            print("EMAIL_HOST_USER=your-gmail@gmail.com")
            print("EMAIL_HOST_PASSWORD=your-16-char-app-password")
            print("DEFAULT_FROM_EMAIL=DidactAI <noreply@DidactAI.com>")
            print()
            
            email = input("Enter your Gmail address: ").strip()
            password = input("Enter your Gmail app password: ").strip()
            
            if email and password:
                print(f"\n✅ Configuration for {email}")
                print("Copy these lines to your .env file:")
                print(f"EMAIL_HOST_USER={email}")
                print(f"EMAIL_HOST_PASSWORD={password}")
                print()
                
                # Test email configuration
                test_choice = input("Test email configuration now? (y/n): ").lower().strip()
                if test_choice == 'y':
                    test_email_configuration(email, password)
            
        else:
            print("ðŸ“§ For development, you can use console backend to see emails in terminal.")
    else:
        print("✅ SMTP backend configured")
        test_choice = input("Test current email configuration? (y/n): ").lower().strip()
        if test_choice == 'y':
            email_user = config('EMAIL_HOST_USER', default='')
            email_pass = config('EMAIL_HOST_PASSWORD', default='')
            if email_user and email_pass:
                test_email_configuration(email_user, email_pass)
            else:
                print("✓Œ EMAIL_HOST_USER or EMAIL_HOST_PASSWORD not configured")

def test_email_configuration(email_user, email_pass):
    """Test email configuration"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        print(f"\n🐧ª Testing SMTP connection to {email_user}...")
        
        # Test SMTP connection
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        
        # Send test email
        test_email = input("Enter email address to send test email: ").strip()
        if test_email:
            msg = MIMEText("This is a test email from DidactAI setup script.")
            msg['Subject'] = 'DidactAI Email Test'
            msg['From'] = email_user
            msg['To'] = test_email
            
            server.send_message(msg)
            print(f"✅ Test email sent successfully to {test_email}")
        
        server.quit()
        
    except Exception as e:
        print(f"✓Œ Email test failed: {str(e)}")
        print("\nCommon issues:")
        print("- Make sure 2-Factor Authentication is enabled on Gmail")
        print("- Use App Password, not your regular Gmail password")
        print("- Check if 'Less secure app access' is enabled (if not using 2FA)")

def show_alternative_options():
    """Show alternative email providers"""
    print("\nðŸ“§ Alternative Email Providers:")
    print("=" * 40)
    print()
    
    print("ðŸ”¹ Outlook/Hotmail:")
    print("EMAIL_HOST=smtp-mail.outlook.com")
    print("EMAIL_PORT=587")
    print()
    
    print("ðŸ”¹ Yahoo Mail:")
    print("EMAIL_HOST=smtp.mail.yahoo.com")
    print("EMAIL_PORT=587")
    print()
    
    print("ðŸ”¹ Custom SMTP:")
    print("EMAIL_HOST=your-smtp-server.com")
    print("EMAIL_PORT=587 (or 465 for SSL)")
    print()

if __name__ == "__main__":
    try:
        setup_email_configuration()
        
        alt_choice = input("\nShow alternative email providers? (y/n): ").lower().strip()
        if alt_choice == 'y':
            show_alternative_options()
            
        print("\n🎉 Email setup guide completed!")
        print("ðŸ’¡ Remember to restart your Django server after updating .env")
        
    except KeyboardInterrupt:
        print("\n\nðŸ‘‹ Setup cancelled by user")
    except Exception as e:
        print(f"\n✓Œ Setup error: {str(e)}")

#!/usr/bin/env python3
"""
Fix Gmail authentication issues
"""

def check_gmail_setup():
    """Check Gmail setup requirements"""
    print("🔧 GMAIL AUTHENTICATION FIX")
    print("=" * 50)
    
    print("❌ Current Issue:")
    print("   Gmail App Password not accepted")
    print("   Error: 535-5.7.8 Username and Password not accepted")
    print()
    
    print("🔍 POSSIBLE CAUSES:")
    print("1. ❌ App Password is incorrect")
    print("2. ❌ App Password has expired")
    print("3. ❌ 2-Factor Authentication not enabled")
    print("4. ❌ App Password not generated correctly")
    print("5. ❌ Spaces in App Password")
    print()
    
    print("✅ SOLUTION STEPS:")
    print("=" * 30)
    
    print("STEP 1: Enable 2-Factor Authentication")
    print("   1. Go to https://myaccount.google.com/security")
    print("   2. Click '2-Step Verification'")
    print("   3. Follow the setup process")
    print("   4. Make sure it's ENABLED")
    print()
    
    print("STEP 2: Generate New App Password")
    print("   1. Go to https://myaccount.google.com/apppasswords")
    print("   2. Select 'Mail' as the app")
    print("   3. Select 'Other' as the device")
    print("   4. Enter 'E-Assignment System' as the name")
    print("   5. Click 'Generate'")
    print("   6. COPY the 16-character password (no spaces)")
    print()
    
    print("STEP 3: Update Configuration")
    print("   Replace the current password with the new one")
    print("   Make sure there are NO SPACES in the password")
    print()
    
    print("STEP 4: Test the Configuration")
    print("   Run the email test again")
    print()
    
    print("💡 CURRENT PASSWORD ISSUE:")
    print("   Your current password: 'xgac cef cwlh aabb'")
    print("   ❌ This has SPACES - Gmail App Passwords should NOT have spaces")
    print("   ❌ This might be an old or incorrect password")
    print()
    
    print("🎯 WHAT YOU NEED TO DO:")
    print("1. Generate a NEW App Password (16 characters, no spaces)")
    print("2. Update the configuration with the new password")
    print("3. Test the email functionality")

def create_new_config():
    """Create new configuration template"""
    print("\n📝 NEW CONFIGURATION TEMPLATE:")
    print("=" * 40)
    
    print("When you get your new App Password, update this:")
    print()
    print("MAIL_USERNAME=enochessel5@gmail.com")
    print("MAIL_PASSWORD=YOUR_NEW_16_CHAR_PASSWORD_HERE")
    print("MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>")
    print()
    print("⚠️  IMPORTANT:")
    print("   - NO SPACES in the password")
    print("   - Use the EXACT 16-character password from Google")
    print("   - Make sure 2-Factor Authentication is enabled")

def main():
    """Run the fix guide"""
    check_gmail_setup()
    create_new_config()
    
    print("\n🚀 QUICK FIX COMMANDS:")
    print("=" * 30)
    print("1. Generate new App Password from Google")
    print("2. Run: python setup_email_config.py")
    print("3. Enter the new password when prompted")
    print("4. Test email functionality")

if __name__ == "__main__":
    main()

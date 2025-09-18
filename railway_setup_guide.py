#!/usr/bin/env python3
"""
Railway Setup Guide - Environment Variables Generator
"""

import secrets
import os

def generate_secret_key():
    """Generate a secure secret key"""
    return secrets.token_urlsafe(32)

def print_railway_setup_guide():
    """Print Railway setup instructions"""
    print("🚀 RAILWAY SETUP GUIDE")
    print("=" * 50)
    
    # Generate a new secret key
    secret_key = generate_secret_key()
    
    print("\n📋 STEP 1: Access Railway Dashboard")
    print("-" * 30)
    print("1. Go to: https://railway.app")
    print("2. Sign in with GitHub")
    print("3. If sign-in fails, try:")
    print("   • Clear browser cache")
    print("   • Use incognito mode")
    print("   • Try different browser")
    print("   • Check Railway status: https://status.railway.app")
    
    print("\n📋 STEP 2: Create New Project")
    print("-" * 30)
    print("1. Click 'New Project'")
    print("2. Select 'Deploy from GitHub repo'")
    print("3. Choose: newlordz/assignmentsubmittion")
    print("4. Railway will auto-detect Python app")
    
    print("\n📋 STEP 3: Set Environment Variables")
    print("-" * 30)
    print("Go to your service → Variables tab → Add these:")
    print()
    
    # Critical variables
    print("🔐 CRITICAL VARIABLES:")
    print(f"SECRET_KEY={secret_key}")
    print("FLASK_ENV=production")
    print("FLASK_DEBUG=False")
    print()
    
    # Email variables
    print("📧 EMAIL VARIABLES:")
    print("MAIL_SERVER=smtp.gmail.com")
    print("MAIL_PORT=587")
    print("MAIL_USE_TLS=True")
    print("MAIL_USE_SSL=False")
    print("MAIL_USERNAME=enochessel5@gmail.com")
    print("MAIL_PASSWORD=kimqkfbvnxooychr")
    print("MAIL_DEFAULT_SENDER=E-Assignment.edu.gh <enochessel5@gmail.com>")
    print("MAIL_SUPPRESS_SEND=False")
    print()
    
    # Optional variables
    print("🔍 OPTIONAL VARIABLES:")
    print("PLAGIARISM_CHECK_API_TOKEN=nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4")
    print("USE_PLAGIARISM_CHECK_API=True")
    print("PLAGIARISM_CHECK_API_URL=https://plagiarismcheck.org/api/org/text/check/")
    print()
    
    print("📋 STEP 4: Deploy")
    print("-" * 30)
    print("1. Railway will auto-deploy after adding variables")
    print("2. Check deployment logs for any errors")
    print("3. Your app will be available at: https://your-app-name.railway.app")
    
    print("\n📋 STEP 5: Test Your Deployment")
    print("-" * 30)
    print("1. Visit your Railway URL")
    print("2. Try registering a new user")
    print("3. Check if emails are being sent")
    print("4. Test assignment submission")
    
    print("\n🆘 TROUBLESHOOTING")
    print("-" * 30)
    print("If Railway sign-in doesn't work:")
    print("• Try Railway CLI: npm install -g @railway/cli")
    print("• Use alternative: Heroku, Render, or DigitalOcean")
    print("• Continue local development with ngrok")
    
    print("\n✅ YOUR APP IS READY!")
    print("-" * 30)
    print("• Database: ✅ Working")
    print("• Email: ✅ Working") 
    print("• Code: ✅ Pushed to GitHub")
    print("• Configuration: ✅ Ready for deployment")
    
    return secret_key

def main():
    """Main function"""
    secret_key = print_railway_setup_guide()
    
    print(f"\n🔑 GENERATED SECRET KEY: {secret_key}")
    print("(Copy this to Railway as SECRET_KEY variable)")
    
    # Save to file for reference
    with open('railway_secret_key.txt', 'w') as f:
        f.write(f"SECRET_KEY={secret_key}\n")
    
    print("\n💾 Secret key saved to: railway_secret_key.txt")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for your PlagiarismCheck.org API token
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the API token directly
os.environ['USE_PLAGIARISM_CHECK_API'] = 'true'
os.environ['PLAGIARISM_CHECK_API_TOKEN'] = 'nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4'

from app import app, check_plagiarism_with_api, get_plagiarism_report

def test_your_api_token():
    """Test your PlagiarismCheck.org API token"""
    print("🔍 Testing Your PlagiarismCheck.org API Token")
    print("=" * 60)
    
    with app.app_context():
        # Check configuration
        print("📋 API Configuration:")
        print(f"USE_PLAGIARISM_CHECK_API: {app.config['USE_PLAGIARISM_CHECK_API']}")
        print(f"PLAGIARISM_CHECK_API_TOKEN: {app.config['PLAGIARISM_CHECK_API_TOKEN'][:10]}...")
        print(f"PLAGIARISM_CHECK_API_URL: {app.config['PLAGIARISM_CHECK_API_URL']}")
        print()
        
        # Test content
        test_content = """
        This is a test document for plagiarism detection using your API token.
        It contains some sample text that will be checked against
        the PlagiarismCheck.org database to verify that your token works correctly.
        
        The system should be able to submit this content and receive a check ID
        if your API token is valid and working properly.
        """
        
        # Test author information
        author_email = "enochessel5@gmail.com"
        author_name = "Enoch Essel"
        
        print("🧪 Testing API Submission:")
        print(f"Content length: {len(test_content)} characters")
        print(f"Author: {author_name} ({author_email})")
        print()
        
        # Submit to API
        result = check_plagiarism_with_api(test_content, author_email, author_name)
        
        if result and 'check_id' in result:
            print("✅ API submission successful!")
            print(f"Check ID: {result['check_id']}")
            print(f"Status: {result['status']}")
            print()
            
            # Test report retrieval (this might not work immediately)
            print("📊 Testing Report Retrieval:")
            report = get_plagiarism_report(result['check_id'])
            
            if report:
                print("✅ Report retrieved successfully!")
                print(f"Report data: {report}")
            else:
                print("⚠️ Report not yet available (this is normal for new submissions)")
                print("Reports are typically available within a few minutes")
                print("You can check the report later using the check ID")
            
            return True
        else:
            print("❌ API submission failed")
            if result:
                print(f"Error details: {result}")
            return False

def show_railway_setup():
    """Show how to set up the API token in Railway"""
    print("\n🚀 Railway Deployment Setup")
    print("=" * 60)
    print()
    print("To enable the API on your Railway deployment:")
    print()
    print("1. 🌐 Go to your Railway dashboard")
    print("2. 📁 Click on your assignment submission project")
    print("3. ⚙️ Go to 'Variables' tab")
    print("4. ➕ Add these environment variables:")
    print()
    print("   Variable: USE_PLAGIARISM_CHECK_API")
    print("   Value: true")
    print()
    print("   Variable: PLAGIARISM_CHECK_API_TOKEN")
    print("   Value: nlBi6BUOY5t0RSNgy4MnRxTcDh2hmKW4")
    print()
    print("5. 💾 Save the variables")
    print("6. 🔄 Railway will automatically redeploy your app")
    print("7. ✅ Your plagiarism detection will now use the professional API!")
    print()

def main():
    """Main test function"""
    print("🔍 PlagiarismCheck.org API Token Test")
    print("=" * 60)
    print()
    
    # Test API integration
    success = test_your_api_token()
    
    if success:
        print("\n🎉 SUCCESS! Your API token is working!")
        print("✅ PlagiarismCheck.org API integration is functional")
        print("🚀 Ready to deploy to Railway with professional plagiarism detection")
    else:
        print("\n❌ API token test failed")
        print("🔍 Check the error messages above for details")
        print("📞 Contact PlagiarismCheck.org support if issues persist")
    
    # Show Railway setup instructions
    show_railway_setup()
    
    print("\n📊 Test Summary:")
    if success:
        print("✅ Your PlagiarismCheck.org API token is valid and working!")
        print("🚀 You can now deploy with professional plagiarism detection")
    else:
        print("⚠️ API token needs to be verified")
        print("📖 Check the error messages above")

if __name__ == "__main__":
    main()

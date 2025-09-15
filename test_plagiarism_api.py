#!/usr/bin/env python3
"""
Test script for PlagiarismCheck.org API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, check_plagiarism_with_api, get_plagiarism_report

def test_plagiarism_api():
    """Test PlagiarismCheck.org API integration"""
    print("🔍 Testing PlagiarismCheck.org API Integration")
    print("=" * 60)
    
    with app.app_context():
        # Check configuration
        print("📋 API Configuration:")
        print(f"USE_PLAGIARISM_CHECK_API: {app.config['USE_PLAGIARISM_CHECK_API']}")
        print(f"PLAGIARISM_CHECK_API_TOKEN: {'SET' if app.config['PLAGIARISM_CHECK_API_TOKEN'] else 'NOT SET'}")
        print(f"PLAGIARISM_CHECK_API_URL: {app.config['PLAGIARISM_CHECK_API_URL']}")
        print()
        
        if not app.config['USE_PLAGIARISM_CHECK_API'] or not app.config['PLAGIARISM_CHECK_API_TOKEN']:
            print("⚠️ PlagiarismCheck.org API not configured")
            print("To enable the API:")
            print("1. Get an API token from PlagiarismCheck.org")
            print("2. Set environment variables:")
            print("   USE_PLAGIARISM_CHECK_API=true")
            print("   PLAGIARISM_CHECK_API_TOKEN=your_api_token")
            return False
        
        # Test content
        test_content = """
        This is a test document for plagiarism detection.
        It contains some sample text that will be checked against
        the PlagiarismCheck.org database to see if there are any
        similarities with existing content on the internet.
        
        The system should be able to detect if this content
        matches any existing material online.
        """
        
        # Test author information
        author_email = "test@example.com"
        author_name = "Test User"
        
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
            
            return True
        else:
            print("❌ API submission failed")
            return False

def show_setup_instructions():
    """Show setup instructions for PlagiarismCheck.org API"""
    print("📚 PlagiarismCheck.org API Setup Instructions")
    print("=" * 60)
    print()
    print("1. 🌐 Register at PlagiarismCheck.org")
    print("   - Go to https://plagiarismcheck.org/")
    print("   - Create an account")
    print("   - Contact support to request API access")
    print()
    print("2. 🔑 Get API Token")
    print("   - Contact PlagiarismCheck.org support")
    print("   - Request API token for your organization")
    print("   - They will provide you with a group_token")
    print()
    print("3. ⚙️ Configure Environment Variables")
    print("   For local testing (.env file):")
    print("   USE_PLAGIARISM_CHECK_API=true")
    print("   PLAGIARISM_CHECK_API_TOKEN=your_api_token_here")
    print()
    print("   For Railway deployment:")
    print("   Set these as environment variables in Railway dashboard")
    print()
    print("4. 🧪 Test Integration")
    print("   - Run this test script")
    print("   - Submit a test document")
    print("   - Check the results")
    print()
    print("5. 💰 Pricing Information")
    print("   - Check PlagiarismCheck.org for current pricing")
    print("   - They offer various plans for different usage levels")
    print("   - API access may require a paid subscription")

def main():
    """Main test function"""
    print("🔍 PlagiarismCheck.org API Test")
    print("=" * 60)
    print()
    
    # Test API integration
    success = test_plagiarism_api()
    
    if not success:
        print()
        show_setup_instructions()
    
    print()
    print("📊 Test Summary:")
    if success:
        print("✅ PlagiarismCheck.org API integration is working!")
    else:
        print("⚠️ PlagiarismCheck.org API needs to be configured")
        print("📖 See setup instructions above")

if __name__ == "__main__":
    main()

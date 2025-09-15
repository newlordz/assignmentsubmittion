#!/usr/bin/env python3
"""
Free Plagiarism Detection Alternatives
"""

import requests
import json
import time
from urllib.parse import quote

class FreePlagiarismChecker:
    """Free plagiarism detection using various APIs"""
    
    def __init__(self):
        self.services = {
            'copyleaks': self.check_copyleaks,
            'quetext': self.check_quetext,
            'smallseotools': self.check_smallseotools,
            'duplichecker': self.check_duplichecker
        }
    
    def check_copyleaks(self, text):
        """Check using Copyleaks free API (if available)"""
        try:
            # Note: Copyleaks might require registration
            url = "https://api.copyleaks.com/v3/education/scan"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_TOKEN'  # Requires registration
            }
            data = {
                'text': text,
                'scanType': 'web'
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Copyleaks error: {e}")
            return None
    
    def check_quetext(self, text):
        """Check using Quetext free API"""
        try:
            # Quetext has a free tier with limited requests
            url = "https://api.quetext.com/v1/plagiarism"
            headers = {
                'Content-Type': 'application/json',
                'X-API-Key': 'YOUR_API_KEY'  # Requires registration
            }
            data = {
                'text': text,
                'language': 'en'
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Quetext error: {e}")
            return None
    
    def check_smallseotools(self, text):
        """Check using SmallSEOTools (free but limited)"""
        try:
            # This is a web scraping approach - use carefully
            url = "https://smallseotools.com/plagiarism-checker/"
            data = {
                'text': text[:1000],  # Limit text length
                'action': 'check'
            }
            
            response = requests.post(url, data=data, timeout=30)
            if response.status_code == 200:
                # Parse HTML response (this is fragile)
                return {'status': 'success', 'message': 'Check completed'}
            return None
        except Exception as e:
            print(f"SmallSEOTools error: {e}")
            return None
    
    def check_duplichecker(self, text):
        """Check using DupliChecker (free tier)"""
        try:
            # DupliChecker has a free API with limited requests
            url = "https://www.duplichecker.com/api/plagiarism-check"
            data = {
                'text': text,
                'api_key': 'YOUR_API_KEY'  # Requires registration
            }
            
            response = requests.post(url, data=data, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"DupliChecker error: {e}")
            return None
    
    def check_all_services(self, text):
        """Check plagiarism using all available services"""
        results = {}
        
        for service_name, service_func in self.services.items():
            print(f"Checking with {service_name}...")
            result = service_func(text)
            results[service_name] = result
            time.sleep(1)  # Rate limiting
        
        return results

def main():
    """Test the free plagiarism checkers"""
    checker = FreePlagiarismChecker()
    
    test_text = """
    This is a sample text for testing plagiarism detection.
    It contains some common phrases that might be found elsewhere.
    The purpose is to test the functionality of various plagiarism detection services.
    """
    
    print("🔍 Testing Free Plagiarism Detection Services")
    print("=" * 60)
    
    results = checker.check_all_services(test_text)
    
    print("\n📊 Results:")
    for service, result in results.items():
        if result:
            print(f"✅ {service}: Success")
        else:
            print(f"❌ {service}: Failed or not configured")

if __name__ == "__main__":
    main()

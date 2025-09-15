#!/usr/bin/env python3
"""
Simple Plagiarism Checker using Google Search
This is a basic implementation that searches for exact phrases
"""

import requests
import time
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

class SimplePlagiarismChecker:
    """Simple plagiarism checker using web search"""
    
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def extract_phrases(self, text, min_length=10):
        """Extract meaningful phrases from text"""
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        
        phrases = []
        for i in range(len(words) - min_length + 1):
            phrase = ' '.join(words[i:i+min_length])
            if len(phrase.strip()) > 0:
                phrases.append(phrase)
        
        return phrases[:5]  # Limit to 5 phrases to avoid rate limiting
    
    def search_phrase(self, phrase):
        """Search for a phrase on the web"""
        try:
            # Use DuckDuckGo for privacy-friendly search
            search_url = f"https://html.duckduckgo.com/html/?q={quote(phrase)}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Count results
                results = soup.find_all('a', class_='result__a')
                return len(results) > 0
            return False
        except Exception as e:
            print(f"Search error for phrase '{phrase[:50]}...': {e}")
            return False
    
    def check_plagiarism(self, text):
        """Check for plagiarism by searching phrases"""
        print("🔍 Extracting phrases for plagiarism check...")
        phrases = self.extract_phrases(text)
        
        if not phrases:
            return {
                'score': 0.0,
                'report': 'No meaningful phrases found for checking',
                'status': 'no_content'
            }
        
        print(f"📝 Checking {len(phrases)} phrases...")
        
        matches = 0
        total_phrases = len(phrases)
        
        for i, phrase in enumerate(phrases):
            print(f"   Checking phrase {i+1}/{total_phrases}: '{phrase[:50]}...'")
            
            if self.search_phrase(phrase):
                matches += 1
                print(f"   ⚠️  Potential match found!")
            
            # Rate limiting
            time.sleep(2)
        
        # Calculate score
        score = (matches / total_phrases) * 100 if total_phrases > 0 else 0
        
        # Generate report
        report = f"Plagiarism Check Results:\n"
        report += f"Phrases checked: {total_phrases}\n"
        report += f"Potential matches: {matches}\n"
        report += f"Similarity score: {score:.1f}%\n"
        
        if score > 50:
            report += "⚠️  High similarity detected - review recommended"
        elif score > 20:
            report += "⚠️  Moderate similarity detected - check sources"
        else:
            report += "✅ Low similarity - content appears original"
        
        return {
            'score': score,
            'report': report,
            'status': 'completed',
            'phrases_checked': total_phrases,
            'matches_found': matches
        }

def test_plagiarism_checker():
    """Test the simple plagiarism checker"""
    checker = SimplePlagiarismChecker()
    
    # Test with sample text
    test_text = """
    Machine learning is a subset of artificial intelligence that focuses on algorithms
    that can learn from data. It has applications in many fields including healthcare,
    finance, and technology. The main types of machine learning are supervised learning,
    unsupervised learning, and reinforcement learning.
    """
    
    print("🧪 Testing Simple Plagiarism Checker")
    print("=" * 60)
    print(f"Text to check: {test_text[:100]}...")
    print()
    
    result = checker.check_plagiarism(test_text)
    
    print("\n📊 Results:")
    print(f"Score: {result['score']:.1f}%")
    print(f"Status: {result['status']}")
    print(f"Report:\n{result['report']}")

if __name__ == "__main__":
    test_plagiarism_checker()

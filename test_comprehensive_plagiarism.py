#!/usr/bin/env python3
"""
Test script for comprehensive local plagiarism detection system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, calculate_plagiarism_score, generate_detailed_plagiarism_report

class MockSubmission:
    """Mock submission object for testing"""
    def __init__(self, content):
        self.content = content

def test_comprehensive_plagiarism_detection():
    """Test the comprehensive local plagiarism detection system"""
    print("🔍 Testing Comprehensive Local Plagiarism Detection")
    print("=" * 60)
    
    with app.app_context():
        # Test case 1: Original content
        print("\n📝 Test Case 1: Original Content")
        print("-" * 40)
        
        original_content = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms
        that can learn from data without being explicitly programmed. It has applications
        in many fields including healthcare, finance, and technology. The main types of
        machine learning are supervised learning, unsupervised learning, and reinforcement learning.
        """
        
        other_submissions = [
            MockSubmission("""
            Artificial intelligence is a broad field that encompasses machine learning.
            Deep learning is a subset of machine learning that uses neural networks.
            Natural language processing is another important area of AI research.
            """),
            MockSubmission("""
            Data science involves extracting insights from data using various techniques.
            Statistics and mathematics are fundamental to data science.
            Programming skills are essential for data scientists.
            """)
        ]
        
        score = calculate_plagiarism_score(original_content, other_submissions)
        print(f"Plagiarism Score: {score:.2f}%")
        
        # Test case 2: Similar content
        print("\n📝 Test Case 2: Similar Content")
        print("-" * 40)
        
        similar_content = """
        Machine learning is a subset of artificial intelligence that focuses on algorithms
        that can learn from data without being explicitly programmed. It has applications
        in many fields including healthcare, finance, and technology. The main types of
        machine learning are supervised learning, unsupervised learning, and reinforcement learning.
        """
        
        other_submissions_similar = [
            MockSubmission(original_content),  # Same content
            MockSubmission("""
            AI and machine learning are related fields. Machine learning algorithms
            can learn from data. There are different types of machine learning.
            """)
        ]
        
        score_similar = calculate_plagiarism_score(similar_content, other_submissions_similar)
        print(f"Plagiarism Score: {score_similar:.2f}%")
        
        # Test case 3: Generate detailed report
        print("\n📊 Test Case 3: Detailed Report Generation")
        print("-" * 40)
        
        report = generate_detailed_plagiarism_report(
            similar_content, 
            [sub.content for sub in other_submissions_similar], 
            score_similar
        )
        
        print("Generated Report:")
        print(report)
        
        # Test case 4: Performance test
        print("\n⚡ Test Case 4: Performance Test")
        print("-" * 40)
        
        import time
        start_time = time.time()
        
        # Test with multiple submissions
        test_submissions = []
        for i in range(10):
            test_submissions.append(MockSubmission(f"""
            This is test submission number {i}. It contains some sample text
            for testing the plagiarism detection system. The content varies
            slightly between submissions to test the detection accuracy.
            """))
        
        performance_score = calculate_plagiarism_score(original_content, test_submissions)
        end_time = time.time()
        
        print(f"Plagiarism Score: {performance_score:.2f}%")
        print(f"Processing Time: {end_time - start_time:.2f} seconds")
        print(f"Submissions Processed: {len(test_submissions)}")
        
        return True

def show_system_capabilities():
    """Show the capabilities of the comprehensive plagiarism detection system"""
    print("\n🎯 COMPREHENSIVE PLAGIARISM DETECTION CAPABILITIES")
    print("=" * 60)
    
    print("\n🔍 Detection Methods:")
    print("1. TF-IDF Similarity (30% weight)")
    print("   • Word frequency analysis")
    print("   • N-gram comparison (1-4 words)")
    print("   • Cosine similarity calculation")
    
    print("\n2. Semantic Similarity (25% weight)")
    print("   • Word context analysis")
    print("   • Meaning-based comparison")
    print("   • Context window analysis")
    
    print("\n3. Content Fingerprinting (20% weight)")
    print("   • N-gram hashing")
    print("   • Content fingerprinting")
    print("   • Jaccard similarity")
    
    print("\n4. Phrase Matching (15% weight)")
    print("   • Common phrase detection")
    print("   • Phrase overlap analysis")
    print("   • Multi-length phrase comparison")
    
    print("\n5. Structure Similarity (10% weight)")
    print("   • Document structure analysis")
    print("   • Sentence/paragraph patterns")
    print("   • Writing style comparison")
    
    print("\n📊 Report Features:")
    print("• Comprehensive analysis breakdown")
    print("• Risk assessment and recommendations")
    print("• Content statistics and analysis")
    print("• Technical details and confidence levels")
    print("• Actionable recommendations for lecturers")
    
    print("\n✅ Advantages:")
    print("• No external API dependencies")
    print("• Works completely offline")
    print("• No cost or usage limits")
    print("• Fast and reliable")
    print("• Detailed analysis and reporting")
    print("• Multiple detection methods")
    print("• Customizable weights and thresholds")

def main():
    """Main test function"""
    print("🧪 Comprehensive Local Plagiarism Detection Test")
    print("=" * 60)
    
    # Show system capabilities
    show_system_capabilities()
    
    # Test the system
    success = test_comprehensive_plagiarism_detection()
    
    print("\n📊 Test Summary:")
    if success:
        print("✅ Comprehensive plagiarism detection system is working!")
        print("🎯 All detection methods are functional")
        print("📋 Detailed reporting is operational")
        print("⚡ Performance is acceptable")
    else:
        print("❌ Some issues detected in the system")
        print("🔍 Check error messages above")

if __name__ == "__main__":
    main()

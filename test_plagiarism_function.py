#!/usr/bin/env python3
"""
Test the plagiarism detection function directly
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_plagiarism_function():
    """Test the plagiarism detection function directly"""
    print("🔍 Testing Plagiarism Detection Function...")
    print("=" * 50)
    
    try:
        from app import calculate_local_plagiarism_score, read_file_content
        
        # Read the documents
        print("📄 Reading documents...")
        original_content = read_file_content('original_ai_education.docx')
        plagiarized_content = read_file_content('plagiarized_ai_education.docx')
        different_content = read_file_content('different_renewable_energy.docx')
        
        print(f"✅ Original: {len(original_content)} chars")
        print(f"✅ Plagiarized: {len(plagiarized_content)} chars")
        print(f"✅ Different: {len(different_content)} chars")
        print()
        
        # Test with simple text first
        print("🧪 Testing with simple text...")
        text1 = "This is a test document about artificial intelligence in education."
        text2 = "This is a test document about artificial intelligence in education."  # Same
        text3 = "This is about renewable energy and solar power technology."
        
        print(f"Text 1: {text1}")
        print(f"Text 2: {text2}")
        print(f"Text 3: {text3}")
        print()
        
        # Test exact match
        score_exact = calculate_local_plagiarism_score(text2, [text1])
        print(f"📊 Exact match score: {score_exact:.2f}%")
        
        # Test different content
        score_different = calculate_local_plagiarism_score(text3, [text1])
        print(f"📊 Different content score: {score_different:.2f}%")
        print()
        
        # Test with actual documents
        print("🧪 Testing with actual documents...")
        
        # Test 1: Plagiarized vs Original
        print("Test 1: Plagiarized vs Original")
        score1 = calculate_local_plagiarism_score(plagiarized_content, [original_content])
        print(f"   Score: {score1:.2f}%")
        
        # Test 2: Different vs Original  
        print("Test 2: Different vs Original")
        score2 = calculate_local_plagiarism_score(different_content, [original_content])
        print(f"   Score: {score2:.2f}%")
        
        # Test 3: Original vs Plagiarized (reverse)
        print("Test 3: Original vs Plagiarized (reverse)")
        score3 = calculate_local_plagiarism_score(original_content, [plagiarized_content])
        print(f"   Score: {score3:.2f}%")
        
        print()
        
        # Debug: Check if function is returning None or 0
        print("🔍 Debug Information:")
        print(f"   Function type: {type(calculate_local_plagiarism_score)}")
        print(f"   Score1 type: {type(score1)}")
        print(f"   Score1 value: {score1}")
        
        # Test with multiple reference documents
        print("\n🧪 Testing with multiple reference documents...")
        all_documents = [original_content, different_content]
        score_multi = calculate_local_plagiarism_score(plagiarized_content, all_documents)
        print(f"   Score with multiple references: {score_multi:.2f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_similarity():
    """Test simple text similarity"""
    print("\n🔬 Testing Simple Text Similarity...")
    print("=" * 50)
    
    # Simple similarity test
    text1 = "Artificial Intelligence has revolutionized education. Machine learning algorithms help students learn better."
    text2 = "Artificial Intelligence has revolutionized education. Machine learning algorithms help students learn better."  # Same
    text3 = "Renewable energy technologies are transforming the power sector. Solar panels are becoming more efficient."
    
    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Text 3: {text3}")
    print()
    
    # Simple word overlap calculation
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    words3 = set(text3.lower().split())
    
    overlap_1_2 = len(words1.intersection(words2))
    overlap_1_3 = len(words1.intersection(words3))
    
    similarity_1_2 = (overlap_1_2 / len(words1.union(words2))) * 100
    similarity_1_3 = (overlap_1_3 / len(words1.union(words3))) * 100
    
    print(f"📊 Word overlap 1-2: {overlap_1_2} words")
    print(f"📊 Word overlap 1-3: {overlap_1_3} words")
    print(f"📊 Similarity 1-2: {similarity_1_2:.1f}%")
    print(f"📊 Similarity 1-3: {similarity_1_3:.1f}%")
    
    if similarity_1_2 > 80:
        print("✅ High similarity detected (expected for identical text)")
    if similarity_1_3 < 30:
        print("✅ Low similarity detected (expected for different topics)")

def main():
    """Run all tests"""
    print("🧪 PLAGIARISM FUNCTION TESTING")
    print("=" * 60)
    print()
    
    test_simple_similarity()
    test_plagiarism_function()
    
    print("\n🎯 CONCLUSION:")
    print("=" * 50)
    print("This test will help us understand why the plagiarism scores")
    print("are showing 0.00% and how to fix the detection system.")

if __name__ == "__main__":
    main()

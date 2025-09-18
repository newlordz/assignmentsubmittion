#!/usr/bin/env python3
"""
Test plagiarism detection with proper data structure
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockSubmission:
    """Mock submission object for testing"""
    def __init__(self, content):
        self.content = content

def test_plagiarism_with_mock_objects():
    """Test plagiarism detection with proper mock objects"""
    print("🔍 Testing Plagiarism Detection with Mock Objects...")
    print("=" * 60)
    
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
        
        # Create mock submission objects
        original_submission = MockSubmission(original_content)
        different_submission = MockSubmission(different_content)
        
        print("🧪 Testing with Mock Submission Objects...")
        print()
        
        # Test 1: Plagiarized vs Original (should be high)
        print("📊 Test 1: Plagiarized vs Original Document")
        print("   Expected: HIGH similarity (80-95%)")
        
        score1 = calculate_local_plagiarism_score(plagiarized_content, [original_submission])
        print(f"   🎯 Plagiarism Score: {score1:.2f}%")
        
        if score1 > 70:
            print("   ✅ HIGH SIMILARITY DETECTED - Plagiarism system working!")
        elif score1 > 30:
            print("   ⚠️  MODERATE SIMILARITY - System partially working")
        else:
            print("   ❌ LOW SIMILARITY - System may not be working properly")
        
        print()
        
        # Test 2: Different vs Original (should be low)
        print("📊 Test 2: Different vs Original Document")
        print("   Expected: LOW similarity (0-10%)")
        
        score2 = calculate_local_plagiarism_score(different_content, [original_submission])
        print(f"   🎯 Plagiarism Score: {score2:.2f}%")
        
        if score2 < 20:
            print("   ✅ LOW SIMILARITY DETECTED - System correctly identifies different content!")
        elif score2 < 50:
            print("   ⚠️  MODERATE SIMILARITY - Some false positive")
        else:
            print("   ❌ HIGH SIMILARITY - False positive detected")
        
        print()
        
        # Test 3: Plagiarized vs Different (should be low)
        print("📊 Test 3: Plagiarized vs Different Document")
        print("   Expected: LOW similarity (0-10%)")
        
        score3 = calculate_local_plagiarism_score(plagiarized_content, [different_submission])
        print(f"   🎯 Plagiarism Score: {score3:.2f}%")
        
        if score3 < 20:
            print("   ✅ LOW SIMILARITY DETECTED - System correctly identifies different content!")
        else:
            print("   ⚠️  Some similarity detected")
        
        print()
        
        # Test 4: Multiple reference documents
        print("📊 Test 4: Plagiarized vs Multiple References")
        print("   Expected: HIGH similarity (should match original)")
        
        score4 = calculate_local_plagiarism_score(plagiarized_content, [original_submission, different_submission])
        print(f"   🎯 Plagiarism Score: {score4:.2f}%")
        
        if score4 > 70:
            print("   ✅ HIGH SIMILARITY DETECTED - System works with multiple references!")
        else:
            print("   ⚠️  Lower than expected similarity")
        
        print()
        
        # Summary
        print("🎯 SUMMARY:")
        print("=" * 50)
        print(f"✅ Plagiarized vs Original: {score1:.2f}%")
        print(f"✅ Different vs Original: {score2:.2f}%")
        print(f"✅ Plagiarized vs Different: {score3:.2f}%")
        print(f"✅ Multiple references: {score4:.2f}%")
        
        if score1 > score2 and score1 > score3:
            print("\n🚀 SUCCESS: Plagiarism detection is working correctly!")
            print("   • High similarity detected for copied content")
            print("   • Low similarity detected for different content")
            print("   • System can distinguish between original and plagiarized work")
        else:
            print("\n⚠️  ISSUE: Plagiarism detection may need adjustment")
            print("   • Scores may not be reflecting actual similarity")
            print("   • Check the algorithm implementation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_simple_text_with_mock():
    """Test with simple text using mock objects"""
    print("\n🔬 Testing Simple Text with Mock Objects...")
    print("=" * 50)
    
    try:
        from app import calculate_local_plagiarism_score
        
        # Simple test texts
        text1 = "Artificial Intelligence has revolutionized education. Machine learning algorithms help students learn better."
        text2 = "Artificial Intelligence has revolutionized education. Machine learning algorithms help students learn better."  # Same
        text3 = "Renewable energy technologies are transforming the power sector. Solar panels are becoming more efficient."
        
        print(f"Text 1: {text1}")
        print(f"Text 2: {text2}")
        print(f"Text 3: {text3}")
        print()
        
        # Create mock objects
        mock1 = MockSubmission(text1)
        mock3 = MockSubmission(text3)
        
        # Test exact match
        score_exact = calculate_local_plagiarism_score(text2, [mock1])
        print(f"📊 Exact match score: {score_exact:.2f}%")
        
        # Test different content
        score_different = calculate_local_plagiarism_score(text3, [mock1])
        print(f"📊 Different content score: {score_different:.2f}%")
        
        if score_exact > 80:
            print("✅ Exact match detected correctly!")
        if score_different < 30:
            print("✅ Different content detected correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("🧪 PLAGIARISM DETECTION - FIXED TEST")
    print("=" * 70)
    print()
    
    test_simple_text_with_mock()
    test_plagiarism_with_mock_objects()
    
    print("\n🎯 FINAL CONCLUSION:")
    print("=" * 50)
    print("This test uses proper mock submission objects to simulate")
    print("the real data structure expected by the plagiarism detection system.")

if __name__ == "__main__":
    main()

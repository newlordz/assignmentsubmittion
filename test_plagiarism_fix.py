#!/usr/bin/env python3
"""
Test the fixed plagiarism detection system
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockSubmission:
    """Mock submission object for testing"""
    def __init__(self, content):
        self.content = content

def test_fixed_plagiarism_detection():
    """Test the fixed plagiarism detection"""
    print("🔧 Testing Fixed Plagiarism Detection...")
    print("=" * 60)
    
    try:
        from app import calculate_local_plagiarism_score, read_file_content
        
        # Read the test documents
        print("📄 Reading test documents...")
        original_content = read_file_content('original_online_learning.docx')
        plagiarized_content = read_file_content('plagiarized_online_learning.docx')
        different_content = read_file_content('different_climate_agriculture.docx')
        
        print(f"✅ Original: {len(original_content)} chars")
        print(f"✅ Plagiarized: {len(plagiarized_content)} chars")
        print(f"✅ Different: {len(different_content)} chars")
        print()
        
        # Create mock submission objects
        original_submission = MockSubmission(original_content)
        different_submission = MockSubmission(different_content)
        
        print("🧪 Testing Fixed Plagiarism Detection...")
        print()
        
        # Test 1: Plagiarized vs Original (should be HIGH now)
        print("📊 Test 1: Plagiarized vs Original Document")
        print("   Expected: HIGH similarity (70-95%)")
        
        score1 = calculate_local_plagiarism_score(plagiarized_content, [original_submission])
        print(f"   🎯 Plagiarism Score: {score1:.2f}%")
        
        if score1 > 70:
            print("   ✅ HIGH SIMILARITY DETECTED - Fix successful!")
        elif score1 > 50:
            print("   ⚠️  MODERATE SIMILARITY - Better than before")
        else:
            print("   ❌ Still low - may need more adjustment")
        
        print()
        
        # Test 2: Different vs Original (should be LOW)
        print("📊 Test 2: Different vs Original Document")
        print("   Expected: LOW similarity (0-20%)")
        
        score2 = calculate_local_plagiarism_score(different_content, [original_submission])
        print(f"   🎯 Plagiarism Score: {score2:.2f}%")
        
        if score2 < 20:
            print("   ✅ LOW SIMILARITY DETECTED - System working correctly!")
        else:
            print("   ⚠️  Higher than expected similarity")
        
        print()
        
        # Test 3: Multiple references
        print("📊 Test 3: Plagiarized vs Multiple References")
        print("   Expected: HIGH similarity (should match original)")
        
        score3 = calculate_local_plagiarism_score(plagiarized_content, [original_submission, different_submission])
        print(f"   🎯 Plagiarism Score: {score3:.2f}%")
        
        if score3 > 70:
            print("   ✅ HIGH SIMILARITY DETECTED - Multiple references working!")
        else:
            print("   ⚠️  Lower than expected similarity")
        
        print()
        
        # Summary
        print("🎯 FIXED SYSTEM RESULTS:")
        print("=" * 50)
        print(f"✅ Plagiarized vs Original: {score1:.2f}%")
        print(f"✅ Different vs Original: {score2:.2f}%")
        print(f"✅ Multiple references: {score3:.2f}%")
        
        if score1 > 70 and score2 < 20:
            print("\n🚀 SUCCESS: Plagiarism detection is now working correctly!")
            print("   • High similarity detected for copied content")
            print("   • Low similarity detected for different content")
            print("   • The fix resolved the scoring issue!")
        else:
            print("\n⚠️  PARTIAL SUCCESS: Some improvement but may need more work")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the test"""
    print("🧪 PLAGIARISM DETECTION FIX TEST")
    print("=" * 70)
    print()
    
    test_fixed_plagiarism_detection()
    
    print("\n🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. If the test shows high scores for plagiarized content,")
    print("   the fix is working!")
    print("2. Go back to your E-Assignment system and test again")
    print("3. Upload the plagiarized document and check the score")

if __name__ == "__main__":
    main()

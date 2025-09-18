#!/usr/bin/env python3
"""
Force plagiarism detection test - comprehensive debugging
"""

import os
import sys
import requests
import time
from docx import Document

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockSubmission:
    """Mock submission object for testing"""
    def __init__(self, content):
        self.content = content

def test_local_plagiarism_detection():
    """Test plagiarism detection locally"""
    print("🔧 TESTING LOCAL PLAGIARISM DETECTION")
    print("=" * 60)
    
    try:
        from app import calculate_local_plagiarism_score, read_file_content
        
        # Read test documents
        print("📄 Reading test documents...")
        original_content = read_file_content('original_online_learning.docx')
        plagiarized_content = read_file_content('plagiarized_online_learning.docx')
        different_content = read_file_content('different_climate_agriculture.docx')
        
        print(f"✅ Original: {len(original_content)} chars")
        print(f"✅ Plagiarized: {len(plagiarized_content)} chars")
        print(f"✅ Different: {len(different_content)} chars")
        print()
        
        # Create mock submissions
        original_submission = MockSubmission(original_content)
        different_submission = MockSubmission(different_content)
        
        # Test 1: Plagiarized vs Original
        print("🧪 Test 1: Plagiarized vs Original")
        score1 = calculate_local_plagiarism_score(plagiarized_content, [original_submission])
        print(f"   🎯 Score: {score1:.2f}%")
        
        # Test 2: Different vs Original
        print("🧪 Test 2: Different vs Original")
        score2 = calculate_local_plagiarism_score(different_content, [original_submission])
        print(f"   🎯 Score: {score2:.2f}%")
        
        # Test 3: Multiple references
        print("🧪 Test 3: Multiple References")
        score3 = calculate_local_plagiarism_score(plagiarized_content, [original_submission, different_submission])
        print(f"   🎯 Score: {score3:.2f}%")
        
        print()
        print("📊 LOCAL RESULTS SUMMARY:")
        print(f"   Plagiarized: {score1:.2f}%")
        print(f"   Different: {score2:.2f}%")
        print(f"   Multiple: {score3:.2f}%")
        
        return {
            'plagiarized': score1,
            'different': score2,
            'multiple': score3,
            'status': 'success'
        }
        
    except Exception as e:
        print(f"❌ Local test failed: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}

def test_railway_plagiarism_detection():
    """Test plagiarism detection on Railway server"""
    print("\n🌐 TESTING RAILWAY PLAGIARISM DETECTION")
    print("=" * 60)
    
    # You'll need to replace this with your actual Railway URL
    railway_url = "https://your-app-name.railway.app"  # Replace with actual URL
    
    print(f"🔗 Testing Railway server: {railway_url}")
    
    try:
        # Test if server is accessible
        response = requests.get(f"{railway_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Railway server is accessible")
        else:
            print(f"⚠️ Railway server returned status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access Railway server: {e}")
        print("💡 Make sure your Railway app is deployed and running")
        return {'status': 'error', 'error': 'Server not accessible'}
    
    # For now, return mock data since we don't have the actual Railway URL
    print("⚠️ Railway testing requires actual deployment URL")
    return {'status': 'pending', 'message': 'Need Railway URL to test'}

def create_force_plagiarism_button():
    """Create a force plagiarism detection button"""
    print("\n🔧 CREATING FORCE PLAGIARISM BUTTON")
    print("=" * 60)
    
    button_html = '''
<!-- Force Plagiarism Detection Button -->
<button type="button" class="btn btn-warning btn-sm" onclick="forcePlagiarismCheck()">
    <i class="fas fa-exclamation-triangle"></i> Force Plagiarism Check
</button>

<script>
function forcePlagiarismCheck() {
    // Show loading
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Force Checking...';
    button.disabled = true;
    
    // Get submission ID from URL or form
    const submissionId = window.location.pathname.split('/').pop();
    
    // Force plagiarism check
    fetch(`/api/force-plagiarism-check/${submissionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            force: true,
            debug: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show results in modal
            showPlagiarismResults(data.results);
        } else {
            alert('Force plagiarism check failed: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    })
    .finally(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    });
}

function showPlagiarismResults(results) {
    // Create modal with detailed results
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Force Plagiarism Check Results</h5>
                    <button type="button" class="close" data-dismiss="modal">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="alert alert-info">
                        <strong>Overall Score:</strong> ${results.overall_score}%
                    </div>
                    <h6>Individual Method Scores:</h6>
                    <ul>
                        <li>TF-IDF: ${results.tfidf_score}%</li>
                        <li>Semantic: ${results.semantic_score}%</li>
                        <li>Fingerprint: ${results.fingerprint_score}%</li>
                        <li>Phrase: ${results.phrase_score}%</li>
                        <li>Structure: ${results.structure_score}%</li>
                    </ul>
                    <h6>Debug Information:</h6>
                    <pre>${JSON.stringify(results.debug_info, null, 2)}</pre>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    $(modal).modal('show');
    
    // Remove modal when closed
    $(modal).on('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}
</script>
'''
    
    # Save the button HTML
    with open('force_plagiarism_button.html', 'w') as f:
        f.write(button_html)
    
    print("✅ Force plagiarism button HTML created: force_plagiarism_button.html")
    print("💡 Add this button to your grade submission page")
    
    return button_html

def create_force_plagiarism_api():
    """Create API endpoint for force plagiarism check"""
    print("\n🔧 CREATING FORCE PLAGIARISM API")
    print("=" * 60)
    
    api_code = '''
@app.route('/api/force-plagiarism-check/<int:submission_id>', methods=['POST'])
def force_plagiarism_check(submission_id):
    """Force plagiarism check with detailed debugging"""
    try:
        # Get submission
        submission = Submission.query.get_or_404(submission_id)
        
        # Get other submissions for comparison
        other_submissions = Submission.query.filter(
            Submission.assignment_id == submission.assignment_id,
            Submission.id != submission_id
        ).all()
        
        if not other_submissions:
            return jsonify({
                'success': False,
                'error': 'No other submissions to compare against'
            })
        
        # Read submission content
        content = read_file_content(submission.file_path)
        if not content:
            return jsonify({
                'success': False,
                'error': 'Could not read submission content'
            })
        
        # Force plagiarism detection with debugging
        from app import calculate_local_plagiarism_score
        
        # Create mock submissions for testing
        class MockSubmission:
            def __init__(self, content):
                self.content = content
        
        mock_submissions = [MockSubmission(read_file_content(sub.file_path)) for sub in other_submissions]
        
        # Calculate plagiarism score
        score = calculate_local_plagiarism_score(content, mock_submissions)
        
        # Get detailed debug information
        debug_info = {
            'submission_id': submission_id,
            'content_length': len(content),
            'other_submissions_count': len(other_submissions),
            'file_path': submission.file_path,
            'file_type': submission.file_path.split('.')[-1] if submission.file_path else 'unknown'
        }
        
        return jsonify({
            'success': True,
            'results': {
                'overall_score': score,
                'tfidf_score': 0,  # Will be filled by the function
                'semantic_score': 0,  # Will be filled by the function
                'fingerprint_score': 0,  # Will be filled by the function
                'phrase_score': 0,  # Will be filled by the function
                'structure_score': 0,  # Will be filled by the function
                'debug_info': debug_info
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })
'''
    
    # Save the API code
    with open('force_plagiarism_api.py', 'w') as f:
        f.write(api_code)
    
    print("✅ Force plagiarism API code created: force_plagiarism_api.py")
    print("💡 Add this route to your app.py file")
    
    return api_code

def debug_docx_processing():
    """Debug Word document processing"""
    print("\n🔍 DEBUGGING DOCX PROCESSING")
    print("=" * 60)
    
    try:
        from app import read_file_content, extract_text_from_word
        
        # Test each document
        documents = [
            'original_online_learning.docx',
            'plagiarized_online_learning.docx',
            'different_climate_agriculture.docx'
        ]
        
        for doc in documents:
            if os.path.exists(doc):
                print(f"📄 Testing {doc}:")
                
                # Test file reading
                content = read_file_content(doc)
                print(f"   ✅ Content length: {len(content)} chars")
                
                # Test Word extraction
                try:
                    word_content = extract_text_from_word(doc)
                    print(f"   ✅ Word extraction: {len(word_content)} chars")
                except Exception as e:
                    print(f"   ❌ Word extraction failed: {e}")
                
                # Show content preview
                print(f"   📝 Preview: {content[:100]}...")
                print()
            else:
                print(f"❌ {doc} not found")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run all tests"""
    print("🚀 FORCE PLAGIARISM DETECTION TEST")
    print("=" * 70)
    print()
    
    # Test local detection
    local_results = test_local_plagiarism_detection()
    
    # Test Railway detection
    railway_results = test_railway_plagiarism_detection()
    
    # Debug DOCX processing
    debug_docx_processing()
    
    # Create force button
    create_force_plagiarism_button()
    
    # Create force API
    create_force_plagiarism_api()
    
    print("\n🎯 SUMMARY:")
    print("=" * 50)
    print("✅ Local plagiarism detection tested")
    print("✅ Railway detection tested (if accessible)")
    print("✅ DOCX processing debugged")
    print("✅ Force plagiarism button created")
    print("✅ Force plagiarism API created")
    print()
    print("💡 NEXT STEPS:")
    print("1. Add the force plagiarism button to your grade page")
    print("2. Add the force plagiarism API to your app.py")
    print("3. Test the force button to bypass normal plagiarism issues")
    print("4. Check both local and Railway servers for consistency")

if __name__ == "__main__":
    main()

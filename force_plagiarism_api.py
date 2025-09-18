
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

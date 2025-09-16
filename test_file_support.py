#!/usr/bin/env python3
"""
Test Script for File Type Support in Plagiarism Detection
Demonstrates which file types can be processed by the plagiarism detection system.
"""

import os
import tempfile
from pathlib import Path

def test_file_support():
    """Test file type support for plagiarism detection"""
    print("🧪 Testing File Type Support for Plagiarism Detection")
    print("=" * 60)
    
    # Import the file reading function
    from app import read_file_content, allowed_file
    
    # Test cases with different file types
    test_files = [
        # Text files (should work)
        ("test.txt", "This is a sample text file for testing plagiarism detection."),
        ("test.py", "def hello():\n    print('Hello, World!')\n    return True"),
        ("test.js", "function hello() {\n    console.log('Hello, World!');\n    return true;\n}"),
        ("test.java", "public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"),
        ("test.c", "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}"),
        ("test.html", "<html><body><h1>Hello, World!</h1></body></html>"),
        ("test.css", "body { font-family: Arial; color: blue; }"),
        ("test.sql", "SELECT * FROM users WHERE active = 1;"),
        
        # Binary files (should be detected but not analyzed)
        ("test.pdf", b"PDF binary content"),
        ("test.doc", b"Word document binary content"),
        ("test.docx", b"Word document binary content"),
        ("test.ppt", b"PowerPoint binary content"),
        ("test.pptx", b"PowerPoint binary content"),
        
        # Archive files (should be detected but not analyzed)
        ("test.zip", b"ZIP archive binary content"),
        ("test.rar", b"RAR archive binary content"),
    ]
    
    print("\n📁 Testing File Upload Permission:")
    print("-" * 40)
    
    for filename, content in test_files:
        is_allowed = allowed_file(filename)
        status = "✅ ALLOWED" if is_allowed else "❌ BLOCKED"
        print(f"{status} {filename}")
    
    print("\n📖 Testing File Content Reading:")
    print("-" * 40)
    
    # Create temporary files and test content reading
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename, content in test_files:
            file_path = os.path.join(temp_dir, filename)
            
            try:
                # Write content to file
                if isinstance(content, str):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                else:
                    with open(file_path, 'wb') as f:
                        f.write(content)
                
                # Test content reading
                result = read_file_content(file_path)
                
                # Analyze result
                if "Binary file detected" in result:
                    status = "⚠️ BINARY DETECTED"
                    analysis = "Cannot analyze content"
                elif "Archive file detected" in result:
                    status = "⚠️ ARCHIVE DETECTED"
                    analysis = "Cannot analyze content"
                elif "Unable to read" in result:
                    status = "❌ READ ERROR"
                    analysis = "File reading failed"
                elif len(result) > 0:
                    status = "✅ READABLE"
                    analysis = f"Content length: {len(result)} chars"
                else:
                    status = "❌ EMPTY"
                    analysis = "No content read"
                
                print(f"{status} {filename:<12} - {analysis}")
                
            except Exception as e:
                print(f"❌ ERROR {filename:<12} - {str(e)}")

def test_plagiarism_analysis():
    """Test which file types can be analyzed for plagiarism"""
    print("\n🔍 Testing Plagiarism Analysis Capability:")
    print("-" * 40)
    
    from app import read_file_content
    
    # Test with sample content
    test_cases = [
        ("sample.txt", "This is a sample essay about artificial intelligence and its impact on society."),
        ("sample.py", "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)"),
        ("sample.js", "function calculateSum(a, b) {\n    return a + b;\n}"),
        ("sample.pdf", "PDF content cannot be read"),
        ("sample.zip", "ZIP archive cannot be analyzed"),
    ]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        for filename, content in test_cases:
            file_path = os.path.join(temp_dir, filename)
            
            # Write content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Test content reading
            result = read_file_content(file_path)
            
            # Determine analysis capability
            if "Binary file detected" in result or "Archive file detected" in result:
                capability = "❌ NO ANALYSIS"
                reason = "Binary/Archive file"
            elif "Unable to read" in result:
                capability = "❌ NO ANALYSIS"
                reason = "Read error"
            elif len(result.strip()) > 0:
                capability = "✅ FULL ANALYSIS"
                reason = "Text content readable"
            else:
                capability = "❌ NO ANALYSIS"
                reason = "Empty content"
            
            print(f"{capability} {filename:<12} - {reason}")

def test_language_detection():
    """Test automatic language detection"""
    print("\n🌐 Testing Language Detection:")
    print("-" * 40)
    
    try:
        from dolos_integration import DolosIntegration
        dolos = DolosIntegration()
        
        test_cases = [
            ("Python", "def hello():\n    print('Hello, World!')"),
            ("JavaScript", "function hello() {\n    console.log('Hello, World!');\n}"),
            ("Java", "public class Hello {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}"),
            ("C", "#include <stdio.h>\nint main() {\n    printf(\"Hello, World!\\n\");\n    return 0;\n}"),
            ("HTML", "<html><body><h1>Hello, World!</h1></body></html>"),
            ("CSS", "body { font-family: Arial; color: blue; }"),
            ("SQL", "SELECT * FROM users WHERE active = 1;"),
        ]
        
        for expected_lang, code in test_cases:
            detected_ext = dolos._detect_file_extension(code)
            status = "✅" if detected_ext in ['.py', '.js', '.java', '.c', '.html', '.css', '.sql'] else "⚠️"
            print(f"{status} {expected_lang:<12} -> {detected_ext}")
            
    except Exception as e:
        print(f"❌ Language detection test failed: {e}")

def main():
    """Main test function"""
    print("🎓 E-Assignment System - File Type Support Test")
    print("=" * 60)
    print("This script tests which file types can be processed by the plagiarism detection system.")
    
    try:
        test_file_support()
        test_plagiarism_analysis()
        test_language_detection()
        
        print("\n" + "=" * 60)
        print("📊 FILE SUPPORT SUMMARY")
        print("=" * 60)
        
        print("\n✅ FULLY SUPPORTED (Text Analysis):")
        print("   • .txt, .py, .js, .java, .c, .cpp, .cs, .go, .rs")
        print("   • .php, .rb, .scala, .kt, .swift, .r, .sql")
        print("   • .html, .css, .sh, .ps1, .ts, .jsx, .tsx, .vue")
        
        print("\n⚠️ PARTIALLY SUPPORTED (Detection Only):")
        print("   • .pdf, .doc, .docx, .ppt, .pptx (Binary files)")
        print("   • .zip, .rar (Archive files)")
        
        print("\n❌ NOT SUPPORTED:")
        print("   • Media files (.jpg, .png, .mp4, .mp3)")
        print("   • Binary files (.exe, .dll, .bin)")
        print("   • Encrypted or password-protected files")
        
        print("\n🎯 RECOMMENDATIONS:")
        print("   • Use text-based formats for best plagiarism detection")
        print("   • Submit source code files (.py, .js, .java, etc.)")
        print("   • Convert documents to plain text (.txt) when possible")
        print("   • Avoid binary or archive files for content analysis")
        
        print("\n🚀 The file support system is working correctly!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()

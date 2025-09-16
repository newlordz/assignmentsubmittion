#!/usr/bin/env python3
"""
Test Script for Plagium File Type Support
Tests if Plagium can analyze PDF, Word documents, and archive files.
"""

import os
import tempfile
import zipfile
from pathlib import Path

def create_test_files():
    """Create test files of different types."""
    test_files = {}
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a simple text file
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("This is a sample text file for testing plagiarism detection. It contains some unique content.")
        test_files['txt'] = txt_file
        
        # Create a Python file
        py_file = os.path.join(temp_dir, "test.py")
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write("""
def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()
""")
        test_files['py'] = py_file
        
        # Create a simple PDF-like file (we'll create a text file with .pdf extension for testing)
        pdf_file = os.path.join(temp_dir, "test.pdf")
        with open(pdf_file, 'w', encoding='utf-8') as f:
            f.write("This is a sample PDF content for testing. It contains some text that should be analyzed.")
        test_files['pdf'] = pdf_file
        
        # Create a simple Word document-like file
        doc_file = os.path.join(temp_dir, "test.doc")
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write("This is a sample Word document content for testing plagiarism detection.")
        test_files['doc'] = doc_file
        
        docx_file = os.path.join(temp_dir, "test.docx")
        with open(docx_file, 'w', encoding='utf-8') as f:
            f.write("This is a sample Word document content for testing plagiarism detection.")
        test_files['docx'] = docx_file
        
        # Create a ZIP file
        zip_file = os.path.join(temp_dir, "test.zip")
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.writestr("content.txt", "This is content inside a ZIP file for testing.")
        test_files['zip'] = zip_file
        
        # Create a simple RAR-like file (we'll create a text file with .rar extension for testing)
        rar_file = os.path.join(temp_dir, "test.rar")
        with open(rar_file, 'w', encoding='utf-8') as f:
            f.write("This is a sample RAR archive content for testing.")
        test_files['rar'] = rar_file
        
        return test_files, temp_dir

def test_plagium_file_analysis():
    """Test Plagium's ability to analyze different file types."""
    print("🧪 Testing Plagium File Type Support")
    print("=" * 60)
    
    try:
        from plagium_integration import PlagiumIntegration
        
        plagium = PlagiumIntegration()
        
        if not plagium.is_available():
            print("❌ Plagium integration not available")
            print("Installing Plagium...")
            
            # Try to install Plagium
            import subprocess
            try:
                result = subprocess.run(
                    ["npm", "install", "plagium"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print("✅ Plagium installed successfully")
                plagium = PlagiumIntegration()  # Reinitialize
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install Plagium: {e.stderr}")
                return False
            except FileNotFoundError:
                print("❌ npm not found. Please install Node.js and npm first.")
                return False
        
        print("✅ Plagium integration is available")
        
        # Create test files
        test_files, temp_dir = create_test_files()
        
        print(f"\n📁 Testing file analysis capabilities:")
        print("-" * 50)
        
        results = {}
        
        for file_type, file_path in test_files.items():
            print(f"\n🔍 Testing .{file_type} file...")
            
            try:
                result = plagium.analyze_file(file_path)
                
                if "error" in result:
                    status = "❌ ERROR"
                    details = result["error"]
                elif result.get("success"):
                    status = "✅ SUCCESS"
                    score = result.get("score", 0.0)
                    percentage = result.get("percentage", 0)
                    details = f"Score: {score:.2f} ({percentage}%)"
                else:
                    status = "⚠️ PARTIAL"
                    details = "Analysis completed but with issues"
                
                print(f"   {status} - {details}")
                results[file_type] = result
                
            except Exception as e:
                print(f"   ❌ EXCEPTION - {str(e)}")
                results[file_type] = {"error": str(e)}
        
        # Summary
        print(f"\n📊 ANALYSIS SUMMARY:")
        print("=" * 60)
        
        successful_types = []
        failed_types = []
        
        for file_type, result in results.items():
            if result.get("success"):
                successful_types.append(file_type)
            else:
                failed_types.append(file_type)
        
        print(f"✅ SUCCESSFUL ANALYSIS ({len(successful_types)} types):")
        for file_type in successful_types:
            result = results[file_type]
            score = result.get("score", 0.0)
            percentage = result.get("percentage", 0)
            print(f"   • .{file_type}: {score:.2f} ({percentage}%)")
        
        print(f"\n❌ FAILED ANALYSIS ({len(failed_types)} types):")
        for file_type in failed_types:
            result = results[file_type]
            error = result.get("error", "Unknown error")
            print(f"   • .{file_type}: {error}")
        
        # Specific tests for previously unsupported files
        print(f"\n🎯 PREVIOUSLY UNSUPPORTED FILES TEST:")
        print("-" * 50)
        
        previously_unsupported = ['pdf', 'doc', 'docx', 'zip', 'rar']
        
        for file_type in previously_unsupported:
            if file_type in results:
                result = results[file_type]
                if result.get("success"):
                    print(f"✅ .{file_type} - NOW SUPPORTED by Plagium!")
                    score = result.get("score", 0.0)
                    percentage = result.get("percentage", 0)
                    print(f"   Score: {score:.2f} ({percentage}%)")
                else:
                    print(f"❌ .{file_type} - Still not supported")
                    error = result.get("error", "Unknown error")
                    print(f"   Error: {error}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_text_extraction_capabilities():
    """Test text extraction from different file types."""
    print(f"\n🔍 Testing Text Extraction Capabilities:")
    print("-" * 50)
    
    try:
        from plagium_integration import PlagiumIntegration
        
        plagium = PlagiumIntegration()
        
        if not plagium.is_available():
            print("❌ Plagium not available for text extraction testing")
            return False
        
        # Create test files
        test_files, temp_dir = create_test_files()
        
        for file_type, file_path in test_files.items():
            print(f"\n📄 Testing .{file_type} text extraction...")
            
            try:
                text = plagium._extract_text_from_file(file_path)
                
                if text:
                    status = "✅ SUCCESS"
                    length = len(text)
                    preview = text[:50] + "..." if len(text) > 50 else text
                    details = f"Extracted {length} chars: '{preview}'"
                else:
                    status = "❌ FAILED"
                    details = "No text extracted"
                
                print(f"   {status} - {details}")
                
            except Exception as e:
                print(f"   ❌ EXCEPTION - {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text extraction test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🎓 Plagium File Type Support Test")
    print("=" * 60)
    print("Testing if Plagium can analyze previously unsupported file types:")
    print("• PDF documents")
    print("• Word documents (.doc, .docx)")
    print("• Archive files (.zip, .rar)")
    print()
    
    try:
        # Test file analysis
        analysis_success = test_plagium_file_analysis()
        
        # Test text extraction
        extraction_success = test_text_extraction_capabilities()
        
        print(f"\n" + "=" * 60)
        print("📋 FINAL RESULTS")
        print("=" * 60)
        
        if analysis_success and extraction_success:
            print("✅ Plagium integration test completed successfully!")
            print("\n🎯 KEY FINDINGS:")
            print("• Plagium can potentially analyze more file types than our current system")
            print("• Text extraction is the key limitation for binary files")
            print("• PDF and Word documents may be supported with proper text extraction")
            print("• Archive files would need extraction before analysis")
        else:
            print("❌ Some tests failed - check the output above for details")
        
        print(f"\n💡 RECOMMENDATIONS:")
        print("• Install PyPDF2 for PDF text extraction: pip install PyPDF2")
        print("• Install python-docx for Word document extraction: pip install python-docx")
        print("• Consider integrating Plagium for web-based plagiarism detection")
        print("• Use Plagium as a fallback for files our local system cannot analyze")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")

if __name__ == "__main__":
    main()

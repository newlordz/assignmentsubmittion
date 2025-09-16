#!/usr/bin/env python3
"""
Plagium Integration Module
Integrates the Plagium npm package for web-based plagiarism detection.
"""

import subprocess
import os
import json
import logging
import tempfile
import shutil
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

class PlagiumIntegration:
    """
    Integration with Plagium npm package for web-based plagiarism detection.
    Plagium uses Google Search API to detect plagiarism in text content.
    """
    
    def __init__(self, node_modules_path: str = "node_modules"):
        self.node_modules_path = node_modules_path
        self.plagium_path = os.path.join(node_modules_path, "plagium")
        self._is_available = self._check_plagium_availability()
        
    def _check_plagium_availability(self) -> bool:
        """Check if Node.js and Plagium are available."""
        try:
            # Check for Node.js
            subprocess.run(["node", "--version"], check=True, capture_output=True)
            logger.info("Node.js is available")
            
            # Check if Plagium is installed
            if os.path.exists(self.plagium_path):
                logger.info("Plagium package found")
                return True
            else:
                logger.warning("Plagium package not found. Will attempt to install.")
                return self._install_plagium()
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("Node.js not found. Plagium integration will not be available.")
            return False
    
    def _install_plagium(self) -> bool:
        """Install Plagium npm package."""
        try:
            logger.info("Installing Plagium package...")
            result = subprocess.run(
                ["npm", "install", "plagium"],
                capture_output=True,
                text=True,
                check=True
            )
            logger.info("Plagium package installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install Plagium: {e.stderr}")
            return False
        except Exception as e:
            logger.error(f"Error installing Plagium: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if Plagium integration is available."""
        return self._is_available
    
    def _extract_text_from_file(self, file_path: str) -> Optional[str]:
        """
        Extract text content from various file types.
        This is a basic implementation - in production, you'd want more robust text extraction.
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.txt':
                # Plain text files
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            
            elif file_extension in ['.pdf']:
                # For PDF files, we'll need a PDF text extraction library
                # This is a placeholder - you'd need to install PyPDF2 or similar
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        pdf_reader = PyPDF2.PdfReader(f)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() + "\n"
                        return text.strip()
                except ImportError:
                    logger.warning("PyPDF2 not available for PDF text extraction")
                    return None
                except Exception as e:
                    logger.error(f"Error extracting text from PDF: {e}")
                    return None
            
            elif file_extension in ['.doc', '.docx']:
                # For Word documents, we'd need python-docx
                try:
                    from docx import Document
                    doc = Document(file_path)
                    text = ""
                    for paragraph in doc.paragraphs:
                        text += paragraph.text + "\n"
                    return text.strip()
                except ImportError:
                    logger.warning("python-docx not available for Word document text extraction")
                    return None
                except Exception as e:
                    logger.error(f"Error extracting text from Word document: {e}")
                    return None
            
            elif file_extension in ['.zip', '.rar']:
                # For archive files, we'd need to extract and analyze contents
                logger.warning("Archive file analysis not implemented yet")
                return None
            
            else:
                # Try to read as text
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
                    
        except Exception as e:
            logger.error(f"Error extracting text from file {file_path}: {e}")
            return None
    
    def analyze_text(self, text: str, language_code: str = "en", 
                    google_api_key: str = None, google_engine_id: str = None) -> Dict[str, Any]:
        """
        Analyze text for plagiarism using Plagium.
        
        Args:
            text: Text content to analyze
            language_code: Language code (default: "en")
            google_api_key: Google API key (optional)
            google_engine_id: Google Custom Search Engine ID (optional)
            
        Returns:
            Analysis results with plagiarism score and details
        """
        if not self.is_available():
            return {
                "error": "Plagium not available",
                "fallback": "Use local plagiarism detection instead"
            }
        
        if not text or len(text.strip()) < 10:
            return {
                "error": "Text too short for analysis",
                "score": 0.0
            }
        
        try:
            # Create a temporary Node.js script to use Plagium
            script_content = f"""
const {{ getPlagiarismScore }} = require('plagium');

async function analyzeText() {{
    try {{
        const score = await getPlagiarismScore({{
            text: `{text.replace('`', '\\`')}`,
            languageCode: '{language_code}',
            googleApiKey: '{google_api_key or ""}',
            googleEngineId: '{google_engine_id or ""}'
        }});
        
        console.log(JSON.stringify({{
            success: true,
            score: score,
            percentage: Math.round(score * 100),
            message: "Analysis completed successfully"
        }}));
    }} catch (error) {{
        console.log(JSON.stringify({{
            success: false,
            error: error.message,
            score: 0.0
        }}));
    }}
}}

analyzeText();
"""
            
            # Write script to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            try:
                # Run the Node.js script
                result = subprocess.run(
                    ["node", script_path],
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout
                )
                
                if result.returncode == 0:
                    # Parse the JSON output
                    output = json.loads(result.stdout.strip())
                    if output.get("success"):
                        return {
                            "success": True,
                            "score": output.get("score", 0.0),
                            "percentage": output.get("percentage", 0),
                            "message": output.get("message", "Analysis completed"),
                            "method": "Plagium (Google Search)"
                        }
                    else:
                        return {
                            "error": output.get("error", "Unknown error"),
                            "score": 0.0
                        }
                else:
                    return {
                        "error": f"Plagium execution failed: {result.stderr}",
                        "score": 0.0
                    }
                    
            finally:
                # Clean up temporary script
                if os.path.exists(script_path):
                    os.unlink(script_path)
                    
        except subprocess.TimeoutExpired:
            return {
                "error": "Plagium analysis timed out",
                "score": 0.0
            }
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON output from Plagium",
                "score": 0.0
            }
        except Exception as e:
            logger.error(f"Error running Plagium analysis: {e}")
            return {
                "error": f"Plagium analysis failed: {str(e)}",
                "score": 0.0
            }
    
    def analyze_file(self, file_path: str, language_code: str = "en",
                    google_api_key: str = None, google_engine_id: str = None) -> Dict[str, Any]:
        """
        Analyze a file for plagiarism using Plagium.
        
        Args:
            file_path: Path to the file to analyze
            language_code: Language code (default: "en")
            google_api_key: Google API key (optional)
            google_engine_id: Google Custom Search Engine ID (optional)
            
        Returns:
            Analysis results with plagiarism score and details
        """
        if not self.is_available():
            return {
                "error": "Plagium not available",
                "fallback": "Use local plagiarism detection instead"
            }
        
        if not os.path.exists(file_path):
            return {
                "error": f"File not found: {file_path}",
                "score": 0.0
            }
        
        # Extract text from file
        text = self._extract_text_from_file(file_path)
        
        if not text:
            return {
                "error": f"Could not extract text from file: {file_path}",
                "score": 0.0
            }
        
        # Analyze the extracted text
        return self.analyze_text(text, language_code, google_api_key, google_engine_id)
    
    def get_supported_file_types(self) -> List[str]:
        """Get list of file types that can be analyzed."""
        return [
            # Text files (direct support)
            "txt", "md", "rst", "tex", "latex", "rtf",
            
            # Code files (direct support)
            "py", "js", "java", "c", "cpp", "cs", "go", "rs", "php", "rb",
            "scala", "kt", "swift", "r", "sql", "html", "css", "sh", "ps1", "ts",
            "jsx", "tsx", "vue", "svelte",
            
            # Document files (with text extraction)
            "pdf", "doc", "docx", "odt",
            
            # Note: Archive files would need extraction first
            # "zip", "rar", "7z", "tar", "gz"
        ]
    
    def get_requirements(self) -> Dict[str, Any]:
        """Get system requirements for Plagium integration."""
        return {
            "nodejs": "Required for running Plagium",
            "npm": "Required for installing Plagium package",
            "plagium": "npm package for plagiarism detection",
            "optional": {
                "PyPDF2": "For PDF text extraction",
                "python-docx": "For Word document text extraction",
                "google_api_key": "For enhanced Google Search API access",
                "google_engine_id": "For custom Google Search Engine"
            }
        }

def test_plagium_integration():
    """Test the Plagium integration."""
    print("🧪 Testing Plagium Integration")
    print("=" * 50)
    
    plagium = PlagiumIntegration()
    
    if not plagium.is_available():
        print("❌ Plagium integration not available")
        print("Requirements:")
        for req, desc in plagium.get_requirements().items():
            print(f"  • {req}: {desc}")
        return False
    
    print("✅ Plagium integration is available")
    
    # Test with sample text
    sample_text = """
    This is a sample text for testing plagiarism detection.
    It contains some unique content that should be analyzed.
    The system will search for similar content on the web.
    """
    
    print(f"\n📝 Testing text analysis...")
    result = plagium.analyze_text(sample_text)
    
    if "error" in result:
        print(f"❌ Text analysis failed: {result['error']}")
    else:
        print(f"✅ Text analysis successful")
        print(f"   Score: {result.get('score', 0.0):.2f}")
        print(f"   Percentage: {result.get('percentage', 0)}%")
        print(f"   Method: {result.get('method', 'Unknown')}")
    
    # Test supported file types
    print(f"\n📁 Supported file types:")
    supported_types = plagium.get_supported_file_types()
    for file_type in supported_types:
        print(f"   • .{file_type}")
    
    return True

if __name__ == "__main__":
    test_plagium_integration()

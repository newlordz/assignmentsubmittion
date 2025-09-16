#!/usr/bin/env python3
"""
Dolos Integration for E-Assignment System
This module provides Python integration with the Dolos plagiarism detection tool.
"""

import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DolosIntegration:
    """
    Python wrapper for Dolos plagiarism detection tool.
    Integrates with the E-Assignment System to provide advanced code plagiarism detection.
    """
    
    def __init__(self, dolos_path: str = None):
        """
        Initialize Dolos integration.
        
        Args:
            dolos_path: Path to the Dolos installation directory
        """
        self.dolos_path = dolos_path or os.path.join(os.getcwd(), "dolos-main")
        self.temp_dir = None
        self.node_available = self._check_node_availability()
        
    def _check_node_availability(self) -> bool:
        """Check if Node.js is available on the system."""
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                logger.info(f"Node.js available: {result.stdout.strip()}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        logger.warning("Node.js not found. Dolos integration will not be available.")
        return False
    
    def _check_dolos_installation(self) -> bool:
        """Check if Dolos is properly installed."""
        if not os.path.exists(self.dolos_path):
            logger.error(f"Dolos path not found: {self.dolos_path}")
            return False
            
        package_json = os.path.join(self.dolos_path, "package.json")
        if not os.path.exists(package_json):
            logger.error(f"Dolos package.json not found: {package_json}")
            return False
            
        return True
    
    def _install_dolos_dependencies(self) -> bool:
        """Install Dolos dependencies using npm."""
        if not self.node_available:
            logger.error("Node.js not available. Cannot install Dolos dependencies.")
            return False
            
        try:
            logger.info("Installing Dolos dependencies...")
            result = subprocess.run(
                ['npm', 'install'],
                cwd=self.dolos_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info("Dolos dependencies installed successfully")
                return True
            else:
                logger.error(f"Failed to install Dolos dependencies: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("Timeout while installing Dolos dependencies")
            return False
        except Exception as e:
            logger.error(f"Error installing Dolos dependencies: {e}")
            return False
    
    def _prepare_files_for_analysis(self, submissions: List[Dict[str, Any]]) -> Tuple[str, List[str]]:
        """
        Prepare submission files for Dolos analysis.
        
        Args:
            submissions: List of submission dictionaries with 'content' and 'id' keys
            
        Returns:
            Tuple of (temp_directory_path, list_of_file_paths)
        """
        # Create temporary directory
        self.temp_dir = tempfile.mkdtemp(prefix="dolos_analysis_")
        file_paths = []
        
        for i, submission in enumerate(submissions):
            content = submission.get('content', '')
            submission_id = submission.get('id', f'submission_{i}')
            
            if not content.strip():
                continue
                
            # Determine file extension based on content
            file_ext = self._detect_file_extension(content)
            filename = f"{submission_id}{file_ext}"
            file_path = os.path.join(self.temp_dir, filename)
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                file_paths.append(file_path)
                logger.info(f"Created file: {filename}")
            except Exception as e:
                logger.error(f"Error creating file {filename}: {e}")
        
        return self.temp_dir, file_paths
    
    def _detect_file_extension(self, content: str) -> str:
        """
        Detect file extension based on content.
        
        Args:
            content: File content to analyze
            
        Returns:
            Appropriate file extension
        """
        content_lower = content.lower().strip()
        
        # Python detection
        if any(keyword in content_lower for keyword in ['def ', 'import ', 'from ', 'class ', 'if __name__']):
            return '.py'
        
        # JavaScript detection
        if any(keyword in content_lower for keyword in ['function ', 'const ', 'let ', 'var ', 'console.log']):
            return '.js'
        
        # Java detection
        if any(keyword in content_lower for keyword in ['public class', 'public static void main', 'import java']):
            return '.java'
        
        # C/C++ detection
        if any(keyword in content_lower for keyword in ['#include', 'int main', 'printf', 'cout']):
            if '#include <iostream>' in content_lower or 'using namespace std' in content_lower:
                return '.cpp'
            return '.c'
        
        # HTML detection
        if content_lower.startswith('<html') or '<!doctype html' in content_lower:
            return '.html'
        
        # CSS detection
        if '{' in content and '}' in content and ':' in content:
            return '.css'
        
        # SQL detection
        if any(keyword in content_lower for keyword in ['select ', 'insert ', 'update ', 'delete ', 'create table']):
            return '.sql'
        
        # Default to text file
        return '.txt'
    
    def _run_dolos_analysis(self, file_paths: List[str], language: str = None) -> Dict[str, Any]:
        """
        Run Dolos analysis on the prepared files.
        
        Args:
            file_paths: List of file paths to analyze
            language: Programming language (optional, auto-detect if None)
            
        Returns:
            Analysis results dictionary
        """
        if not self.node_available:
            raise RuntimeError("Node.js not available")
        
        if len(file_paths) < 2:
            raise ValueError("Need at least 2 files for plagiarism analysis")
        
        # Build Dolos command
        cmd = ['node', os.path.join(self.dolos_path, 'cli', 'dist', 'cli.js'), 'run']
        
        # Add language if specified
        if language:
            cmd.extend(['--language', language])
        
        # Add output format (JSON for programmatic use)
        cmd.extend(['--format', 'json'])
        
        # Add file paths
        cmd.extend(file_paths)
        
        try:
            logger.info(f"Running Dolos analysis: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                try:
                    # Parse JSON output
                    analysis_result = json.loads(result.stdout)
                    logger.info("Dolos analysis completed successfully")
                    return analysis_result
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Dolos JSON output: {e}")
                    logger.error(f"Raw output: {result.stdout}")
                    return {"error": "Failed to parse analysis results"}
            else:
                logger.error(f"Dolos analysis failed: {result.stderr}")
                return {"error": f"Dolos analysis failed: {result.stderr}"}
                
        except subprocess.TimeoutExpired:
            logger.error("Dolos analysis timed out")
            return {"error": "Analysis timed out"}
        except Exception as e:
            logger.error(f"Error running Dolos analysis: {e}")
            return {"error": f"Analysis error: {e}"}
    
    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info("Cleaned up temporary files")
            except Exception as e:
                logger.error(f"Error cleaning up temporary files: {e}")
    
    def analyze_submissions(self, submissions: List[Dict[str, Any]], language: str = None) -> Dict[str, Any]:
        """
        Analyze submissions for plagiarism using Dolos.
        
        Args:
            submissions: List of submission dictionaries with 'content' and 'id' keys
            language: Programming language (optional, auto-detect if None)
            
        Returns:
            Analysis results with plagiarism scores and details
        """
        if not self.node_available:
            return {
                "error": "Node.js not available",
                "fallback": "Use local plagiarism detection instead"
            }
        
        if not self._check_dolos_installation():
            return {
                "error": "Dolos not properly installed",
                "fallback": "Use local plagiarism detection instead"
            }
        
        try:
            # Prepare files for analysis
            temp_dir, file_paths = self._prepare_files_for_analysis(submissions)
            
            if len(file_paths) < 2:
                return {
                    "error": "Need at least 2 valid submissions for analysis",
                    "fallback": "Use local plagiarism detection instead"
                }
            
            # Run Dolos analysis
            analysis_result = self._run_dolos_analysis(file_paths, language)
            
            # Process results
            processed_result = self._process_dolos_results(analysis_result, submissions)
            
            return processed_result
            
        except Exception as e:
            logger.error(f"Error in Dolos analysis: {e}")
            return {
                "error": f"Analysis failed: {e}",
                "fallback": "Use local plagiarism detection instead"
            }
        finally:
            self._cleanup_temp_files()
    
    def _process_dolos_results(self, dolos_result: Dict[str, Any], submissions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process Dolos results into a format compatible with the E-Assignment System.
        
        Args:
            dolos_result: Raw Dolos analysis results
            submissions: Original submission data
            
        Returns:
            Processed results with plagiarism scores
        """
        if "error" in dolos_result:
            return dolos_result
        
        try:
            # Extract plagiarism information from Dolos results
            plagiarism_scores = {}
            similarity_details = {}
            
            # Process pairs of similar files
            if "pairs" in dolos_result:
                for pair in dolos_result["pairs"]:
                    file1 = pair.get("file1", {}).get("path", "")
                    file2 = pair.get("file2", {}).get("path", "")
                    similarity = pair.get("similarity", 0.0)
                    
                    # Extract submission IDs from file paths
                    sub1_id = self._extract_submission_id(file1)
                    sub2_id = self._extract_submission_id(file2)
                    
                    if sub1_id and sub2_id:
                        # Store similarity score
                        key = f"{sub1_id}_{sub2_id}"
                        similarity_details[key] = {
                            "submission1": sub1_id,
                            "submission2": sub2_id,
                            "similarity": similarity,
                            "details": pair
                        }
                        
                        # Update individual plagiarism scores
                        plagiarism_scores[sub1_id] = max(plagiarism_scores.get(sub1_id, 0.0), similarity)
                        plagiarism_scores[sub2_id] = max(plagiarism_scores.get(sub2_id, 0.0), similarity)
            
            return {
                "method": "dolos",
                "plagiarism_scores": plagiarism_scores,
                "similarity_details": similarity_details,
                "total_submissions": len(submissions),
                "analyzed_files": len([s for s in submissions if s.get('content', '').strip()]),
                "raw_results": dolos_result
            }
            
        except Exception as e:
            logger.error(f"Error processing Dolos results: {e}")
            return {
                "error": f"Failed to process results: {e}",
                "fallback": "Use local plagiarism detection instead"
            }
    
    def _extract_submission_id(self, file_path: str) -> Optional[str]:
        """Extract submission ID from file path."""
        try:
            filename = os.path.basename(file_path)
            # Remove file extension
            submission_id = os.path.splitext(filename)[0]
            return submission_id
        except:
            return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return [
            "javascript", "typescript", "python", "java", "c", "cpp", "csharp",
            "go", "rust", "php", "ruby", "scala", "kotlin", "swift", "r",
            "sql", "html", "css", "bash", "powershell"
        ]
    
    def is_available(self) -> bool:
        """Check if Dolos integration is available."""
        return self.node_available and self._check_dolos_installation()


def test_dolos_integration():
    """Test function for Dolos integration."""
    print("🧪 Testing Dolos Integration...")
    
    # Initialize Dolos integration
    dolos = DolosIntegration()
    
    # Check availability
    if not dolos.is_available():
        print("❌ Dolos integration not available")
        print("Requirements:")
        print("- Node.js must be installed")
        print("- Dolos must be properly set up")
        return False
    
    print("✅ Dolos integration is available")
    
    # Test with sample submissions
    sample_submissions = [
        {
            "id": "student1",
            "content": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        },
        {
            "id": "student2", 
            "content": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))
"""
        },
        {
            "id": "student3",
            "content": """
def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fib(10))
"""
        }
    ]
    
    print("🔍 Running plagiarism analysis...")
    results = dolos.analyze_submissions(sample_submissions, language="python")
    
    if "error" in results:
        print(f"❌ Analysis failed: {results['error']}")
        return False
    
    print("✅ Analysis completed successfully")
    print(f"📊 Results: {json.dumps(results, indent=2)}")
    
    return True


if __name__ == "__main__":
    test_dolos_integration()

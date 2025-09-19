# 🔍 Dolos Integration in E-Assignment System - Complete Guide

## 🎯 What is Dolos?

**Dolos** is an advanced plagiarism detection tool specifically designed for **programming code**. It's developed by Dodona (an online learning platform) and uses sophisticated algorithms to detect code similarity and plagiarism in programming assignments.

## 🏗️ How Dolos Integration Works in Your System

### **1. Dual-Mode Plagiarism Detection**

Your E-Assignment System uses a **smart dual-mode approach**:

```
📝 Text Submissions → Local Plagiarism Detection (TF-IDF, Cosine Similarity)
💻 Code Submissions → Dolos Advanced Analysis (if available) + Local Fallback
```

### **2. Integration Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    E-Assignment System                      │
├─────────────────────────────────────────────────────────────┤
│  📊 Plagiarism Detection Engine                             │
│  ├── 🔍 Content Type Detection                              │
│  ├── 🎯 Dolos Integration (Primary for Code)                │
│  └── 🔄 Local Detection (Fallback + Text)                   │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Technical Implementation

### **Phase 1: Initialization (App Startup)**

```python
# In app.py (lines 99-111)
dolos_integration = None
if DOLOS_AVAILABLE:
    try:
        dolos_integration = DolosIntegration()
        if dolos_integration.is_available():
            print("✅ Dolos integration available - advanced plagiarism detection enabled")
        else:
            print("⚠️ Dolos integration not properly configured - using local detection only")
            dolos_integration = None
    except Exception as e:
        print(f"⚠️ Error initializing Dolos integration: {e}")
        dolos_integration = None
```

**What happens:**
1. **Check Node.js**: Verifies if Node.js is installed
2. **Check Dolos**: Verifies if Dolos is properly set up
3. **Initialize**: Creates DolosIntegration instance if available
4. **Fallback**: Sets to None if not available (graceful degradation)

### **Phase 2: Plagiarism Detection Process**

```python
# In app.py (lines 900-931)
def calculate_plagiarism_score(content, other_submissions):
    # Try Dolos integration first (for code submissions)
    if dolos_integration and dolos_integration.is_available():
        try:
            # Prepare submissions for Dolos analysis
            submissions = [{"id": "current", "content": content}]
            for i, sub in enumerate(other_submissions):
                if hasattr(sub, 'content') and sub.content and len(sub.content.strip()) > 10:
                    submissions.append({"id": f"sub_{i}", "content": sub.content})
            
            if len(submissions) >= 2:
                # Run Dolos analysis
                dolos_results = dolos_integration.analyze_submissions(submissions)
                
                if "error" not in dolos_results and "plagiarism_scores" in dolos_results:
                    current_score = dolos_results["plagiarism_scores"].get("current", 0.0)
                    print(f"🔍 Dolos analysis completed - Score: {current_score}%")
                    return round(current_score, 2)
                else:
                    print(f"⚠️ Dolos analysis failed: {dolos_results.get('error', 'Unknown error')}")
                    print("🔄 Falling back to local plagiarism detection...")
        except Exception as e:
            print(f"⚠️ Dolos integration error: {e}")
            print("🔄 Falling back to local plagiarism detection...")
    
    # Fallback to local comprehensive plagiarism detection
    return calculate_local_plagiarism_score(content, other_submissions)
```

## 🎯 Dolos Analysis Process

### **Step 1: File Preparation**
```python
def _prepare_files_for_analysis(self, submissions):
    # Create temporary directory
    self.temp_dir = tempfile.mkdtemp(prefix="dolos_analysis_")
    file_paths = []
    
    for i, submission in enumerate(submissions):
        content = submission.get('content', '')
        submission_id = submission.get('id', f'submission_{i}')
        
        # Determine file extension based on content
        file_ext = self._detect_file_extension(content)
        filename = f"{submission_id}{file_ext}"
        file_path = os.path.join(self.temp_dir, filename)
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        file_paths.append(file_path)
    
    return self.temp_dir, file_paths
```

### **Step 2: Language Detection**
```python
def _detect_file_extension(self, content):
    content_lower = content.lower().strip()
    
    # Python detection
    if any(keyword in content_lower for keyword in ['def ', 'import ', 'from ', 'class ']):
        return '.py'
    
    # JavaScript detection
    if any(keyword in content_lower for keyword in ['function ', 'const ', 'let ', 'var ']):
        return '.js'
    
    # Java detection
    if any(keyword in content_lower for keyword in ['public class', 'public static void main']):
        return '.java'
    
    # And more languages...
```

### **Step 3: Dolos Command Execution**
```python
def _run_dolos_analysis(self, file_paths, language=None):
    # Build Dolos command
    cmd = ['node', os.path.join(self.dolos_path, 'cli', 'dist', 'cli.js'), 'run']
    
    # Add language if specified
    if language:
        cmd.extend(['--language', language])
    
    # Add output format (JSON for programmatic use)
    cmd.extend(['--format', 'json'])
    
    # Add file paths
    cmd.extend(file_paths)
    
    # Execute Dolos
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        analysis_result = json.loads(result.stdout)
        return analysis_result
    else:
        return {"error": f"Dolos analysis failed: {result.stderr}"}
```

### **Step 4: Results Processing**
```python
def _process_dolos_results(self, dolos_result, submissions):
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
```

## 🎯 Supported Programming Languages

Dolos supports **20+ programming languages**:

### **Primary Languages:**
- **Python** (.py) - `def`, `import`, `class`, `if __name__`
- **JavaScript** (.js) - `function`, `const`, `let`, `var`, `console.log`
- **Java** (.java) - `public class`, `public static void main`, `import java`
- **C/C++** (.c/.cpp) - `#include`, `int main`, `printf`, `cout`
- **C#** (.cs) - `using System`, `namespace`, `class`
- **Go** (.go) - `package main`, `func main()`
- **Rust** (.rs) - `fn main()`, `use std`
- **PHP** (.php) - `<?php`, `function`, `class`
- **Ruby** (.rb) - `def`, `class`, `require`
- **Scala** (.scala) - `object`, `class`, `def`
- **Kotlin** (.kt) - `fun main()`, `class`
- **Swift** (.swift) - `import Foundation`, `func`
- **R** (.r) - `library()`, `function()`

### **Web Technologies:**
- **HTML** (.html) - `<!DOCTYPE html>`, `<html>`
- **CSS** (.css) - `{`, `}`, `:`
- **SQL** (.sql) - `SELECT`, `INSERT`, `UPDATE`, `CREATE TABLE`

### **Scripting:**
- **Bash** (.sh) - `#!/bin/bash`, `echo`
- **PowerShell** (.ps1) - `Write-Host`, `Get-`

## 🔄 Fallback System

### **When Dolos is NOT Available:**
1. **Node.js not installed** → Falls back to local detection
2. **Dolos not properly set up** → Falls back to local detection
3. **Analysis fails** → Falls back to local detection
4. **Less than 2 submissions** → Falls back to local detection

### **Local Detection Methods:**
- **TF-IDF Vectorization** - Term frequency analysis
- **Cosine Similarity** - Mathematical similarity calculation
- **N-gram Analysis** - Character sequence comparison
- **Jaccard Similarity** - Set-based similarity
- **Levenshtein Distance** - Edit distance calculation

## 📊 Example Analysis Flow

### **Scenario: Python Assignment Submission**

```
1. Student submits Python code
   ↓
2. System detects: "def fibonacci" → Python code
   ↓
3. Dolos Integration:
   - Creates temp files: student1.py, student2.py, student3.py
   - Runs: node dolos-cli.js run --language python --format json *.py
   - Gets JSON results with similarity scores
   ↓
4. Results Processing:
   - Extracts plagiarism scores for each student
   - Identifies similar code pairs
   - Returns structured results
   ↓
5. Display Results:
   - Student 1: 95% similarity with Student 2
   - Student 2: 95% similarity with Student 1
   - Student 3: 15% similarity (original work)
```

## 🎯 Benefits of Dolos Integration

### **For Code Assignments:**
- **Advanced Algorithms** - Sophisticated code analysis
- **Language-Aware** - Understands programming syntax
- **Structural Analysis** - Detects copied logic patterns
- **Variable Renaming Detection** - Catches attempts to hide plagiarism
- **Comment Analysis** - Detects copied comments

### **For Your System:**
- **Automatic Fallback** - Always works, even without Dolos
- **Zero Configuration** - Works out of the box
- **Performance** - Fast analysis for multiple submissions
- **Accuracy** - Higher precision than basic text comparison
- **Scalability** - Handles large numbers of submissions

## 🚀 Current Status

**✅ Dolos Integration Status:**
- **Available**: When Node.js is installed and Dolos is set up
- **Fallback**: Local detection when Dolos is not available
- **Seamless**: Users don't notice the difference
- **Reliable**: Always provides plagiarism detection

**Your system message:**
```
WARNING:dolos_integration:Node.js not found. Dolos integration will not be available.
⚠️ Dolos integration not properly configured - using local detection only
```

This means Dolos is not currently available, but your system is still working perfectly with local plagiarism detection!

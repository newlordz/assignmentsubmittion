# 📁 Plagiarism Detection - Supported File Types

## 🎯 **Overview**

The E-Assignment System's plagiarism detection can process different types of files with varying levels of analysis capability. Here's a comprehensive breakdown:

---

## ✅ **FULLY SUPPORTED (Text-Based Analysis)**

### **📝 Text Files**
- **`.txt`** - Plain text files
- **`.py`** - Python code files
- **`.js`** - JavaScript files
- **`.java`** - Java source files
- **`.c`** - C source files
- **`.cpp`** - C++ source files
- **`.cs`** - C# source files
- **`.go`** - Go source files
- **`.rs`** - Rust source files
- **`.php`** - PHP files
- **`.rb`** - Ruby files
- **`.scala`** - Scala files
- **`.kt`** - Kotlin files
- **`.swift`** - Swift files
- **`.r`** - R script files
- **`.sql`** - SQL script files
- **`.html`** - HTML files
- **`.css`** - CSS files
- **`.sh`** - Bash shell scripts
- **`.ps1`** - PowerShell scripts
- **`.ts`** - TypeScript files
- **`.jsx`** - React JSX files
- **`.tsx`** - TypeScript JSX files
- **`.vue`** - Vue.js files
- **`.svelte`** - Svelte files

### **📊 Analysis Capabilities:**
- ✅ **Full Content Analysis** - Complete text content is analyzed
- ✅ **Dolos Integration** - Advanced code plagiarism detection (if Node.js available)
- ✅ **Local Detection** - 5-method local plagiarism detection
- ✅ **Language Detection** - Automatic programming language detection
- ✅ **Similarity Scoring** - Detailed similarity analysis

---

## ⚠️ **PARTIALLY SUPPORTED (Limited Analysis)**

### **📄 Document Files**
- **`.pdf`** - PDF documents
- **`.doc`** - Microsoft Word documents (legacy)
- **`.docx`** - Microsoft Word documents
- **`.ppt`** - Microsoft PowerPoint presentations (legacy)
- **`.pptx`** - Microsoft PowerPoint presentations

### **📦 Archive Files**
- **`.zip`** - ZIP archives
- **`.rar`** - RAR archives

### **📊 Analysis Capabilities:**
- ❌ **Content Analysis** - Cannot extract text content
- ⚠️ **File Detection** - System detects file type but cannot analyze
- 📝 **Status Message** - Shows "Binary file detected" or "Archive file detected"
- 🔄 **Fallback** - Plagiarism score set to 0.0

---

## 🚫 **NOT SUPPORTED**

### **🖼️ Media Files**
- **`.jpg`, `.jpeg`** - Image files
- **`.png`** - PNG images
- **`.gif`** - GIF images
- **`.mp4`** - Video files
- **`.mp3`** - Audio files
- **`.wav`** - Audio files

### **💾 Binary Files**
- **`.exe`** - Executable files
- **`.dll`** - Dynamic link libraries
- **`.so`** - Shared object files
- **`.bin`** - Binary data files

### **📊 Analysis Capabilities:**
- ❌ **Upload Blocked** - These files are not allowed for upload
- 🚫 **No Analysis** - Cannot be processed by plagiarism detection

---

## 🔍 **Detection Methods by File Type**

### **For Code Files (Dolos Integration)**
When Node.js is available, the system uses **Dolos** for advanced analysis:

#### **Supported Programming Languages:**
```python
[
    "javascript", "typescript", "python", "java", "c", "cpp", "csharp",
    "go", "rust", "php", "ruby", "scala", "kotlin", "swift", "r",
    "sql", "html", "css", "bash", "powershell"
]
```

#### **Dolos Analysis Features:**
- ✅ **Fingerprint Analysis** - Advanced code fingerprinting
- ✅ **Token Matching** - Syntax-aware token comparison
- ✅ **Structure Analysis** - Code structure similarity
- ✅ **Fragment Detection** - Identifies copied code blocks
- ✅ **Multi-language Support** - 20+ programming languages

### **For Text Files (Local Detection)**
When Dolos is not available, the system uses **5-method local detection**:

#### **Local Analysis Methods:**
1. **TF-IDF Similarity** - Term frequency analysis
2. **Semantic Similarity** - Word context analysis
3. **Content Fingerprinting** - Document fingerprinting
4. **Phrase Matching** - Exact phrase detection
5. **Structure Similarity** - Document structure analysis

---

## 📋 **File Upload Configuration**

### **Allowed Extensions (Current)**
```python
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar'
}
```

### **Recommended Extensions for Best Results**
```python
RECOMMENDED_EXTENSIONS = {
    # Text files (full analysis)
    'txt', 'py', 'js', 'java', 'c', 'cpp', 'cs', 'go', 'rs', 'php', 'rb',
    'scala', 'kt', 'swift', 'r', 'sql', 'html', 'css', 'sh', 'ps1', 'ts',
    'jsx', 'tsx', 'vue', 'svelte',
    
    # Documents (limited analysis)
    'pdf', 'doc', 'docx', 'ppt', 'pptx',
    
    # Archives (detection only)
    'zip', 'rar'
}
```

---

## 🎯 **Best Practices for Plagiarism Detection**

### **✅ Recommended File Types**
1. **Code Assignments**: Use `.py`, `.js`, `.java`, `.c`, `.cpp` files
2. **Text Assignments**: Use `.txt` files
3. **Web Assignments**: Use `.html`, `.css`, `.js` files
4. **Database Assignments**: Use `.sql` files

### **⚠️ Limited Support**
1. **Document Assignments**: `.pdf`, `.doc`, `.docx` (cannot analyze content)
2. **Presentation Assignments**: `.ppt`, `.pptx` (cannot analyze content)
3. **Archive Submissions**: `.zip`, `.rar` (cannot analyze content)

### **❌ Not Recommended**
1. **Media Files**: Images, videos, audio files
2. **Binary Files**: Executables, compiled code
3. **Encrypted Files**: Password-protected documents

---

## 🔧 **Technical Implementation**

### **File Content Reading**
```python
def read_file_content(file_path):
    file_extension = file_path.split('.')[-1].lower()
    
    if file_extension == 'txt':
        # Read text files directly
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    elif file_extension in ['pdf', 'doc', 'docx', 'ppt', 'pptx']:
        # Binary files - cannot analyze
        return f"Binary file detected ({file_extension.upper()}). Content analysis not available."
    
    elif file_extension in ['zip', 'rar']:
        # Archive files - cannot analyze
        return f"Archive file detected ({file_extension.upper()}). Content analysis not available."
    
    else:
        # Try to read as text with different encodings
        # Attempts UTF-8, Latin-1, CP1252, ISO-8859-1
        return attempt_text_reading(file_path)
```

### **Language Detection**
```python
def _detect_file_extension(content: str) -> str:
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
    
    # And so on for other languages...
```

---

## 📊 **Analysis Results by File Type**

### **Text Files (.txt, .py, .js, etc.)**
```
✅ Plagiarism Score: 85.5%
✅ Detailed Report: Available
✅ Similarity Analysis: Complete
✅ Code Structure: Analyzed
```

### **Binary Files (.pdf, .doc, .docx)**
```
⚠️ Plagiarism Score: 0.0%
⚠️ Detailed Report: "Binary file detected (PDF). Content analysis not available."
⚠️ Similarity Analysis: Skipped
⚠️ Code Structure: Not applicable
```

### **Archive Files (.zip, .rar)**
```
⚠️ Plagiarism Score: 0.0%
⚠️ Detailed Report: "Archive file detected (ZIP). Content analysis not available."
⚠️ Similarity Analysis: Skipped
⚠️ Code Structure: Not applicable
```

---

## 🚀 **Recommendations**

### **For Maximum Plagiarism Detection:**
1. **Use text-based file formats** (.txt, .py, .js, .java, etc.)
2. **Ensure files contain readable text content**
3. **Avoid binary or encrypted files**
4. **Use plain text for essays and reports**

### **For Code Assignments:**
1. **Submit source code files** (.py, .js, .java, .c, .cpp)
2. **Avoid compiled or executable files**
3. **Include all source files, not just executables**
4. **Use standard file extensions**

### **For Document Assignments:**
1. **Convert to plain text** (.txt) for best analysis
2. **Extract text from PDFs** before submission
3. **Avoid password-protected documents**
4. **Use simple formatting**

---

## 📞 **Support**

### **File Type Issues**
- **"Cannot analyze file"**: File is binary or unsupported format
- **"Content not readable"**: File encoding issues or corruption
- **"Archive detected"**: Extract files from archive and submit individually

### **Improving Detection**
- **Use text-based formats** for maximum compatibility
- **Ensure proper file encoding** (UTF-8 recommended)
- **Submit individual files** rather than archives
- **Use standard file extensions**

---

## 🎉 **Summary**

**✅ Best Support**: Text files, code files (.txt, .py, .js, .java, .c, .cpp, etc.)
**⚠️ Limited Support**: Document files (.pdf, .doc, .docx, .ppt, .pptx)
**❌ No Support**: Media files, binary files, executables

**For optimal plagiarism detection, use text-based file formats whenever possible!** 📁✨

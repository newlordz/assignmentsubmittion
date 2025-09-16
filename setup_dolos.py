#!/usr/bin/env python3
"""
Dolos Setup Script for E-Assignment System
This script sets up Dolos plagiarism detection integration.
"""

import os
import subprocess
import sys
import platform
import shutil
from pathlib import Path

def check_node_installation():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js found: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ Node.js not found")
    return False

def check_npm_installation():
    """Check if npm is installed."""
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ npm found: {version}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("❌ npm not found")
    return False

def install_node_dependencies():
    """Install Node.js dependencies for Dolos."""
    dolos_path = os.path.join(os.getcwd(), "dolos-main")
    
    if not os.path.exists(dolos_path):
        print(f"❌ Dolos directory not found: {dolos_path}")
        print("Please make sure you have downloaded and extracted Dolos to 'dolos-main' directory")
        return False
    
    print(f"📦 Installing Dolos dependencies in {dolos_path}...")
    
    try:
        # Install dependencies
        result = subprocess.run(
            ['npm', 'install'],
            cwd=dolos_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print("✅ Dolos dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install Dolos dependencies:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def build_dolos():
    """Build Dolos components."""
    dolos_path = os.path.join(os.getcwd(), "dolos-main")
    
    print("🔨 Building Dolos components...")
    
    try:
        # Build the project
        result = subprocess.run(
            ['npm', 'run', 'build'],
            cwd=dolos_path,
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        if result.returncode == 0:
            print("✅ Dolos build completed successfully")
            return True
        else:
            print(f"❌ Build failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out")
        return False
    except Exception as e:
        print(f"❌ Error building Dolos: {e}")
        return False

def test_dolos_integration():
    """Test Dolos integration."""
    print("🧪 Testing Dolos integration...")
    
    try:
        # Import and test the integration
        from dolos_integration import DolosIntegration
        
        dolos = DolosIntegration()
        
        if dolos.is_available():
            print("✅ Dolos integration is working correctly")
            return True
        else:
            print("❌ Dolos integration is not available")
            return False
            
    except ImportError as e:
        print(f"❌ Failed to import Dolos integration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing Dolos integration: {e}")
        return False

def provide_node_installation_instructions():
    """Provide instructions for installing Node.js."""
    system = platform.system().lower()
    
    print("\n📋 Node.js Installation Instructions:")
    print("=" * 50)
    
    if system == "windows":
        print("For Windows:")
        print("1. Go to https://nodejs.org/")
        print("2. Download the LTS version for Windows")
        print("3. Run the installer and follow the instructions")
        print("4. Make sure to check 'Add to PATH' during installation")
        print("5. Restart your command prompt/terminal")
        
    elif system == "darwin":  # macOS
        print("For macOS:")
        print("Option 1 - Using Homebrew:")
        print("  brew install node")
        print()
        print("Option 2 - Download from website:")
        print("1. Go to https://nodejs.org/")
        print("2. Download the LTS version for macOS")
        print("3. Run the installer")
        
    elif system == "linux":
        print("For Linux:")
        print("Option 1 - Using package manager (Ubuntu/Debian):")
        print("  sudo apt update")
        print("  sudo apt install nodejs npm")
        print()
        print("Option 2 - Using package manager (CentOS/RHEL):")
        print("  sudo yum install nodejs npm")
        print()
        print("Option 3 - Download from website:")
        print("1. Go to https://nodejs.org/")
        print("2. Download the LTS version for Linux")
        print("3. Extract and add to PATH")
    
    print("\nAfter installation, run this script again to continue setup.")

def main():
    """Main setup function."""
    print("🎓 Dolos Setup for E-Assignment System")
    print("=" * 50)
    print("This script will set up Dolos plagiarism detection integration.")
    print()
    
    # Check Node.js installation
    if not check_node_installation():
        provide_node_installation_instructions()
        return False
    
    # Check npm installation
    if not check_npm_installation():
        print("❌ npm is required but not found")
        return False
    
    # Install Dolos dependencies
    if not install_node_dependencies():
        print("❌ Failed to install Dolos dependencies")
        return False
    
    # Build Dolos
    if not build_dolos():
        print("❌ Failed to build Dolos")
        return False
    
    # Test integration
    if not test_dolos_integration():
        print("❌ Dolos integration test failed")
        return False
    
    print("\n🎉 Dolos setup completed successfully!")
    print("=" * 50)
    print("✅ Dolos plagiarism detection is now available in your E-Assignment System")
    print("✅ The system will automatically use Dolos for code plagiarism detection")
    print("✅ Local plagiarism detection remains as fallback")
    print()
    print("🚀 You can now run your E-Assignment System with advanced plagiarism detection!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Setup failed. Please check the error messages above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

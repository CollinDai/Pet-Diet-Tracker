#!/usr/bin/env python3
"""
Dependency checker for the Pet Food Consumption Monitor
"""

import sys
import subprocess

def check_module(module_name, import_name=None):
    """Check if a module can be imported."""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✅ {module_name}: OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name}: MISSING - {e}")
        return False

def check_dependencies():
    """Check all required dependencies."""
    print("Checking Pet Food Monitor dependencies...")
    print("=" * 50)
    
    dependencies = [
        ("Flask", "flask"),
        ("pytest", "pytest"),
        ("google-genai", "google.genai"),
        ("Pillow", "PIL"),
        ("picamera2", "picamera2"),
        ("python-dotenv", "dotenv"),
        ("numpy", "numpy")  # Usually installed with other packages
    ]
    
    missing = []
    for dep_name, import_name in dependencies:
        if not check_module(dep_name, import_name):
            missing.append(dep_name)
    
    print("\n" + "=" * 50)
    if missing:
        print(f"❌ {len(missing)} dependencies missing:")
        for dep in missing:
            print(f"   - {dep}")
        print("\nTo install missing dependencies:")
        print("pip install -r requirements.txt")
        print("\nOr install individually:")
        for dep in missing:
            print(f"pip install {dep}")
    else:
        print("✅ All dependencies are installed!")
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 7):
        print("⚠️  Warning: Python 3.7+ recommended")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not in virtual environment (recommended to use venv)")

if __name__ == "__main__":
    check_dependencies()
#!/usr/bin/env python3
"""
Michelin Star Recipe Generator
Installation script for dependencies
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install all required dependencies"""
    print("Installing dependencies for Michelin Star Recipe Generator...")
    
    # List of required packages
    packages = [
        "PyQt5>=5.15.0",
        "openai>=1.0.0",
        "keyring>=23.0.0",
        "pathlib>=1.0.1"
    ]
    
    # Install each package
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install it manually.")
    
    print("\nDependency installation complete!")
    print("You can now run the application with: python run.py")

if __name__ == "__main__":
    install_dependencies()
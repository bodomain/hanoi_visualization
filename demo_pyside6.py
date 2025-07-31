#!/usr/bin/env python3
"""
Demo script for the PySide6 port of Towers of Hanoi

This script demonstrates how to install and run the new PySide6 version
of the Towers of Hanoi visualization.
"""

import subprocess
import sys
import os

def install_pyside6():
    """Install PySide6 using pip"""
    print("Installing PySide6...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6>=6.5.0"])
        print("✓ PySide6 installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install PySide6: {e}")
        return False

def check_pyside6():
    """Check if PySide6 is available"""
    try:
        import PySide6
        print(f"✓ PySide6 version {PySide6.__version__} is available")
        return True
    except ImportError:
        print("✗ PySide6 not found")
        return False

def run_demo():
    """Run the PySide6 demo"""
    print("\\nStarting Towers of Hanoi PySide6 Demo...")
    try:
        # Add current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Import and run the application
        from ui.main_window import HanoiMainWindow
        from PySide6.QtWidgets import QApplication
        
        app = QApplication(sys.argv)
        app.setApplicationName("Towers of Hanoi - PySide6 Demo")
        
        window = HanoiMainWindow()
        window.show()
        
        print("✓ Application started successfully!")
        print("\\nFeatures in PySide6 version:")
        print("• Professional native GUI")
        print("• Menu bar and toolbar")
        print("• Speed control slider")
        print("• Status bar with progress info")
        print("• Keyboard shortcuts")
        print("• Modern dialog for disk selection")
        print("• Better performance and rendering")
        
        return app.exec()
        
    except Exception as e:
        print(f"✗ Failed to run demo: {e}")
        return 1

def main():
    """Main demo function"""
    print("=" * 60)
    print("Towers of Hanoi - PySide6 Port Demo")
    print("=" * 60)
    
    # Check if PySide6 is available
    if not check_pyside6():
        print("\\nPySide6 is required. Attempting to install...")
        if not install_pyside6():
            print("\\nPlease install PySide6 manually:")
            print("pip install PySide6")
            return 1
    
    # Run the demo
    return run_demo()

if __name__ == "__main__":
    sys.exit(main())

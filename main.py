#!/usr/bin/env python3
"""
Towers of Hanoi Visualization - PySide6 Version

A modern, interactive visualization of the classic Towers of Hanoi problem
using PySide6 for a professional GUI experience.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from ui.main_window import HanoiMainWindow


def main():
    """Main application entry point"""
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Towers of Hanoi")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Educational Software")
    
    # Set application properties
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    
    # Create and show the main window
    try:
        window = HanoiMainWindow()
        window.show()
        
        # Center the window on screen
        screen = app.primaryScreen().geometry()
        window_geometry = window.geometry()
        x = (screen.width() - window_geometry.width()) // 2
        y = (screen.height() - window_geometry.height()) // 2
        window.move(x, y)
        
    except Exception as e:
        print(f"Error creating main window: {e}")
        return 1
    
    # Run the application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

"""
Theme manager for the Towers of Hanoi application.
Handles switching between light and dark themes.
"""

import os
from PySide6.QtCore import QObject, Signal, QSettings
from PySide6.QtWidgets import QApplication


class ThemeManager(QObject):
    """Manages application themes and theme switching"""
    
    theme_changed = Signal(str)  # Emitted when theme changes
    
    LIGHT_THEME = "light"
    DARK_THEME = "dark"
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.current_theme = self.load_theme_preference()
        
    def load_theme_preference(self):
        """Load the saved theme preference"""
        return self.settings.value("theme", self.LIGHT_THEME)
        
    def save_theme_preference(self, theme):
        """Save the theme preference"""
        self.settings.setValue("theme", theme)
        self.settings.sync()
        
    def get_current_theme(self):
        """Get the current theme"""
        return self.current_theme
        
    def set_theme(self, theme):
        """Set and apply a theme"""
        if theme not in [self.LIGHT_THEME, self.DARK_THEME]:
            raise ValueError(f"Invalid theme: {theme}")
            
        if theme != self.current_theme:
            self.current_theme = theme
            self.save_theme_preference(theme)
            self.apply_theme()
            self.theme_changed.emit(theme)
            
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        new_theme = self.DARK_THEME if self.current_theme == self.LIGHT_THEME else self.LIGHT_THEME
        self.set_theme(new_theme)
        
    def apply_theme(self):
        """Apply the current theme to the application"""
        app = QApplication.instance()
        if app is None:
            return
            
        stylesheet = self.load_stylesheet(self.current_theme)
        app.setStyleSheet(stylesheet)
        
    def load_stylesheet(self, theme):
        """Load the stylesheet for the given theme"""
        try:
            # Get the directory where this file is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            resources_dir = os.path.join(os.path.dirname(current_dir), 'resources')
            
            if theme == self.DARK_THEME:
                style_path = os.path.join(resources_dir, 'dark_theme.qss')
            else:
                style_path = os.path.join(resources_dir, 'light_theme.qss')
                
            if os.path.exists(style_path):
                with open(style_path, 'r') as f:
                    return f.read()
            else:
                print(f"Warning: Theme file not found: {style_path}")
                return ""
                
        except Exception as e:
            print(f"Error loading stylesheet: {e}")
            return ""
            
    def get_theme_colors(self):
        """Get theme-specific colors for custom drawing"""
        if self.current_theme == self.DARK_THEME:
            return {
                'background': '#2b2b2b',
                'text': '#ffffff',
                'tower': '#666666',
                'disk_colors': [
                    '#ff6b6b',  # Red
                    '#4ecdc4',  # Teal
                    '#45b7d1',  # Blue
                    '#f9ca24',  # Yellow
                    '#f0932b',  # Orange
                    '#eb4d4b',  # Dark Red
                    '#6c5ce7',  # Purple
                    '#a29bfe',  # Light Purple
                ]
            }
        else:
            return {
                'background': '#ffffff',
                'text': '#000000',
                'tower': '#000000',
                'disk_colors': [
                    '#ff6b6b',  # Red
                    '#4ecdc4',  # Teal
                    '#45b7d1',  # Blue
                    '#f9ca24',  # Yellow
                    '#f0932b',  # Orange
                    '#eb4d4b',  # Dark Red
                    '#6c5ce7',  # Purple
                    '#a29bfe',  # Light Purple
                ]
            }

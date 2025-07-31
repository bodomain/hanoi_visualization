# Towers of Hanoi Visualization - PySide6 Port

A modern, professional visualization of the classic Towers of Hanoi problem, now ported from Pygame to PySide6 for a superior GUI experience.

## 🆕 What's New in the PySide6 Version

### Enhanced User Interface
- **Professional Native GUI**: Native look and feel on all platforms
- **Menu Bar**: File, View, and Help menus with standard shortcuts
- **Toolbar**: Quick access to common actions
- **Status Bar**: Real-time progress and status information
- **Modern Dialogs**: Professional disk selection dialog

### Improved Controls
- **Speed Control**: Adjustable animation speed with slider
- **Better Navigation**: Step forward/backward through moves
- **Keyboard Shortcuts**: 
  - `Space`: Play/Pause
  - `←/→`: Step backward/forward
  - `Ctrl+N`: New game
  - `Ctrl+Q`: Quit

### Enhanced Visualization
- **Anti-aliased Rendering**: Smooth, high-quality graphics
- **Responsive Layout**: Adapts to different window sizes
- **Better Color Scheme**: More vibrant and distinct disk colors
- **Improved Typography**: Better fonts and text rendering

## 📁 Project Structure

```
hanoi_visualization/
├── main_pyside6.py         # New PySide6 entry point
├── main.py                 # Original Pygame version
├── hanoi.py               # Core logic (unchanged)
├── ui/                    # PySide6 UI components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   ├── hanoi_widget.py    # Custom visualization widget
│   └── input_dialog.py    # Disk selection dialog
├── resources/
│   └── styles.qss         # Application stylesheet
├── requirements.txt       # PySide6 dependencies
└── demo_pyside6.py       # Demo and installation script
```

## 🚀 Installation and Usage

### Prerequisites
- Python 3.8 or higher
- PySide6 6.5.0 or higher

### Quick Start

1. **Install PySide6**:
   ```bash
   pip install PySide6
   ```

2. **Run the PySide6 version**:
   ```bash
   python main_pyside6.py
   ```

3. **Or use the demo script** (includes auto-installation):
   ```bash
   python demo_pyside6.py
   ```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv_pyside6

# Activate virtual environment
# On Windows:
venv_pyside6\\Scripts\\activate
# On macOS/Linux:
source venv_pyside6/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main_pyside6.py
```

## 🎮 How to Use

1. **Start a New Game**: The application will prompt you to select the number of disks (1-8)
2. **Controls**:
   - **Play/Pause**: Click the Play button or press `Space`
   - **Step Through**: Use Step Forward/Back buttons or arrow keys
   - **Speed**: Adjust the speed slider to control animation timing
   - **Reset**: Reset to initial state at any time
3. **Visualization**: Watch the recursive algorithm in action with:
   - Real-time code display
   - Call stack visualization
   - Move counter and progress

## 🔧 Features Comparison

| Feature | Pygame Version | PySide6 Version |
|---------|----------------|-----------------|
| **GUI Framework** | Custom Pygame | Native PySide6 |
| **Window Management** | Basic | Professional with menus |
| **Input Dialog** | Custom drawn | Native dialog |
| **Controls** | Keyboard only | GUI + Keyboard |
| **Speed Control** | Fixed | Adjustable slider |
| **Status Display** | Basic text | Status bar + labels |
| **Styling** | Manual | CSS-like stylesheets |
| **Responsiveness** | Fixed size | Resizable layouts |
| **Accessibility** | Limited | Full Qt accessibility |
| **Platform Integration** | Basic | Native integration |

## 🏗️ Architecture

### Component Overview

1. **HanoiMainWindow**: Main application window with menus, toolbar, and layout management
2. **HanoiWidget**: Custom widget handling visualization and animation using QPainter
3. **DiskInputDialog**: Professional dialog for selecting number of disks
4. **Styling**: CSS-like stylesheets for consistent appearance

### Key Improvements

- **Separation of Concerns**: Clear separation between UI and logic
- **Event-Driven Architecture**: Proper Qt signal/slot connections
- **Memory Management**: Automatic Qt object lifecycle management
- **Performance**: Hardware-accelerated rendering through Qt

## 🎨 Customization

### Styling
Edit `resources/styles.qss` to customize the appearance:
```css
QPushButton {
    background-color: #4CAF50;
    border-radius: 6px;
    padding: 8px 16px;
}
```

### Colors
Modify disk colors in `ui/hanoi_widget.py`:
```python
self.disk_colors = [
    QColor(255, 100, 100),  # Red
    QColor(100, 255, 100),  # Green
    # Add more colors...
]
```

## 🐛 Troubleshooting

### Common Issues

1. **PySide6 Import Error**:
   ```bash
   pip install --upgrade PySide6
   ```

2. **Display Issues on High-DPI Screens**:
   The application should automatically handle high-DPI displays through Qt's scaling.

3. **Performance Issues**:
   Ensure you have the latest graphics drivers installed.

## 🔄 Migration from Pygame Version

The core logic in `hanoi.py` remains unchanged. The main differences:

- **Entry Point**: Use `main_pyside6.py` instead of `main.py`
- **Dependencies**: PySide6 instead of Pygame
- **UI**: Professional GUI instead of custom drawing

Both versions can coexist in the same directory.

## 🚧 Future Enhancements

Potential improvements for future versions:

- **Animation Easing**: Smooth disk movement animations
- **3D Visualization**: OpenGL-based 3D rendering
- **Multiple Algorithms**: Compare different solving strategies
- **Statistics Tracking**: Performance metrics and timing
- **Internationalization**: Multi-language support
- **Themes**: Dark/light theme support
- **Export Features**: Save animations as video or images

## 📝 License

This project is educational software. Feel free to use and modify for learning purposes.

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional visualization features
- Performance optimizations
- Accessibility enhancements
- Cross-platform testing
- Documentation improvements

---

**Enjoy exploring the Towers of Hanoi with this modern, professional interface!** 🗼

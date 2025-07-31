# Towers of Hanoi Visualization

A modern Python application that visualizes the solution to the classic Towers of Hanoi puzzle using PySide6 for a professional GUI experience.

## Features

- **Professional GUI**: Native look and feel with menus, toolbar, and status bar
- **Interactive Controls**: Play/pause, step through moves, adjustable speed
- **Visual Code Display**: See the recursive algorithm and call stack in real-time
- **Modern Input Dialog**: Easy disk selection with multiple input methods
- **Keyboard Shortcuts**: Space for play/pause, arrow keys for navigation

## Requirements

- Python 3.8 or higher
- PySide6

## Installation

1. **Clone the repository or download the source code.**

2. **Install PySide6:**
   ```bash
   pip install PySide6
   ```

   Or install from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

Execute the `main.py` script to start the visualization:

```bash
python main.py
```

You will be presented with a dialog to select the number of disks (from 1 to 8) for the puzzle.

## Controls

- **Play/Pause Button**: Start or stop the automated animation
- **Step Forward/Back Buttons**: Manually step through moves
- **Speed Slider**: Adjust animation speed
- **Keyboard Shortcuts**:
  - **Spacebar**: Play or pause the animation
  - **Right Arrow**: Step forward one move
  - **Left Arrow**: Step backward one move
  - **Ctrl+N**: Start a new game
  - **Ctrl+Q**: Quit the application

## User Interface

- **Menu Bar**: File, View, and Help menus with standard shortcuts
- **Toolbar**: Quick access to common actions
- **Status Bar**: Shows current move progress and status
- **Code Panel**: Displays the recursive algorithm
- **Call Stack Panel**: Shows the recursive call stack in real-time

## Demo

You can also run the demo script which includes auto-installation:

```bash
python demo_pyside6.py
```

This script will check for PySide6 and install it if needed, then launch the application.

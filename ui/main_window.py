from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QMenuBar, QToolBar, QPushButton, QSlider, QLabel, 
                             QStatusBar, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence, QIcon

from .hanoi_widget import HanoiWidget
from .input_dialog import DiskInputDialog
from .theme_manager import ThemeManager


class HanoiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Towers of Hanoi Visualization")
        self.setMinimumSize(1000, 700)
        
        # Initialize theme manager
        self.theme_manager = ThemeManager()
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Apply the current theme
        self.theme_manager.apply_theme()
        
        # Initialize with default or get from dialog
        self.num_disks = self.get_disk_input()
        if self.num_disks is None:
            self.close()
            return
            
        self.setup_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        
    def load_stylesheet(self):
        """Load the application stylesheet"""
        try:
            import os
            style_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'styles.qss')
            if os.path.exists(style_path):
                with open(style_path, 'r') as f:
                    self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Could not load stylesheet: {e}")
        
    def get_disk_input(self):
        """Show input dialog to get number of disks"""
        dialog = DiskInputDialog(self)
        if dialog.exec() == DiskInputDialog.Accepted:
            return dialog.get_disk_count()
        return None
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create the Hanoi visualization widget
        self.hanoi_widget = HanoiWidget(self.num_disks, self)
        self.hanoi_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Enable focus to receive keyboard events
        self.hanoi_widget.setFocusPolicy(Qt.StrongFocus)
        self.hanoi_widget.setFocus()
        
        main_layout.addWidget(self.hanoi_widget)
        
        # Control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
    def create_control_panel(self):
        """Create the control panel widget"""
        panel = QWidget()
        layout = QHBoxLayout(panel)
        
        # Playback controls
        self.play_pause_btn = QPushButton("Play")
        self.play_pause_btn.clicked.connect(self.toggle_playback)
        
        self.step_back_btn = QPushButton("◀ Step Back")
        self.step_back_btn.clicked.connect(self.step_back)
        
        self.step_forward_btn = QPushButton("Step Forward ▶")
        self.step_forward_btn.clicked.connect(self.step_forward)
        
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_animation)
        
        # Speed control
        speed_label = QLabel("Speed:")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(100, 2000)  # 100ms to 2000ms
        self.speed_slider.setValue(500)
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        
        self.speed_value_label = QLabel("500ms")
        
        # Add to layout
        layout.addWidget(self.play_pause_btn)
        layout.addWidget(self.step_back_btn)
        layout.addWidget(self.step_forward_btn)
        layout.addWidget(self.reset_btn)
        layout.addStretch()
        layout.addWidget(speed_label)
        layout.addWidget(self.speed_slider)
        layout.addWidget(self.speed_value_label)
        
        return panel
        
    def create_menus(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New Game", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.setStatusTip("Start a new game")
        new_action.triggered.connect(self.new_game)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        reset_view_action = QAction("&Reset View", self)
        reset_view_action.setStatusTip("Reset the visualization")
        reset_view_action.triggered.connect(self.reset_animation)
        view_menu.addAction(reset_view_action)
        
        view_menu.addSeparator()
        
        # Theme submenu
        theme_menu = view_menu.addMenu("&Theme")
        
        light_theme_action = QAction("&Light Theme", self)
        light_theme_action.setStatusTip("Switch to light theme")
        light_theme_action.setCheckable(True)
        light_theme_action.triggered.connect(lambda: self.set_theme(ThemeManager.LIGHT_THEME))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("&Dark Theme", self)
        dark_theme_action.setStatusTip("Switch to dark theme")
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(lambda: self.set_theme(ThemeManager.DARK_THEME))
        theme_menu.addAction(dark_theme_action)
        
        # Store theme actions for updating checkmarks
        self.light_theme_action = light_theme_action
        self.dark_theme_action = dark_theme_action
        
        # Set initial checkmarks
        self.update_theme_menu_checkmarks()
        
        toggle_theme_action = QAction("Toggle &Theme", self)
        toggle_theme_action.setShortcut("Ctrl+T")
        toggle_theme_action.setStatusTip("Toggle between light and dark themes")
        toggle_theme_action.triggered.connect(self.theme_manager.toggle_theme)
        view_menu.addAction(toggle_theme_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.setStatusTip("About this application")
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        
        # Add actions to toolbar
        play_action = QAction("Play/Pause", self)
        play_action.setStatusTip("Play or pause the animation")
        play_action.triggered.connect(self.toggle_playback)
        toolbar.addAction(play_action)
        
        toolbar.addSeparator()
        
        step_back_action = QAction("Step Back", self)
        step_back_action.setStatusTip("Step back one move")
        step_back_action.triggered.connect(self.step_back)
        toolbar.addAction(step_back_action)
        
        step_forward_action = QAction("Step Forward", self)
        step_forward_action.setStatusTip("Step forward one move")
        step_forward_action.triggered.connect(self.step_forward)
        toolbar.addAction(step_forward_action)
        
        toolbar.addSeparator()
        
        reset_action = QAction("Reset", self)
        reset_action.setStatusTip("Reset to initial state")
        reset_action.triggered.connect(self.reset_animation)
        toolbar.addAction(reset_action)
        
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Add permanent widgets to status bar
        self.move_label = QLabel("Move: 0/0")
        self.status_label = QLabel("Ready")
        
        self.status_bar.addWidget(self.move_label)
        self.status_bar.addPermanentWidget(self.status_label)
        
        # Update status bar initially
        self.update_status_bar()
        
    def toggle_playback(self):
        """Toggle between play and pause"""
        self.hanoi_widget.toggle_autoplay()
        self.update_play_button()
        self.update_status_bar()
        
    def step_back(self):
        """Step back one move"""
        self.hanoi_widget.previous_move()
        self.update_status_bar()
        
    def step_forward(self):
        """Step forward one move"""
        self.hanoi_widget.next_move()
        self.update_status_bar()
        
    def reset_animation(self):
        """Reset the animation to initial state"""
        self.hanoi_widget.reset_animation()
        self.update_play_button()
        self.update_status_bar()
        
    def on_speed_changed(self, value):
        """Handle speed slider change"""
        self.hanoi_widget.set_animation_speed(value)
        self.speed_value_label.setText(f"{value}ms")
        
    def update_play_button(self):
        """Update the play/pause button text"""
        if self.hanoi_widget.auto_play:
            self.play_pause_btn.setText("Pause")
        else:
            self.play_pause_btn.setText("Play")
            
    def update_status_bar(self):
        """Update the status bar information"""
        total_moves = len(self.hanoi_widget.solver.moves)
        current_move = self.hanoi_widget.current_move
        
        self.move_label.setText(f"Move: {current_move}/{total_moves}")
        
        if self.hanoi_widget.auto_play:
            self.status_label.setText("Playing")
        elif current_move == total_moves:
            self.status_label.setText("Completed")
        else:
            self.status_label.setText("Paused")
            
    def new_game(self):
        """Start a new game with possibly different number of disks"""
        num_disks = self.get_disk_input()
        if num_disks is not None:
            self.num_disks = num_disks
            # Create new hanoi widget with new disk count
            old_widget = self.hanoi_widget
            self.hanoi_widget = HanoiWidget(self.num_disks, self)
            self.hanoi_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.hanoi_widget.setFocusPolicy(Qt.StrongFocus)
            self.hanoi_widget.setFocus()
            
            # Replace in layout
            central_widget = self.centralWidget()
            layout = central_widget.layout()
            layout.replaceWidget(old_widget, self.hanoi_widget)
            old_widget.deleteLater()
            
            # Update UI
            self.update_play_button()
            self.update_status_bar()
            
            # Apply theme to new widget
            self.hanoi_widget.update_theme_colors()
            
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Towers of Hanoi",
                         "Towers of Hanoi Visualization\\n\\n"
                         "A educational tool to visualize the classic "
                         "Towers of Hanoi problem and its recursive solution.\\n\\n"
                         "Controls:\\n"
                         "• Space: Play/Pause\\n"
                         "• Left Arrow: Previous move\\n"
                         "• Right Arrow: Next move\\n\\n"
                         "Built with PySide6")
                         
    def keyPressEvent(self, event):
        """Handle global keyboard shortcuts"""
        # Forward to hanoi widget for visualization controls
        self.hanoi_widget.keyPressEvent(event)
        # Update UI after key press
        self.update_play_button()
        self.update_status_bar()
        super().keyPressEvent(event)
        
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop any running timers
        if hasattr(self.hanoi_widget, 'timer'):
            self.hanoi_widget.timer.stop()
        event.accept()
        
    def set_theme(self, theme):
        """Set the application theme"""
        self.theme_manager.set_theme(theme)
        
    def on_theme_changed(self, theme):
        """Handle theme change"""
        # Update menu checkmarks
        self.update_theme_menu_checkmarks()
        
        # Update hanoi widget colors
        if hasattr(self, 'hanoi_widget'):
            self.hanoi_widget.update_theme_colors()
            self.hanoi_widget.update()  # Force repaint
        
    def update_theme_menu_checkmarks(self):
        """Update the checkmarks in the theme menu"""
        current_theme = self.theme_manager.get_current_theme()
        self.light_theme_action.setChecked(current_theme == ThemeManager.LIGHT_THEME)
        self.dark_theme_action.setChecked(current_theme == ThemeManager.DARK_THEME)

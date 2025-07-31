from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QGridLayout, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class DiskInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Towers of Hanoi - Setup")
        self.setModal(True)
        self.setFixedSize(500, 350)
        
        # Store the selected number of disks
        self.selected_disks = 3
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Enter Number of Disks")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instructions
        instruction_label = QLabel("Click a number button or use the spinner")
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)
        
        # Spinner for disk selection
        spinner_layout = QHBoxLayout()
        spinner_layout.addStretch()
        
        spinner_label = QLabel("Number of disks:")
        self.disk_spinner = QSpinBox()
        self.disk_spinner.setRange(1, 8)
        self.disk_spinner.setValue(3)
        self.disk_spinner.valueChanged.connect(self.on_spinner_changed)
        
        spinner_layout.addWidget(spinner_label)
        spinner_layout.addWidget(self.disk_spinner)
        spinner_layout.addStretch()
        
        layout.addLayout(spinner_layout)
        
        # Number buttons grid
        buttons_widget = QWidget()
        buttons_layout = QGridLayout(buttons_widget)
        buttons_layout.setSpacing(10)
        
        self.number_buttons = []
        for i in range(1, 9):
            button = QPushButton(str(i))
            button.setFixedSize(50, 50)
            button.setCheckable(True)
            button.clicked.connect(lambda checked, num=i: self.on_number_button_clicked(num))
            self.number_buttons.append(button)
            
            # Arrange in 2 rows of 4
            row = 0 if i <= 4 else 1
            col = (i - 1) % 4
            buttons_layout.addWidget(button, row, col)
        
        # Set initial selection
        self.number_buttons[2].setChecked(True)  # Button for 3 disks
        
        layout.addWidget(buttons_widget)
        
        # Selected display
        self.selected_label = QLabel("Selected: 3 disks")
        self.selected_label.setAlignment(Qt.AlignCenter)
        selected_font = QFont()
        selected_font.setPointSize(12)
        selected_font.setBold(True)
        self.selected_label.setFont(selected_font)
        layout.addWidget(self.selected_label)
        
        # OK and Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        ok_button = QPushButton("OK")
        ok_button.setDefault(True)
        ok_button.clicked.connect(self.accept)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def on_spinner_changed(self, value):
        """Handle spinner value change"""
        self.selected_disks = value
        self.update_selection()
        
    def on_number_button_clicked(self, number):
        """Handle number button click"""
        self.selected_disks = number
        self.disk_spinner.setValue(number)
        self.update_selection()
        
    def update_selection(self):
        """Update UI to reflect current selection"""
        # Update button states
        for i, button in enumerate(self.number_buttons):
            button.setChecked(i + 1 == self.selected_disks)
        
        # Update label
        self.selected_label.setText(f"Selected: {self.selected_disks} disks")
        
    def get_disk_count(self):
        """Return the selected number of disks"""
        return self.selected_disks

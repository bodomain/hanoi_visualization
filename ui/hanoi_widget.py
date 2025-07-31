from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, QRect, Signal
from PySide6.QtGui import QPainter, QColor, QFont, QPen, QBrush
from hanoi import HanoiSolver, Tower


class HanoiWidget(QWidget):
    def __init__(self, num_disks=3, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        
        # Initialize the Hanoi solver
        self.num_disks = num_disks
        self.solver = HanoiSolver(num_disks)
        self.solver.solve()
        
        # Reset towers to their initial state for visualization
        self.solver.towers = {
            'A': Tower('A'),
            'B': Tower('B'),
            'C': Tower('C')
        }
        for size in range(self.num_disks, 0, -1):
            self.solver.towers['A'].push(size)
        
        # Animation control
        self.current_move = 0
        self.auto_play = False
        self.animation_speed = 500  # ms per move
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_move)
        
        # Colors
        self.bg_color = QColor(255, 255, 255)
        self.tower_color = QColor(0, 0, 0)
        self.disk_colors = [
            QColor(255, 100, 100),  # Red
            QColor(100, 255, 100),  # Green
            QColor(100, 100, 255),  # Blue
            QColor(255, 255, 100),  # Yellow
            QColor(255, 100, 255),  # Magenta
            QColor(100, 255, 255),  # Cyan
            QColor(255, 150, 100),  # Orange
            QColor(150, 100, 255),  # Purple
        ]
        
        # Fonts
        self.font = QFont('Arial', 12)
        self.code_font = QFont('Courier', 10)
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
    def paintEvent(self, event):
        """Main drawing method"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Clear background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Calculate drawing areas
        widget_width = self.width()
        widget_height = self.height()
        
        # Main visualization area (left side)
        viz_width = min(widget_width * 0.6, widget_width - 400)
        viz_height = widget_height
        
        # Draw the visualization
        self.draw_towers(painter, viz_width, viz_height)
        self.draw_disks(painter, viz_width, viz_height)
        
        # Draw side panel (right side)
        if widget_width > 800:
            panel_x = viz_width + 20
            self.draw_code_panel(painter, panel_x, 20, widget_width - panel_x - 20, viz_height - 40)
            self.draw_call_stack_panel(painter, panel_x, viz_height // 2, 
                                     widget_width - panel_x - 20, viz_height // 2 - 20)
        
        # Draw controls
        self.draw_controls(painter, 20, widget_height - 60, viz_width - 40, 40)
        
    def draw_towers(self, painter, width, height):
        """Draw the three towers"""
        painter.setPen(QPen(self.tower_color, 3))
        painter.setBrush(QBrush(self.tower_color))
        
        # Calculate tower positions
        tower_width = width * 0.8
        tower_height = height * 0.6
        tower_start_x = (width - tower_width) // 2
        tower_start_y = height * 0.2
        
        # Draw base
        base_rect = QRect(tower_start_x, tower_start_y + tower_height - 20, 
                         tower_width, 20)
        painter.drawRect(base_rect)
        
        # Draw the three pegs
        peg_positions = [
            tower_start_x + tower_width * 0.2,
            tower_start_x + tower_width * 0.5,
            tower_start_x + tower_width * 0.8
        ]
        
        for i, pos in enumerate(peg_positions):
            # Draw peg
            peg_rect = QRect(pos - 5, tower_start_y, 10, tower_height - 20)
            painter.drawRect(peg_rect)
            
            # Draw tower label
            painter.setFont(self.font)
            label = chr(65 + i)  # A, B, C
            painter.drawText(pos - 5, tower_start_y + tower_height + 15, label)
            
    def draw_disks(self, painter, width, height):
        """Draw the disks on the towers"""
        # Calculate tower positions (same as in draw_towers)
        tower_width = width * 0.8
        tower_height = height * 0.6
        tower_start_x = (width - tower_width) // 2
        tower_start_y = height * 0.2
        
        peg_positions = [
            tower_start_x + tower_width * 0.2,
            tower_start_x + tower_width * 0.5,
            tower_start_x + tower_width * 0.8
        ]
        
        tower_mapping = {'A': 0, 'B': 1, 'C': 2}
        
        for tower_name, tower in self.solver.towers.items():
            peg_x = peg_positions[tower_mapping[tower_name]]
            
            for i, disk in enumerate(tower.disks):
                # Calculate disk dimensions
                disk_width = 30 + disk * 25
                disk_height = 20
                disk_x = peg_x - disk_width // 2
                disk_y = tower_start_y + tower_height - 40 - i * (disk_height + 2)
                
                # Draw disk
                color = self.disk_colors[min(disk - 1, len(self.disk_colors) - 1)]
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor(0, 0, 0), 2))
                
                disk_rect = QRect(disk_x, disk_y, disk_width, disk_height)
                painter.drawRoundedRect(disk_rect, 5, 5)
                
                # Draw disk number
                painter.setPen(QPen(QColor(255, 255, 255)))
                painter.setFont(self.font)
                painter.drawText(disk_rect, Qt.AlignCenter, str(disk))
                
    def draw_code_panel(self, painter, x, y, width, height):
        """Draw the code visualization panel"""
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont('Arial', 14, QFont.Bold))
        painter.drawText(x, y + 20, "Move Function Code")
        
        # Code lines with syntax highlighting
        code_lines = [
            ("def _move_disks(self, n, source, target, auxiliary):", QColor(0, 0, 255)),
            ("    if n > 0:", QColor(0, 0, 255)),
            ("        self._move_disks(n-1, source, auxiliary, target)", QColor(0, 0, 0)),
            ("        disk = self.towers[source].pop()", QColor(0, 0, 0)),
            ("        self.towers[target].push(disk)", QColor(0, 0, 0)),
            ("        self.moves.append((source, target, disk))", QColor(0, 0, 0)),
            ("        self._move_disks(n-1, auxiliary, target, source)", QColor(0, 0, 0)),
        ]
        
        painter.setFont(self.code_font)
        y_offset = y + 50
        for line, color in code_lines:
            painter.setPen(QPen(color))
            painter.drawText(x, y_offset, line)
            y_offset += 20
            
    def draw_call_stack_panel(self, painter, x, y, width, height):
        """Draw the call stack visualization panel"""
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(QFont('Arial', 14, QFont.Bold))
        painter.drawText(x, y + 20, "Recursive Call Stack")
        
        if self.current_move < len(self.solver.call_stack_history):
            painter.setFont(self.code_font)
            y_offset = y + 50
            
            for i, call in enumerate(self.solver.call_stack_history[self.current_move]):
                indentation = "  " * i
                painter.drawText(x, y_offset, indentation + call)
                y_offset += 18
                
                # Don't draw too many to avoid overflow
                if y_offset > y + height - 20:
                    break
                    
    def draw_controls(self, painter, x, y, width, height):
        """Draw control information"""
        painter.setPen(QPen(QColor(0, 0, 0)))
        painter.setFont(self.font)
        
        controls_text = "← Previous | → Next | Space: Play/Pause"
        painter.drawText(x, y + 15, controls_text)
        
        move_text = f"Move {self.current_move}/{len(self.solver.moves)}"
        painter.drawText(x, y + 35, move_text)
        
        status_text = "Playing" if self.auto_play else "Paused"
        painter.drawText(x + 300, y + 35, f"Status: {status_text}")
        
    def keyPressEvent(self, event):
        """Handle keyboard input"""
        if event.key() == Qt.Key_Space:
            self.toggle_autoplay()
        elif event.key() == Qt.Key_Right and not self.auto_play:
            self.next_move()
        elif event.key() == Qt.Key_Left and not self.auto_play:
            self.previous_move()
        else:
            super().keyPressEvent(event)
            
    def toggle_autoplay(self):
        """Toggle between play and pause"""
        self.auto_play = not self.auto_play
        if self.auto_play:
            self.timer.start(self.animation_speed)
        else:
            self.timer.stop()
        self.update()
        
    def next_move(self):
        """Execute the next move"""
        if self.current_move < len(self.solver.moves):
            source, target, disk = self.solver.moves[self.current_move]
            self.solver.towers[target].push(
                self.solver.towers[source].pop())
            self.current_move += 1
            self.update()
        else:
            # Animation finished
            if self.auto_play:
                self.toggle_autoplay()
                
    def previous_move(self):
        """Undo the previous move"""
        if self.current_move > 0:
            self.current_move -= 1
            source, target, disk = self.solver.moves[self.current_move]
            # Reverse the move: move disk from target back to source
            self.solver.towers[source].push(
                self.solver.towers[target].pop())
            self.update()
            
    def reset_animation(self):
        """Reset to initial state"""
        self.auto_play = False
        self.timer.stop()
        self.current_move = 0
        
        # Reset towers
        self.solver.towers = {
            'A': Tower('A'),
            'B': Tower('B'),
            'C': Tower('C')
        }
        for size in range(self.num_disks, 0, -1):
            self.solver.towers['A'].push(size)
            
        self.update()
        
    def set_animation_speed(self, speed):
        """Set the animation speed in milliseconds"""
        self.animation_speed = speed
        if self.auto_play:
            self.timer.setInterval(speed)

import pygame
import sys
from hanoi import HanoiSolver, Tower

class HanoiVisualization:
    def __init__(self, num_disks=3):
        pygame.init()
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
        
        # Display settings
        self.width = 1400
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Towers of Hanoi Visualization")
        
        # Colors
        self.bg_color = (255, 255, 255)
        self.tower_color = (0, 0, 0)
        self.disk_colors = [
            (200, 200, 200), (180, 180, 180), (160, 160, 160),
            (140, 140, 140), (120, 120, 120), (100, 100, 100),
            (80, 80, 80), (60, 60, 60)
        ]
        
        # Animation control
        self.current_move = 0
        self.animation_speed = 500  # ms per move
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.code_font = pygame.font.SysFont('Courier', 20)

    def draw_code(self):
        title = self.font.render("Move Function Code", True, (0, 0, 0))
        self.screen.blit(title, (720, 20))
        code_font = pygame.font.SysFont('Courier', 16)
        code_colors = {
            "keyword": (0, 0, 255),
            "function": (0, 128, 128),
            "self": (128, 0, 128),
            "default": (0, 0, 0)
        }

        code_lines = [
            [("def ", "keyword"), ("_move_disks", "function"), ("(self, n, source, target, auxiliary):", "default")],
            [("    if ", "keyword"), ("n > 0:", "default")],
            [("        self._move_disks(n-1, source, auxiliary, target)", "default")],
            [("        disk = self.towers[source].pop()", "default")],
            [("        self.towers[target].push(disk)", "default")],
            [("        self.moves.append((source, target, disk))", "default")],
            [("        self._move_disks(n-1, auxiliary, target, source)", "default")],
        ]
        y_offset = 60
        for line in code_lines:
            x_offset = 720
            for text, color_key in line:
                color = code_colors.get(color_key, code_colors["default"])
                text_surface = code_font.render(text, True, color)
                self.screen.blit(text_surface, (x_offset, y_offset))
                x_offset += text_surface.get_width()
            y_offset += 20

    def draw_call_stack(self):
        title = self.font.render("Recursive Call Stack", True, (0, 0, 0))
        self.screen.blit(title, (720, 220))
        y_offset = 260
        if self.current_move < len(self.solver.call_stack_history):
            for i, call in enumerate(self.solver.call_stack_history[self.current_move]):
                # Indent based on the call stack depth
                indentation = "  " * i
                text = self.code_font.render(indentation + call, True, (0, 0, 0))
                self.screen.blit(text, (720, y_offset))
                y_offset += 25
    
    def draw_towers(self):
        # Draw the base
        pygame.draw.rect(self.screen, self.tower_color, 
                         (100, 400, 600, 20))
        
        # Draw the three pegs
        for i, pos in enumerate([200, 400, 600]):
            pygame.draw.rect(self.screen, self.tower_color, 
                             (pos-10, 200, 20, 200))
            
            # Draw tower label
            label = self.font.render(chr(65+i), True, (0, 0, 0))
            self.screen.blit(label, (pos-8, 420))
    
    def draw_disks(self):
        for tower_name in ['A', 'B', 'C']:
            tower = self.solver.towers[tower_name]
            for i, disk in enumerate(tower.disks):
                width = 20 + disk * 30
                x = {'A': 200, 'B': 400, 'C': 600}[tower_name] - width//2
                y = 380 - i * 30
                color = self.disk_colors[disk-1]
                pygame.draw.rect(self.screen, color, (x, y, width, 20))
                # Draw disk size label
                text_color = (0, 0, 0) if color[0] > 128 else (255, 255, 255)
                label = self.font.render(str(disk), True, text_color)
                self.screen.blit(label, (x + width//2 - 5, y + 2))
    
    def run(self):
        running = True
        auto_play = False
        last_move_time = pygame.time.get_ticks()
        
        while running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        auto_play = not auto_play
                    elif event.key == pygame.K_RIGHT and not auto_play:
                        if self.current_move < len(self.solver.moves):
                            source, target, disk = self.solver.moves[self.current_move]
                            self.solver.towers[target].push(
                                self.solver.towers[source].pop())
                            self.current_move += 1
                    elif event.key == pygame.K_LEFT and not auto_play:
                        if self.current_move > 0:
                            self.current_move -= 1
                            source, target, disk = self.solver.moves[self.current_move]
                            # Reverse the move: move disk from target back to source
                            self.solver.towers[source].push(
                                self.solver.towers[target].pop())
            
            # Auto play logic
            if auto_play and current_time - last_move_time > self.animation_speed:
                if self.current_move < len(self.solver.moves):
                    source, target, disk = self.solver.moves[self.current_move]
                    self.solver.towers[target].push(
                        self.solver.towers[source].pop())
                    self.current_move += 1
                    last_move_time = current_time
            
            # Drawing
            self.screen.fill(self.bg_color)
            self.draw_towers()
            self.draw_disks()
            self.draw_call_stack()
            self.draw_code()
            
            # Display controls
            controls = self.font.render(
                "Left: Prev | Right: Next | Space: Play/Pause", 
                True, (0, 0, 0))
            self.screen.blit(controls, (20, 20))
            
            move_info = self.font.render(
                f"Move {self.current_move}/{len(self.solver.moves)}", 
                True, (0, 0, 0))
            self.screen.blit(move_info, (20, 50))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


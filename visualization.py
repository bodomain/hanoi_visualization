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
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Towers of Hanoi Visualization")
        
        # Colors
        self.bg_color = (240, 240, 240)
        self.tower_color = (100, 100, 100)
        self.disk_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (128, 0, 0), (0, 128, 0), (0, 0, 128)
        ]
        
        # Animation control
        self.current_move = 0
        self.animation_speed = 500  # ms per move
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
    
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
                label = self.font.render(str(disk), True, (255, 255, 255))
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
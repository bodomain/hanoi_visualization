class Tower:
    def __init__(self, name):
        self.name = name
        self.disks = []
    
    def push(self, disk):
        self.disks.append(disk)
    
    def pop(self):
        return self.disks.pop()

class HanoiSolver:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.moves = []
        self.towers = {
            'A': Tower('A'),
            'B': Tower('B'),
            'C': Tower('C')
        }
        # Initialize tower A with disks
        for size in range(num_disks, 0, -1):
            self.towers['A'].push(size)
    
    def solve(self):
        self._move_disks(self.num_disks, 'A', 'C', 'B')
    
    def _move_disks(self, n, source, target, auxiliary):
        if n > 0:
            # Move n-1 disks from source to auxiliary
            self._move_disks(n-1, source, auxiliary, target)
            
            # Move the nth disk from source to target
            disk = self.towers[source].pop()
            self.towers[target].push(disk)
            self.moves.append((source, target, disk))
            
            # Move the n-1 disks from auxiliary to target
            self._move_disks(n-1, auxiliary, target, source)

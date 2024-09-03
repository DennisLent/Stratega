ATTACK_DAMAGE = 10
MOVEMENT_LIMIT = 2

class Player():
    def __init__(self, name:str, start_position: tuple, health: int, movement_points=MOVEMENT_LIMIT):
        self.name = name
        self.position = list(start_position)
        self.health = health
        self.movement_points = movement_points
        self.max_movement = movement_points
    
    def __repr__(self) -> str:
        return f"{self.name}: Pos={tuple(self.position)}, HP={self.health}, MP={self.movement_points}"
    
    def moveUp(self):
        if self.movement_points > 0:
            self.position[1] += 1
            self.movement_points -= 1
    
    def moveDown(self):
        if self.movement_points > 0:
            self.position[1] -= 1
            self.movement_points -= 1
    
    def moveLeft(self):
        if self.movement_points > 0:
            self.position[0] -= 1
            self.movement_points -=1
    
    def moveRight(self):
        if self.movement_points > 0:
            self.position[0] += 1
            self.movement_points -= 1
    
    def attack(self, other):
        other.health -= ATTACK_DAMAGE
        self.movement_points -= 1
    
    # refresh movement points at the end of a turn
    def reset(self):
        self.movement_points = self.max_movement
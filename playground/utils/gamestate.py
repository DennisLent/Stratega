from utils.character import Player, ATTACK_DAMAGE, MOVEMENT_LIMIT
from utils.rewards import calculate_reward
import copy
import random

MAX_TURNS = 100

class GameState():
    def __init__(self, map_size=20, random_init=False):
        self.done = False
        self.turn = 0
        self.map_size = map_size

        # own player and opponent starting positions
        # opponent has 0 movement points to mimic a "do nothing agent"
        if random_init:
            middle_point = round(map_size/2)
            point1 = (random.choice([i for i in range(0, middle_point)]))
            point2 = (random.choice([i for i in range(middle_point, self.map_size)]))
            self.player = Player(name="Player", start_position=(point1, point1), health=100)
            self.opponent = Player(name="Opp", start_position=(point2, point2), health=20, movement_points=0)
        else:
            self.player = Player(name="Player", start_position=(0,0), health=100)
            self.opponent = Player(name="Opp", start_position=(12,12), health=20, movement_points=0)
        
        self.reward = calculate_reward(self)
        
    
    # check if the game is done if either player is dead or max turns have been reached
    def check_done(self) -> None:
        if (self.player.health <= 0) or (self.opponent.health <= 0) or (self.turn >= MAX_TURNS):
            self.done = True
    
    # make sure you can only attack if you are next to eachother
    def can_attack(self) -> bool:
        (player_x, player_y) = self.player.position
        (other_x, other_y) = self.opponent.position
        squared_distance = ((player_x - other_x)**2 + (player_y - other_y)**2)
        if (squared_distance <= 2):
            return True
        else:
            return False
    
    # return all possible moves that a player can make
    # if we are iterating in the tree and we want to check for the next turn, we will need to make sure that we update the turns and movement points here
    def get_available_moves(self) -> list:
        moves = []
        if not self.done:
            if self.player.movement_points > 0:
                moves.extend(["up", "down", "left", "right"])
                if self.can_attack():
                    moves.append("attack")
                return moves
            # no movement points left
            else:
                self.turn += 1
                self.player.reset()
                return self.get_available_moves()


    # run actions for the player only as the opponent will do nothing
    def player_action(self, command) -> None:
        match command:
            case "up":
                self.player.moveUp()
            case "down":
                self.player.moveDown()
            case "left":
                self.player.moveLeft()
            case "right":
                self.player.moveRight()
            case "attack":
                self.player.attack(self.opponent)
        
        self.check_done()

        self.reward = calculate_reward(self)
    
    # forward model that advances the game by n actions
    def simulate_turns(self, actions: list):
        game_state_copy = copy.deepcopy(self)
        for action in actions:
            game_state_copy.player_action(action)
            if game_state_copy.player.movement_points == 0:
                game_state_copy.turn += 1
                game_state_copy.player.reset()
        return game_state_copy

    def print_map(self):
        grid = [["." for _ in range(self.map_size)] for _ in range(self.map_size)]
        
        # Place the player and opponent on the map
        player_x, player_y = self.player.position
        opponent_x, opponent_y = self.opponent.position
        
        # opponent and player
        grid[player_y][player_x] = "P"
        grid[opponent_y][opponent_x] = "O" 
        
        # Print the grid
        print("Game Map:")
        for row in grid:
            print(" ".join(row))
        print()

    
    def __repr__(self) -> str:
        return (f"Turn: {self.turn}, Reward: {self.reward:.2f}, "f"{self.player}, {self.opponent}")
    
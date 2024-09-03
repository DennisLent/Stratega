import copy
from utils.gamestate import GameState

class TreeNode:
    def __init__(self, game_state: GameState, parent=None, action=None) -> None:
        self.game_state = game_state 
        self.parent = parent 
        self.children = []
        self.action = action
        self.visits = 0
        self.value = 0
    
    def __repr__(self) -> str:
        return f"{self.action} -> {self.game_state})"

    # check if there are any available moves
    def is_fully_expanded(self) -> bool:
        return len(self.children) == len(self.game_state.get_available_moves())

    # add new node based on an action
    def add_child(self, action) -> None:
        # need to make a deepcopy of the game state to not mess with the current one we have
        new_game_state = copy.deepcopy(self.game_state)
        new_game_state.player_action(action)
        new_node = TreeNode(game_state=new_game_state, parent=self, action=action)
        self.children.append(new_node)

    # print the tree
    def pretty_print(self, prefix="", is_last=True):
        print(prefix, end="")
        if self.parent is not None:
            if is_last:
                print("∟———", end="")
                prefix += "     "
            else:
                print("ͱ———", end="")
                prefix += "⎸   "
        print(f"{self.action} -> {self.game_state} (Visits: {self.visits}) (Value: {self.value})")
        
        child_count = len(self.children)
        for i, child in enumerate(self.children):
            is_last_child = (i == (child_count - 1))
            child.pretty_print(prefix, is_last_child)
    
    # return the best child according to UCT
    # https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    def best_child(self, exploration_weight=1.4):
        choices_weights = [
            (child.value / child.visits) + exploration_weight * (2 * (self.visits) ** 0.5 / (1 + child.visits))
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

# expand the tree from a given gamestate (node)
def expand_tree(node: TreeNode, depth=1):
    if depth == 0 or node.game_state.done:
        return
    
    # get available moves from the gamestate
    available_moves = node.game_state.get_available_moves()

    # add new gamestate and expand the gamestates recursively
    for move in available_moves:
        node.add_child(move)
        expand_tree(node.children[-1], depth - 1)

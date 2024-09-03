import copy
from utils.gamestate import GameState

class AbstractTreeNode:
    def __init__(self, game_state: GameState, parent=None, action=None) -> None:
        self.game_state = game_state 
        self.parent = parent 
        self.children = []
        self.action = [action] if action is not None else []
        self.visits = 0
        self.value = 0
        self.original_children = []
        self.merged_with = None
    
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
        new_node = AbstractTreeNode(game_state=new_game_state, parent=self, action=action)
        self.children.append(new_node)
    
    # merge nodes that are similar
    # we average their cumulative rewards and visits
    def merge_with(self, other):
        
        self.original_children.append((other, other.children[:]))
        self.merged_with = other

        # Combine actions into a list
        if isinstance(self.action, list):
            self.action.append(other.action[0])
        else:
            self.action = [self.action, other.action[0]]
        
        # average the visits and value of the nodes
        self.visits = round((self.visits + other.visits) / 2)
        self.value = (self.value + other.value) / 2

        # update the children of the nodes to point to this node
        for child in other.children:
            child.parent = self
        self.children.extend(other.children)

        #remove merged node from the parent node
        self.parent.children.remove(other)
    
    # method to unmerge the changes and to revert back to the original tree
    def unmerge(self):
        if self.merge_with:
            # split up the value and visits between the nodes that were merged
            split_value = self.value / len(self.original_children)
            split_visits = round(self.visits / len(self.original_children))
            for (original_node, original_children) in self.original_children:
                for child in original_children:
                    self.children.remove(child)
                original_node.children = original_children
                
                # assign the split values
                self.value, original_node.value = split_value, split_value
                self.visits, original_node.visits = split_visits, split_visits

                # append original node to parent
                self.parent.children.append(original_node)
            
            # Restore the original action
            self.action = [self.action[0]] if len(self.action) > 1 else self.action

            # clear merge
            self.merge_with = None
            self.original_children = []

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
def expand_tree(node: AbstractTreeNode, depth=1):
    if depth == 0 or node.game_state.done:
        return
    
    # get available moves from the gamestate
    available_moves = node.game_state.get_available_moves()

    # add new gamestate and expand the gamestates recursively
    for move in available_moves:
        node.add_child(move)
        expand_tree(node.children[-1], depth - 1)

import copy
from playground.utils.gamestate import GameState

class AbstractTreeNode:
    def __init__(self, game_state: GameState, parent=None, action=None) -> None:
        self.game_state = game_state 
        self.parent: AbstractTreeNode = parent 
        self.children: list[AbstractTreeNode] = []
        self.action = [action] if action is not None else []
        self.visits = 0
        self.value = 0
        self.original_children: list[AbstractTreeNode] = []
        self.merged_with: AbstractTreeNode = None
    
    def __repr__(self) -> str:
        if self.merge_with:
            return f"{self.action} -> R={round(self.game_state.reward, 3)} P={self.game_state.player.position})"
        else:
            return f"{self.action} -> R={round(self.game_state.reward, 3)} P={self.game_state.player.position})"
    
    # override eq method to check for actual values of the node
    def __eq__(self, other) -> bool:
        return (self.action == other.action) and (self.value == other.value) and (self.visits == other.visits) and (self.game_state == other.game_state)
    
    def __hash__(self):
        # Compute a hash based on unique properties of the node
        return hash((self.game_state, self.parent, tuple(self.action)))

    # check if there are any available moves
    def is_fully_expanded(self) -> bool:
        # check before abstraction i.e. there are as many children as there are available moves
        if len(self.children) == len(self.game_state.get_available_moves()):
            return True
        
        #check if all available moves have been used in the children
        all_actions = self.game_state.get_available_moves()
        tried_actions = []
        for child in self.children:
            tried_actions.extend(child.action)
        
        return all(move in tried_actions for move in all_actions)

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

        # make sure we only merge one node for now
        if not self.merged_with:

            #if the other node has children we save them
            if other.children:
                for child in other.children:
                    self.original_children.append(child)
                    child.parent = self
                    self.children.append(child)

            #show that this node is merged
            self.merged_with = other

            # Combine actions into a list
            # for debugging
            for node_action in other.action:
                self.action.append(node_action)
            
            # average the visits and value of the nodes
            self.visits = round((self.visits + other.visits) / 2)
            self.value = (self.value + other.value) / 2

            self.parent.children.remove(other)
        
    
    # method to unmerge the changes and to revert back to the original tree
    def unmerge(self):
        if self.merged_with:

            #get original node that was merged and add children to it
            unmerged_node = self.merged_with
            for child in self.original_children:
                child.parent = unmerged_node
                self.children.remove(child)
            
            #update values
            unmerged_node.value = self.value
            unmerged_node.visits = self.visits
            
            #add unmerged node back to parent
            self.parent.children.append(unmerged_node)
            self.action.pop()
    
            # clear merge
            self.merged_with = None
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
        print(f"{self.action} -> R={round(self.game_state.reward, 3)} P={self.game_state.player.position} (Visits: {self.visits}) (Value: {self.value})")

        
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

import pytest
from playground.utils.gamestate import GameState
from playground.utils.abstract_tree import AbstractTreeNode, expand_tree
from playground.utils.character import Player
import copy

# Mock GameState class for testing
class MockGameState(GameState):
    def __init__(self, done=False, moves=None, reward=0):
        self.done = done
        self.reward = reward
        self.moves = moves if moves is not None else ['up', 'down', 'left', 'right']
        self.player = Player("test", (0,0), 100)

    def get_available_moves(self):
        return self.moves

    def player_action(self, action):
        # Simulate basic action logic
        if action == 'up':
            self.done = True  # 'up' finishes the game

    def __eq__(self, other):
        return (self.reward == other.reward) and (self.done == other.done)

    def __hash__(self):
        return hash((self.reward, self.done))

    def __repr__(self):
        return f"MockGameState(done={self.done}, reward={self.reward})"


# Test AbstractTreeNode initialization
def test_treenode_initialization():
    game_state = MockGameState()
    node = AbstractTreeNode(game_state)

    assert node.game_state == game_state
    assert node.parent is None
    assert node.action == []
    assert node.visits == 0
    assert node.value == 0
    assert node.children == []

# Test adding children
def test_add_child():
    game_state = MockGameState()
    node = AbstractTreeNode(game_state)

    node.add_child("up")
    assert len(node.children) == 1
    assert node.children[0].action == ["up"]
    assert node.children[0].parent == node
    assert node.children[0].game_state.done  # 'up' should mark the game as done

    node.add_child("down")
    assert len(node.children) == 2
    assert node.children[1].action == ["down"]

# Test if node is fully expanded
def test_is_fully_expanded():
    game_state = MockGameState(moves=["up", "down"])
    node = AbstractTreeNode(game_state)

    assert not node.is_fully_expanded()  # No children yet

    node.add_child("up")
    assert not node.is_fully_expanded()  # One child added, but not fully expanded

    node.add_child("down")
    assert node.is_fully_expanded()  # Now all moves are added

# Test merging nodes
def test_merge_with():
    game_state = MockGameState(reward=5)
    root = AbstractTreeNode(game_state)
    # give the root 2 nodes to merge
    root.add_child("down")
    root.add_child("left")
    for child in root.children:
        child.visits = 10
        child.value = 10

    #make sure that there are 2 child nodes
    assert len(root.children) == 2

    #make sure that node1 has no children
    assert len(root.children[0].children) == 0

    #give child2 a child node
    root.children[1].add_child("down")

    #make sure child2 has 1 child
    assert len(root.children[1].children) == 1

    #copy of child2
    node2_copy = copy.deepcopy(root.children[1])

    #merge child1 and child2
    root.children[0].merge_with(root.children[1])

    assert root.children[0].visits == 10  # Average of visits
    assert root.children[0].value == 10  # Average of values
    assert len(root.children[0].children) == 1  # Children from node2 should be added
    assert len(root.children) == 1
    for node in root.children:
        assert node != node2_copy

# Test unmerging nodes
def test_unmerge():
    game_state = MockGameState(reward=5)
    root = AbstractTreeNode(game_state)
    # give the root 2 nodes to merge
    root.add_child("down")
    root.add_child("left")
    for child in root.children:
        child.visits = 10
        child.value = 10

    #make sure that there are 2 child nodes
    assert len(root.children) == 2

    #make sure that node1 has no children
    assert len(root.children[0].children) == 0

    #give child2 a child node
    root.children[1].add_child("down")

    #make sure child2 has 1 child
    assert len(root.children[1].children) == 1

    #copy of child2
    node2_copy = copy.deepcopy(root.children[1])

    #merge child1 and child2
    root.children[0].merge_with(root.children[1])

    assert len(root.children[0].children) == 1

    # Unmerge nodes
    root.children[0].unmerge()

    #make sure root has two children
    assert len(root.children) == 2

    #make sure child1 has no children
    assert len(root.children[0].children) == 0

    #make sure child2 has 1 child
    assert len(root.children[1].children) == 1

    #make sure node2 is back in root children
    assert node2_copy in root.children

    #make sure split child has the correct parent
    assert root.children[1].children[0].parent == root.children[1]

# Test best child selection
def test_best_child():
    game_state = MockGameState()
    node = AbstractTreeNode(game_state)
    
    # Add two children with different visits and values
    node.add_child('up')
    node.children[0].visits = 10
    node.children[0].value = 5

    node.add_child('down')
    node.children[1].visits = 20
    node.children[1].value = 10

    # Set the root node visits to calculate UCT
    node.visits = 30

    best = node.best_child()
    assert best.action[0] == 'up'  # Since 'down' has better value/visit ratio

# Test expand_tree function
def test_expand_tree():
    game_state = MockGameState(moves=["up", "down"], done=False)
    root = AbstractTreeNode(game_state)

    expand_tree(root, depth=2)

    assert len(root.children) == len(game_state.get_available_moves())
    for child in root.children:
        # if game state is done, should not expand
        if child.game_state.done:
            assert len(child.children) == 0
        else:
        # else expand
            assert len(child.children) == len(game_state.get_available_moves())


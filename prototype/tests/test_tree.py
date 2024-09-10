import pytest
from playground.utils.tree import TreeNode, expand_tree
from playground.utils.gamestate import GameState
from playground.utils.character import Player

# Mock GameState class for testing
class MockGameState(GameState):
    def __init__(self, done=False, moves=None, reward=0):
        self.done = done
        self.reward = reward
        self.moves = moves if moves is not None else ['up', 'down', 'left', 'right']
        self.turn = 0
        self.player = Player("test1", (0,0), 100)
        self.opponent = Player("opp", (12,12), 20)

    def get_available_moves(self):
        return self.moves

    def player_action(self, action):
        # Simulate a basic action
        if action == 'up':
            self.done = True  # Let's say 'up' finishes the game

    def __repr__(self):
        return f"MockGameState(done={self.done}, reward={self.reward})"

# Test TreeNode initialization
def test_treenode_initialization():
    game_state = MockGameState()
    node = TreeNode(game_state)

    assert node.game_state == game_state
    assert node.parent is None
    assert node.action is None
    assert node.visits == 0
    assert node.value == 0
    assert node.children == []

# Test is_fully_expanded
def test_is_fully_expanded():
    game_state = MockGameState(moves=['up', 'down'])
    node = TreeNode(game_state)

    assert not node.is_fully_expanded()  # No children yet

    node.add_child('up')
    assert not node.is_fully_expanded()  # One child added, not fully expanded

    node.add_child('down')
    assert node.is_fully_expanded()  # Now all moves are added

# Test add_child
def test_add_child():
    game_state = MockGameState()
    node = TreeNode(game_state)

    assert len(node.children) == 0

    node.add_child('up')
    assert len(node.children) == 1
    assert node.children[0].action == 'up'
    assert node.children[0].parent == node
    assert isinstance(node.children[0].game_state, MockGameState)

# Test pretty_print (you can verify by looking at the console output)
def test_pretty_print(capsys):
    game_state = MockGameState()
    node = TreeNode(game_state)

    node.add_child('up')
    node.add_child('down')

    node.pretty_print()

    captured = capsys.readouterr()
    assert "up" in captured.out
    assert "down" in captured.out

# Test best_child
def test_best_child():
    game_state = MockGameState()
    node = TreeNode(game_state)
    
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
    assert best.action == 'up'  # Since 'down' has better value/visit ratio

# Test expand_tree
def test_expand_tree():
    game_state = MockGameState()
    root = TreeNode(game_state)

    expand_tree(root, depth=2)

    assert len(root.children) == len(game_state.get_available_moves())
    for child in root.children:
        # if game state is done, should not expand
        if child.game_state.done:
            assert len(child.children) == 0
        else:
        # else expand
            assert len(child.children) == len(game_state.get_available_moves())

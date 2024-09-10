import pytest
from playground.utils.tree import GameState, TreeNode
from playground.agents.mcts import MCTSAgent

# Mock GameState and TreeNode to avoid full game simulation
class MockGameState(GameState):
    def __init__(self, done=False, reward=0):
        self.done = done
        self.reward = reward
        self.moves = ['up', 'down', 'left', 'right']

    def get_available_moves(self):
        return self.moves

    def player_action(self, action):
        # Randomly complete the game for testing
        if action == 'up':
            self.done = True
            self.reward = 1.0

class MockTreeNode(TreeNode):
    def __init__(self, game_state: GameState, parent=None, action=None):
        super().__init__(game_state, parent, action)
        self.visits = 0
        self.value = 0

# Test Initialization
def test_mcts_initialization():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)

    assert agent is not None
    assert agent.time_limit == 0.5
    assert isinstance(agent.root, TreeNode)

# Test Select Functionality
def test_mcts_select():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)

    selected_node = agent.select(agent.root)
    assert selected_node is not None
    assert isinstance(selected_node, TreeNode)

# Test Expansion
def test_mcts_expand():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)
    
    expanded_node = agent.expand(agent.root)
    
    assert expanded_node is not None
    assert isinstance(expanded_node, TreeNode)
    assert expanded_node.action in game_state.get_available_moves()

# Test Simulation
def test_mcts_simulate():
    game_state = MockGameState(done=False)
    agent = MCTSAgent(game_state, time_limit=0.5)

    node = agent.root
    reward = agent.simulate(node)
    
    assert reward in [0.0, 1.0]  # Since 'up' finishes the game, reward should be 1.0 or 0.0 otherwise

# Test Backpropagation
def test_mcts_backpropagate():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)

    node = agent.root
    reward = 1.0
    agent.backpropagate(node, reward)

    assert node.visits == 1
    assert node.value == 1.0

# Test Run Functionality
def test_mcts_run():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)

    actions, final_node = agent.run()

    assert isinstance(actions, list)
    assert final_node is not None
    assert isinstance(final_node, TreeNode)

# Test Best Action Sequence
def test_mcts_best_action_sequence():
    game_state = MockGameState()
    agent = MCTSAgent(game_state, time_limit=0.5)

    actions, final_node = agent.best_action_sequence()

    assert isinstance(actions, list)
    assert final_node is not None

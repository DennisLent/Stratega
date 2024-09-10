import time
import random
from playground.utils.tree import GameState, TreeNode, copy

# MCTS agent to run the game
class MCTSAgent:
    def __init__(self, game_state: GameState, time_limit=0.1):
        self.root = TreeNode(game_state)
        # given a timelimit of 100ms
        self.time_limit = time_limit 

    # run MCTS
    def run(self, debug=False) -> tuple[list, TreeNode]:
        start_time = time.time()

        while (time.time() - start_time) < self.time_limit:
            node = self.select(self.root)
            if not node.game_state.done:
                node = self.expand(node)
            reward = self.simulate(node)
            self.backpropagate(node, reward)

        return self.best_action_sequence()

    # select a node to start with
    def select(self, node: TreeNode) -> TreeNode:
        while not node.game_state.done and node.is_fully_expanded():
            node = node.best_child()
        return node

    def expand(self, node: TreeNode) -> TreeNode:
        available_moves = node.game_state.get_available_moves()
        # print(f"available moves = {available_moves}")
        tried_moves = [child.action for child in node.children]
        # print(f"tried moves = {tried_moves}")

        for move in available_moves:
            if move not in tried_moves:
                node.add_child(move)
                return node.children[-1]

    def simulate(self, node: TreeNode) -> float:
        current_state = copy.deepcopy(node.game_state)
        depth = 0
        max_depth = 5  # Limiting the simulation depth to prevent infinite loops

        while not current_state.done and depth < max_depth:
            available_moves = current_state.get_available_moves()
            action = random.choice(available_moves)
            current_state.player_action(action)
            depth += 1

        return current_state.reward

    def backpropagate(self, node: TreeNode, reward: float) -> None:
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent

    def best_action_sequence(self) -> tuple[list, TreeNode]:
        node = self.root
        actions = []
        
        while node.children:
            best_child = node.best_child(exploration_weight=0)
            actions.append(best_child.action)
            node = best_child
        
        return (actions, node)
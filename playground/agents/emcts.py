import time
import random
from utils.abstract_tree import AbstractTreeNode, GameState, copy
import numpy as np

# Elastic MCTS agent that uses approximate homomorphism
class EMCTSAgent:
    def __init__(self, game_state: GameState, time_limit=0.1, alpha_abs=100, batch_size=10, eta_r=5.0, eta_t=5.0):
        self.root = AbstractTreeNode(game_state)
        self.time_limit = time_limit
        self.alpha_abs = alpha_abs
        self.batch_size = batch_size
        self.eta_r = eta_r
        self.eta_t = eta_t
        self.iteration_count = 0
        self.state_abstraction = {}
    
    def count_nodes(self):
        visited = set()
        return self.count_nodes_recursive(self.root, visited)

    def count_nodes_recursive(self, node: AbstractTreeNode, visited: set):
        if node in visited:
            return 0
        visited.add(node)

        count = 1  # Count the current node
        for child in node.children:
            count += self.count_nodes_recursive(child, visited)
        return count
    
    def run(self, debug=False):
        start_time = time.time()

        while (time.time() - start_time) < self.time_limit:
            if debug:
                print(f"Iteration count: {self.iteration_count}")
            
            node = self.select(self.root)
            if not node.game_state.done:
                node = self.expand(node)
            reward = self.simulate(node)
            self.backpropagate(node, reward)
            self.iteration_count += 1

            if self.iteration_count % self.batch_size == 0:
                if debug:
                    print(f"Before homomorphism, node count: {self.count_nodes()}")
                self.update_abstraction()
                if debug:
                    print(f"After homomorphism, node count: {self.count_nodes()}")

            if self.iteration_count > self.alpha_abs:
                print(f"Reverting abstraction after reaching alpha_abs limit.")
                self.revert_abstraction()
                if debug:
                    print(f"After reverting abstraction, node count: {self.count_nodes()}")

        return self.best_action_sequence()

    def select(self, node: AbstractTreeNode) -> AbstractTreeNode:
        while not node.game_state.done and node.is_fully_expanded():
            node = node.best_child()
        return node

    def expand(self, node: AbstractTreeNode) -> AbstractTreeNode:
        available_moves = node.game_state.get_available_moves()
        
        # This is different thatn in the normal tree node as the actions here are a list
        # so we need to handle it appropriatly
        tried_moves = [move for child in node.children for move in child.action]

        for move in available_moves:
            if move not in tried_moves:
                node.add_child(move)
                return node.children[-1]

    def simulate(self, node: AbstractTreeNode):
        current_state = copy.deepcopy(node.game_state)
        depth = 0
        max_depth = 5 

        while not current_state.done and depth < max_depth:
            available_moves = current_state.get_available_moves()
            action = random.choice(available_moves)
            current_state.player_action(action)
            depth += 1

        return current_state.reward

    def backpropagate(self, node: AbstractTreeNode, reward: float):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent
    
    def _get_max_depth(self, node: AbstractTreeNode, current_depth=0) -> int:
        if not node.children:
            return current_depth
        return max(self._get_max_depth(child, current_depth + 1) for child in node.children)

    # main method to be called when abstracting
    def update_abstraction(self):
        # determine the maximum depth
        max_depth = self._get_max_depth(self.root)

        # we go from leaves to root
        for depth in reversed(range(max_depth + 1)):
            
            # we get all the nodes at this depth and see if we can group them
            nodes_at_depth = self._get_nodes_at_depth(depth)
            for node in nodes_at_depth:
                self._group_nodes(node, depth)
    
    def _get_nodes_at_depth(self, depth) -> list[AbstractTreeNode]:
        nodes = []
        self._collect_nodes_at_depth(self.root, depth, 0, nodes)
        return nodes

    def _collect_nodes_at_depth(self, node, target_depth, current_depth, nodes) -> list[AbstractTreeNode]:
        if current_depth == target_depth:
            nodes.append(node)
        elif current_depth < target_depth:
            for child in node.children:
                self._collect_nodes_at_depth(child, target_depth, current_depth + 1, nodes)

    def _group_nodes(self, node: AbstractTreeNode, depth: int):
        for abstract_node in self.state_abstraction.get(depth, []):
            # we merge the nodes if they are similar AND have the same parent IMPORTANT!
            print(f"{node} and {abstract_node}")
            print(f"e_r = {self._calculate_reward_error(node, abstract_node)}")
            print(f"e_t = {self._calculate_transition_error(node, abstract_node)}")
            if (self._is_similar(node, abstract_node)) and (node.parent == abstract_node.parent):
                print(f"merging node1: {node} & node2: {abstract_node}")
                abstract_node.merge_with(node)
                return

    def _is_similar(self, node1: AbstractTreeNode, node2: AbstractTreeNode):
        error_r = self._calculate_reward_error(node1, node2)
        error_t = self._calculate_transition_error(node1, node2)
        return (error_r <= self.eta_r) and (error_t <= self.eta_t)
    
    def _calculate_reward_error(self, node1: AbstractTreeNode, node2: AbstractTreeNode):
        return abs(node1.game_state.reward - node2.game_state.reward)

    def _calculate_transition_error(self, node1: AbstractTreeNode, node2: AbstractTreeNode):
        (node1_x, node1_y) = node1.game_state.player.position
        (node2_x, node2_y) = node2.game_state.player.position
        distance = np.sqrt((node1_x - node2_x) ** 2 + (node1_y - node2_y) ** 2)
        return distance

    def revert_abstraction(self):
        for node in self.get_all_nodes():
            node.unmerge()
        self.state_abstraction.clear()

    def best_action_sequence(self) -> tuple[list, AbstractTreeNode]:
        node = self.root
        actions = []
        
        while node.children:
            best_child = node.best_child(exploration_weight=0)
            actions.append(best_child.action)
            node = best_child
        
        return (actions, node)

    def _get_all_nodes(self) -> list[AbstractTreeNode]:
        all_nodes = []
        self._collect_all_nodes(self.root, all_nodes)
        return all_nodes

    def _collect_all_nodes(self, node, all_nodes):
        all_nodes.append(node)
        for child in node.children:
            self._collect_all_nodes(child, all_nodes)

import time
import random
from playground.utils.abstract_tree import AbstractTreeNode, GameState, copy
import numpy as np

# Elastic MCTS agent that uses approximate homomorphism
class EMCTSAgent:
    def __init__(self, game_state: GameState, time_limit=0.1, alpha_abs=100, batch_size=20, eta_r=0.5, eta_t=1.42):
        self.root = AbstractTreeNode(game_state)
        self.time_limit = time_limit
        self.alpha_abs = alpha_abs
        self.batch_size = batch_size
        self.eta_r = eta_r
        self.eta_t = eta_t
        self.iteration_count = 0
        self.nodes_to_merge = {}
    
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

            if (self.iteration_count > 0) and (self.iteration_count % self.batch_size) == 0:
                # print(f"going into abstraction: {self.iteration_count} {self.iteration_count % self.batch_size}")
                # print(f"Before homomorphism, node count: {self.count_nodes()}")
                self.update_abstraction()
                # print(f"After homomorphism, node count: {self.count_nodes()}")

            if self.iteration_count > self.alpha_abs:
                self.revert_abstraction()
                if debug:
                    print(f"After reverting abstraction, node count: {self.count_nodes()}")

        #at the end we have to revert the abstraction and return the best actions
        self.revert_abstraction()
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
    def update_abstraction(self) -> None:
        # determine the maximum depth
        max_depth = self._get_max_depth(self.root)

        # we go from leaves to root
        for depth in reversed(range(max_depth + 1)):
            print(f"===== DEPTH {depth} =====")
            
            # we get all the nodes at this depth and see if we can group them
            nodes_at_depth = self._get_nodes_at_depth(depth)
            # print(f"nodes at depth {depth}: {nodes_at_depth}")
            for node in nodes_at_depth:
                # we check all the nodes if we can group them
                # we remove the node we are checking for to make sure that we only group the nodes that make sense
                current_node_removed = [check_node for check_node in nodes_at_depth if check_node != node]

                self.nodes_to_merge[node] = []

                for other_node in current_node_removed:
                    # print(f"{node} and {other_node}")
                    # print(f"e_r = {self._calculate_reward_error(node, other_node)}")
                    # print(f"e_t = {self._calculate_transition_error(node, other_node)}")
                    if (self._is_similar(node, other_node)) and (node.parent == other_node.parent):
                        # print(f"merging node1: {node} & node2: {other_node}")
                        self.nodes_to_merge[node].append(other_node)
            # we now have a dictionary of nodes and nodes that it can merge with
            # now we group them based on this dictionary
            self._group_nodes()
                        
    def _get_nodes_at_depth(self, depth) -> list[AbstractTreeNode]:
        node_list = []
        self._collect_nodes_at_depth(self.root, depth, 0, node_list)
        return node_list

    def _collect_nodes_at_depth(self, node, target_depth, current_depth, node_list) -> list[AbstractTreeNode]:
        if current_depth == target_depth:
            node_list.append(node)
        elif current_depth < target_depth:
            for child in node.children:
                self._collect_nodes_at_depth(child, target_depth, current_depth + 1, node_list)

    def _group_nodes(self) -> None:

        # set of nodes to check if they have already been used
        grouped_nodes = set()

        for node in self.nodes_to_merge:
            # if this node has been grouped already, we skip it
            if node in grouped_nodes:
                continue
            
            for other_node in self.nodes_to_merge[node]:
                if other_node not in grouped_nodes and (node.parent == other_node.parent):
                    print(f"{node.parent} {other_node.parent}")
                    grouped_nodes.add(node)
                    node.merge_with(other_node)
                    grouped_nodes.add(other_node)
                    
            grouped_nodes.add(node)
        #reset nodes to merge
        self.nodes_to_merge = {}

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
        # similar to merging, we start at the bottom and unmerge
        max_depth = self._get_max_depth(self.root)

        for depth in reversed(range(max_depth + 1)):

            #get nodes at each depth
            nodes_at_depth = self._get_nodes_at_depth(depth)
            # print(f"nodes at depth {depth}: {nodes_at_depth}")
            for node in nodes_at_depth:
                #check the actions to see if the node has been merged
                node.unmerge()


    def best_action_sequence(self) -> tuple[list, AbstractTreeNode]:
        node = self.root
        actions = []
        
        while node.children:
            best_child = node.best_child(exploration_weight=0)
            actions.append(best_child.action[0])
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

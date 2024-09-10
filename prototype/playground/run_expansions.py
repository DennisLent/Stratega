import time
from utils.tree import GameState
from agents.mcts import MCTSAgent
from agents.emcts import EMCTSAgent

def run_test_case(agent_class, game_state_class, description):
    print(f"\nRunning test case: {description}")
    
    game_state = game_state_class()
    agent = agent_class(game_state, time_limit=0.5)
    
    # run a single expansion
    for i in range(25):
        node = agent.select(agent.root)
        new_node = agent.expand(node)
        reward = agent.simulate(new_node)
        agent.backpropagate(new_node, reward)
        print(f"ITERATION {i}: \n{agent.root.pretty_print()}")

        # only for EMCTS agent
        if isinstance(agent, EMCTSAgent):
            if (i>0) and (i % agent.batch_size) == 0:
                print(f"Before homomorphism, node count: {agent.count_nodes()}")
                agent.update_abstraction()
                print(f"After homomorphism, node count: {agent.count_nodes()}")
                agent.root.pretty_print()
            
            if (i == 15):
                agent.revert_abstraction()

    print(f"best actions = {agent.best_action_sequence()}")

def main():
    # Test case for regular MCTS
    run_test_case(MCTSAgent, GameState, "Standard MCTS")

    # Test case for Elastic MCTS
    run_test_case(EMCTSAgent, GameState, "Elastic MCTS with Approximate Homomorphism")

if __name__ == "__main__":
    main()

import argparse
from agents.mcts import MCTSAgent, GameState
from agents.emcts import EMCTSAgent

def main():
    parser = argparse.ArgumentParser(description="Run MCTS or EMCTS on the GameState.")
    parser.add_argument("--agent", choices=["mcts", "emcts"], default="mcts", help="Choose the agent: 'mcts' or 'emcts'.")
    parser.add_argument("--random_init", action="store_true", help="Initialize the GameState positions randomly.")
    parser.add_argument("--debug", action="store_true", help="Run with debug")
    args = parser.parse_args()

    print(f"Running {args.agent} -- random initialization {args.random_init}")

    state = GameState(random_init=args.random_init)
    runs = 1

    while not state.done:
        print(f"=============== RUN {runs} ===============")
        
        if args.agent == "mcts":
            agent = MCTSAgent(game_state=state, time_limit=0.1)
        elif args.agent == "emcts":
            agent = EMCTSAgent(game_state=state, time_limit=0.1)
        
        best_action_sequence, final_node = agent.run()
        
        print(f"Best action sequence: {best_action_sequence}")
        print(f"Best final node: {final_node}")
        
        # Apply the sequence of actions to the game state
        state = state.simulate_turns(best_action_sequence)
        
        # Print the resulting game state
        print(f"New state: {state}")
        state.print_map()
        runs += 1

if __name__ == "__main__":
    main()

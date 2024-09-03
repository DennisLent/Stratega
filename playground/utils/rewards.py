# basic heuristics function to evaluate a gamestate
def calculate_reward(game_state) -> float:
    # Reward for reducing opponent's health
    opponent_health_penalty = 20 - game_state.opponent.health  # Max damage = 20
    
    # Penalty for losing player's health
    player_health_penalty = 100 - game_state.player.health 

    # reward for getting closer to the opponent
    player_x, player_y = game_state.player.position
    opp_x, opp_y = game_state.opponent.position
    distance_to_opponent = ((player_x - opp_x) ** 2 + (player_y - opp_y) ** 2) ** 0.5
    # Maximum possible distance
    max_distance = ((12 - 0) ** 2 + (12 - 0) ** 2) ** 0.5  
    proximity_reward = (max_distance - distance_to_opponent) / max_distance * 10 
    
    # Penalty for the number of turns taken (to encourage quicker victories)
    turn_penalty = game_state.turn / 100  # Normalize to [0,1]
    
    # Bonus for winning
    if game_state.opponent.health <= 0:
        victory_bonus = 100
    else:
        victory_bonus = 0

    # Calculate the total reward
    reward = opponent_health_penalty - player_health_penalty - turn_penalty + victory_bonus + proximity_reward
    
    return reward

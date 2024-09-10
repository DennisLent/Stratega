import pytest
from playground.utils.character import Player, ATTACK_DAMAGE, MOVEMENT_LIMIT
from playground.utils.rewards import calculate_reward
from playground.utils.gamestate import GameState, MAX_TURNS
import random

# Test GameState initialization with and without random positions
def test_gamestate_initialization():
    game_state = GameState(map_size=20, random_init=False)
    
    # Check initial player and opponent positions
    assert game_state.player.position == [0,0]
    assert game_state.opponent.position == [12, 12]
    assert game_state.player.health == 100
    assert game_state.opponent.health == 20
    assert not game_state.done
    assert game_state.turn == 0

    # Check random initialization
    random_game_state = GameState(map_size=20, random_init=True)
    assert random_game_state.player.position != random_game_state.opponent.position
    assert random_game_state.turn == 0

# Test GameState equality
def test_gamestate_equality():
    game_state_1 = GameState(map_size=20, random_init=False)
    game_state_2 = GameState(map_size=20, random_init=False)

    assert game_state_1 == game_state_2

    game_state_2.player.moveUp()
    assert game_state_1 != game_state_2

# Test hash function
def test_gamestate_hash():
    game_state_1 = GameState(map_size=20, random_init=False)
    game_state_2 = GameState(map_size=20, random_init=False)

    assert hash(game_state_1) == hash(game_state_2)

    game_state_2.player.moveUp()
    assert hash(game_state_1) != hash(game_state_2)

# Test available moves when player has movement points
def test_get_available_moves_with_movement_points():
    game_state = GameState(map_size=20, random_init=False)
    
    moves = game_state.get_available_moves()
    assert "up" in moves
    assert "down" in moves
    assert "left" in moves
    assert "right" in moves
    assert "attack" not in moves  # Players are far apart, so no attack

    # Move the player closer to the opponent to test attack availability
    game_state.player.position = (11, 12)
    assert "attack" in game_state.get_available_moves()

# Test available moves when player has no movement points (turn advances)
def test_get_available_moves_no_movement_points():
    game_state = GameState(map_size=20, random_init=False)
    game_state.player.movement_points = 0

    moves = game_state.get_available_moves()
    assert "up" in moves  # After resetting, the player should regain movement points
    assert game_state.turn == 1  # Turn should have incremented

# Test player movement and actions
def test_player_actions():
    game_state = GameState(map_size=20, random_init=False)
    
    # Move up
    game_state.player_action("up")
    assert game_state.player.position == [0, 1]

    # Move down
    game_state.player_action("down")
    assert game_state.player.position == [0, 0]

    # Move left (shouldn't move because at the left boundary)
    game_state.player_action("left")
    assert game_state.player.position == [0, 0]

    # Move right
    game_state.player_action("right")
    assert game_state.player.position == [0, 0]

# Test player attack and check done state
def test_player_attack():
    game_state = GameState(map_size=20, random_init=False)

    # Place player next to opponent
    game_state.player.position = [11, 12]

    # Player attacks opponent
    game_state.player_action("attack")
    assert game_state.opponent.health == (20 - ATTACK_DAMAGE)

    # Attack until opponent dies
    game_state.player_action("attack")
    game_state.player_action("attack")  # Assuming ATTACK_DAMAGE is 10, the opponent should now be dead

    assert game_state.opponent.health <= 0
    assert game_state.done  # Game should be marked as done

# Test simulate_turns
def test_simulate_turns():
    game_state = GameState(map_size=20, random_init=False)
    actions = ["up", "up", "right", "attack"]

    # Move player closer and simulate attack
    game_state.player.position = [11, 12]
    
    new_game_state = game_state.simulate_turns(actions)

    # Ensure the original state is unchanged
    assert game_state.player.position == [11, 12]

    # Ensure the new game state reflects the actions
    assert new_game_state.player.position == [12, 14]
    assert new_game_state.opponent.health == (20 - ATTACK_DAMAGE)

# Test can_attack
def test_can_attack():
    game_state = GameState(map_size=20, random_init=False)
    
    # Far away from opponent
    assert not game_state.can_attack()

    # Move player next to opponent
    game_state.player.position = (11, 12)
    assert game_state.can_attack()

# Test check_done
def test_check_done():
    game_state = GameState(map_size=20, random_init=False)

    # Check done when player dies
    game_state.player.health = 0
    game_state.check_done()
    assert game_state.done

    # Reset and check done when opponent dies
    game_state = GameState(map_size=20, random_init=False)
    game_state.opponent.health = 0
    game_state.check_done()
    assert game_state.done

    # Check done after max turns
    game_state = GameState(map_size=20, random_init=False)
    game_state.turn = MAX_TURNS
    game_state.check_done()
    assert game_state.done

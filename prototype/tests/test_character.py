import pytest
from playground.utils.character import Player

def test_init():
    player = Player("test", (0,0), 100)
    assert(player.name == "test")
    assert(player.health == 100)
    assert(player.position[0] == 0)
    assert(player.position[1] == 0)

def test_moveUp():
    player = Player("test", (0,0), 100)
    player.moveUp()
    assert(player.position == [0, 1])

def test_moveDown():
    player = Player("test", (0,0), 100)
    player.moveDown()
    assert(player.position == [0, -1])

def test_moveLeft():
    player = Player("test", (0,0), 100)
    player.moveLeft()
    assert(player.position == [-1, 0])

def test_moveRight():
    player = Player("test", (0,0), 100)
    player.moveRight()
    assert(player.position == [1, 0])
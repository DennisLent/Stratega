from utils.gamestate import GameState
from utils.abstract_tree import AbstractTreeNode, expand_tree  # Assuming the classes are in abstract_tree.py

def test_tree_creation():
    """Test the basic creation and expansion of the tree."""
    print("=== Test Tree Creation ===")
    root_state = GameState()
    root = AbstractTreeNode(game_state=root_state)

    expand_tree(root, depth=1)  # Expand the tree to depth 2
    root.pretty_print()
    print()

def test_merge_nodes():
    """Test merging of nodes."""
    print("=== Test Merging Nodes ===")
    root_state = GameState()
    root = AbstractTreeNode(game_state=root_state)
    
    expand_tree(root, depth=1)  # Expand the tree to depth 1

    # Manually create two child nodes with the same parent and merge them
    child1 = root.children[0]
    child3 = root.children[3]

    # Assign some arbitrary visits and values
    child1.visits = 10
    child1.value = 50
    child3.visits = 20
    child3.value = 70

    print("Before merging:")
    root.pretty_print()

    # Merge the two nodes
    child1.merge_with(child3)

    print("\nAfter merging:")
    root.pretty_print()
    print()

def test_unmerge_nodes():
    """Test unmerging of nodes."""
    print("=== Test Unmerging Nodes ===")
    root_state = GameState()
    root = AbstractTreeNode(game_state=root_state)
    
    expand_tree(root, depth=1)  # Expand the tree to depth 1

    # Manually create two child nodes with the same parent and merge them
    child1 = root.children[0]
    child3 = root.children[3]

    # Assign some arbitrary visits and values
    child1.visits = 10
    child1.value = 50
    child3.visits = 20
    child3.value = 70

    print("Before merging:")
    root.pretty_print()

    # Merge the two nodes
    child1.merge_with(child3)

    print("\nAfter merging:")
    root.pretty_print()

    # Now unmerge
    child1.unmerge()

    print("\nAfter unmerging:")
    root.pretty_print()
    print()

def run_all_tests():
    test_tree_creation()
    test_merge_nodes()
    test_unmerge_nodes()

if __name__ == "__main__":
    run_all_tests()

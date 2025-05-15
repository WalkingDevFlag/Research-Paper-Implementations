```markdown
# Python Radix Tree Implementation

This repository contains a Python implementation of a Radix Tree (also known as a Patricia Trie or compact prefix tree). A Radix Tree is a space-optimized trie data structure that stores string keys efficiently. Nodes with only one child are merged with that child, resulting in edges labeled with sequences of characters rather than single characters.

This implementation is designed for clarity of the core algorithms, making it suitable for educational purposes and as a foundation for understanding more complex trie-based structures.

## Features

*   **String Key Storage:** Efficiently stores and retrieves values associated with string keys.
*   **Insertion:** Supports adding new key-value pairs. If a key already exists, its value is updated. Handles node splitting and path compression automatically.
*   **Search:** Allows searching for keys to retrieve their associated values.
*   **Deletion:** Supports removing keys from the tree. Includes logic for node merging and path compaction to maintain Radix Tree properties.
*   **Prefix Search (`starts_with`):** Finds all keys in the tree that begin with a given prefix, useful for autocomplete-like functionality.
*   **Type Hinting:** Code includes type hints for better readability and static analysis.
*   **Visualization:** A `display_structure` method is provided to print a representation of the tree's structure, showing stored keys and the segments of nodes.

## File Structure

*   `radix_tree.py`: Contains the Python implementation of `RadixTreeNode` and `RadixTree` classes, along with a demonstration function.

## Core Concepts of Radix Tree (Implemented)

1.  **Node Structure (`RadixTreeNode`):**
    *   `key_segment`: The string segment on the edge leading to this node.
    *   `value`: The value stored if this node marks the end of a complete key.
    *   `is_end_of_key`: A boolean flag indicating if a key terminates at this node.
    *   `children`: A dictionary mapping the first character of a child's `key_segment` to the child `RadixTreeNode` object.

2.  **Insertion Logic:**
    *   Traverse the tree based on matching prefixes of the key being inserted and the `key_segment`s of child nodes.
    *   If a full `key_segment` is matched, move to the child.
    *   If a partial `key_segment` is matched (LCP - Longest Common Prefix), split the existing child node:
        *   An intermediate node is created for the LCP.
        *   The original child becomes a child of this intermediate node, with its `key_segment` updated to the remaining suffix.
        *   The new key's remaining suffix (if any) forms another branch from the intermediate node.
    *   If no child matches the current part of the key, create a new child node with the remaining key segment.

3.  **Deletion Logic:**
    *   Locate the node corresponding to the key.
    *   Mark the node as `is_end_of_key = False` and clear its `value`.
    *   Perform **compaction** upwards from the parent of the deleted key's node:
        *   If a node is not an endpoint for another key and has no children, remove it from its parent.
        *   If a node is not an endpoint and has only one child, merge it with that child (combine their `key_segment`s and update the parent's pointer).

4.  **Prefix Search (`starts_with`):**
    *   Traverse the tree to the node where the given prefix path ends (or is contained within an edge).
    *   Perform a Depth-First Search (DFS) from that node to collect all keys in its subtree.

## How to Use

1.  **Clone the repository or save `radix_tree.py`.**
2.  **Import the `RadixTree` class:**
    ```python
    from radix_tree import RadixTree
    ```
3.  **Create an instance of the RadixTree:**
    ```python
    rt = RadixTree()
    ```
4.  **Use the methods:**
    ```python
    # Insert key-value pairs
    rt.insert("apple", 10)
    rt.insert("apply", 20)
    rt.insert("apricot", 30)
    rt.insert("banana", 40)

    # Search for a key
    value = rt.search("apple")
    print(f"Value for 'apple': {value}") # Output: 10

    # Find keys starting with a prefix
    prefix_matches = rt.starts_with("ap")
    print(f"Keys starting with 'ap': {prefix_matches}") # Output: ['apple', 'apply', 'apricot'] (order may vary before sorting)

    # Delete a key
    rt.delete("apply")
    print(f"Search for 'apply' after deletion: {rt.search('apply')}") # Output: None

    # Display the tree structure
    rt.display_structure()
    ```

## Running the Demonstration

The `radix_tree.py` file includes a `demonstration_indian_names()` function that showcases the tree's functionalities using a sample dataset of Indian names. You can run this directly:

```bash
python radix_tree.py
```

This will output the steps of insertion, searching, prefix searching, deletion, and display the tree structure at various stages.

## For Memorization / Understanding the Core Algorithm

To best understand and memorize the Radix Tree operations, focus on:

*   **`insert` method:** Pay close attention to the logic for finding the Longest Common Prefix (LCP) and the three main cases:
    1.  No matching child: Create a new child.
    2.  Full segment match with a child: Descend into the child.
    3.  Partial segment match with a child: Split the child node by creating an intermediate node.
*   **`delete` method:** Understand the two main parts:
    1.  Locating the node and unmarking it as an end-of-key.
    2.  The `_compact_path_after_delete` helper, which handles merging single-child intermediate nodes or removing unnecessary leaf nodes by traversing upwards.
*   **Node Structure:** How `key_segment`, `value`, `is_end_of_key`, and `children` work together.
*   **Path Compression:** The core idea that edges represent sequences of characters (segments) rather than single characters, achieved by merging nodes that would otherwise have only one child.

The provided code attempts to keep these core logic parts explicit and readable.

## Potential Further Optimizations (Beyond this Scope)

For extreme performance in a production system (e.g., low-level networking or large-scale databases), Radix Trees might be implemented in C/C++/Rust or use more advanced memory management techniques. However, this Python implementation serves as an excellent way to learn and prototype.
```
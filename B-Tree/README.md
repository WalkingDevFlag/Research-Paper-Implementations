# B-Tree Implementation in Python

## Overview

This Python script provides a comprehensive implementation of a B-Tree data structure. A B-Tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time. B-Trees are particularly well-suited for storage systems that read and write large blocks of data, such as databases and file systems, because they minimize disk I/O operations due to their high fanout (nodes can have many children).

## Purpose of this Script

The primary goal of this script is to demonstrate the core operations of a B-Tree:
*   **Insertion:** Adding new key-value pairs, including logic for splitting nodes when they become full.
*   **Search:** Efficiently finding values associated with specific keys.
*   **Deletion:** Removing key-value pairs, including complex rebalancing logic such as borrowing keys from sibling nodes or merging nodes to maintain B-Tree properties.

This demonstration uses an in-memory "Employee Database" where employee records are indexed by their `emp_id` using the B-Tree.

## Key Features Implemented

*   **`BTreeNode` Class:** Represents a node in the B-Tree. Each node stores:
    *   A list of keys.
    *   A list of associated values (`vals`).
    *   A list of child node pointers (`children`).
    *   A boolean flag (`leaf`) indicating if it's a leaf node.
    *   The minimum degree `t` of the B-Tree.
*   **`BTree` Class:** Represents the B-Tree itself, managing the root node and overall tree operations.
*   **Insertion (`insert`):**
    *   Handles insertion into non-full nodes.
    *   Implements node splitting when a node overflows, causing the tree to grow in height if the root splits.
*   **Search (`search`):**
    *   Efficiently locates a key by traversing the tree.
*   **Deletion (`delete`):**
    *   Handles deletion from leaf and internal nodes.
    *   Implements rebalancing strategies:
        *   **Borrowing:** If a node underflows after deletion, it attempts to borrow a key from an adjacent sibling node (left or right).
        *   **Merging:** If borrowing is not possible, the underfull node is merged with a sibling and a key from the parent node.
    *   Manages changes in tree height if the root node becomes empty and has only one child.
*   **Employee Database Simulation:**
    *   A simple `Employee` dataclass to store employee data.
    *   An `EmployeeDB` class that uses the `BTree` to manage an index of employees.

## Structure of the Code

The script is contained in a single Python file and includes:

1.  **`BTreeNode` Class:** Contains all logic for node-level operations (search within a node, splitting, handling keys/values/children, deletion rebalancing logic like borrowing and merging).
2.  **`BTree` Class:** Manages the `root` of the tree and provides the main interface for `insert`, `search`, and `delete` operations. It handles root-specific cases like splitting the root or shrinking the tree.
3.  **`Employee` Dataclass & `EmployeeDB` Class:** A simple application layer to demonstrate the B-Tree's usage.
4.  **`demo()` Function:** Sets up an `EmployeeDB`, adds employees, performs searches, deletes employees (showcasing various scenarios including emptying the tree), and prints the B-Tree structure at different stages.

## How to Run

1.  Save the code as a Python file (e.g., `btree_script.py`).
2.  Run it from your terminal:
    ```bash
    python btree_script.py
    ```
    The script will print the actions being performed (additions, deletions) and the structure of the B-Tree at various points.

## Customization

*   **B-Tree Degree (`t`):** The minimum degree `t` of the B-Tree can be changed when creating an `EmployeeDB` instance (e.g., `db = EmployeeDB(t_degree=3)`).
    *   `t` determines the node capacity:
        *   Minimum keys per node (except root): `t-1`
        *   Maximum keys per node: `2t-1`
    *   A smaller `t` (like `t=2`, which forms a 2-3-4 tree) makes structural changes (splits, merges) more frequent and easier to observe in the demonstration. Larger `t` values result in wider, shallower trees, which is beneficial for disk-based systems.
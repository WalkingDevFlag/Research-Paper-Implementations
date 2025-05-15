# ----------------------------------------------------------------------------------
# Radix Tree (Patricia Trie) Implementation and Demonstration
#
# Problem:
# This script demonstrates a Python implementation of a Radix Tree.
# A Radix Tree is a space-optimized trie where nodes with only one child are
# merged, resulting in edges labeled with sequences of characters. It's
# efficient for storing and searching string keys, especially for tasks like
# autocomplete or IP routing.
#
# The demonstration uses Indian names as keys in a simple key-value store,
# showcasing insertion, search, deletion, and prefix-based searching.
#
# Aim:
# The code aims for clarity of the core Radix Tree algorithms to aid understanding
# and memorization, while incorporating type hints and good Python practices
# suitable for a foundational "production-quality" understanding.
# ----------------------------------------------------------------------------------

from typing import Dict, Optional, Any, Tuple, List, Iterator

class RadixTreeNode:
    """Represents a node in the Radix Tree."""
    def __init__(self, key_segment: str = ""):
        self.key_segment: str = key_segment  # Segment of the key on the edge leading to this node
        self.value: Optional[Any] = None     # Value associated if this node marks the end of a key
        self.is_end_of_key: bool = False     # True if a key explicitly ends at this node
        self.children: Dict[str, RadixTreeNode] = {}  # Maps 1st char of child's segment to child node

    def __repr__(self) -> str:
        return (f"Node(seg='{self.key_segment}', value_exists={self.value is not None}, "
                f"is_end={self.is_end_of_key}, num_children={len(self.children)})")

class RadixTree:
    """
    Radix Tree implementation supporting string keys.
    Allows insertion, search, deletion, and prefix-based queries.
    """
    def __init__(self):
        self.root: RadixTreeNode = RadixTreeNode()

    def insert(self, key: str, value: Any) -> None:
        """
        Inserts a key-value pair into the Radix Tree.
        If the key already exists, its value is updated.
        """
        if not key:
            raise ValueError("Empty string cannot be used as a key.")

        current_node: RadixTreeNode = self.root
        remaining_key: str = key

        while True:
            if not remaining_key:  # Entire key has been processed
                current_node.value = value
                current_node.is_end_of_key = True
                return

            first_char_remaining: str = remaining_key[0]
            child_node: Optional[RadixTreeNode] = current_node.children.get(first_char_remaining)

            if not child_node:
                # No child starts with this character, create a new child with the rest of the key
                new_node = RadixTreeNode(key_segment=remaining_key)
                new_node.value = value
                new_node.is_end_of_key = True
                current_node.children[first_char_remaining] = new_node
                return

            # A child node exists, compare segments
            child_segment: str = child_node.key_segment
            lcp_len: int = 0  # Length of Longest Common Prefix
            for i in range(min(len(remaining_key), len(child_segment))):
                if remaining_key[i] == child_segment[i]:
                    lcp_len += 1
                else:
                    break
            
            if lcp_len == len(child_segment):
                # The child's segment is a prefix of (or equals) remaining_key.
                # Traverse to this child and continue with the rest of remaining_key.
                current_node = child_node
                remaining_key = remaining_key[lcp_len:]
            else:
                # Partial match: the child_segment needs to be split.
                # old_child_segment_prefix is the common part, e.g., "app"
                # old_child_segment_suffix is what remains of original child's segment, e.g., "le" from "apple"
                
                intermediate_node_segment: str = child_segment[:lcp_len]
                old_child_new_segment: str = child_segment[lcp_len:]

                # Create new intermediate node for the common prefix
                intermediate_node = RadixTreeNode(key_segment=intermediate_node_segment)
                current_node.children[first_char_remaining] = intermediate_node # Parent points to new intermediate

                # The original child_node becomes a child of intermediate_node
                child_node.key_segment = old_child_new_segment
                intermediate_node.children[old_child_new_segment[0]] = child_node

                # Handle the part of the inserted key that extends beyond the common prefix
                suffix_of_inserted_key: str = remaining_key[lcp_len:]
                if not suffix_of_inserted_key:
                    # Inserted key ends exactly at the new intermediate_node (e.g., inserting "app")
                    intermediate_node.value = value
                    intermediate_node.is_end_of_key = True
                else:
                    # Inserted key has a further suffix (e.g., inserting "apply", suffix "ly")
                    new_suffix_node = RadixTreeNode(key_segment=suffix_of_inserted_key)
                    new_suffix_node.value = value
                    new_suffix_node.is_end_of_key = True
                    intermediate_node.children[suffix_of_inserted_key[0]] = new_suffix_node
                return

    def search(self, key: str) -> Optional[Any]:
        """
        Searches for a key in the Radix Tree.
        Returns the associated value if the key is found, otherwise None.
        """
        if not key: return None # Or handle root value if it can store one.

        current_node: RadixTreeNode = self.root
        remaining_key: str = key

        while True:
            if not remaining_key: # Entire search key has been processed
                return current_node.value if current_node.is_end_of_key else None

            first_char_remaining: str = remaining_key[0]
            child_node: Optional[RadixTreeNode] = current_node.children.get(first_char_remaining)

            if not child_node:
                return None  # No path matches the remaining key

            child_segment: str = child_node.key_segment
            if remaining_key.startswith(child_segment):
                # Full segment match, continue traversal
                current_node = child_node
                remaining_key = remaining_key[len(child_segment):]
            else:
                # Segment mismatch (e.g., search "apricot", child_segment="apple")
                return None
    
    def delete(self, key: str) -> bool:
        """
        Deletes a key (and its associated value) from the Radix Tree.
        Returns True if the key was successfully deleted, False otherwise.
        """
        if not key: return False 

        # Path stores tuples of (parent_node, char_key_in_parent_children_dict, current_child_node)
        path: List[Tuple[RadixTreeNode, str, RadixTreeNode]] = [] 
        current_node: RadixTreeNode = self.root
        remaining_key: str = key

        # Step 1: Find the node corresponding to the key to be deleted
        while True:
            if not remaining_key: # Reached the node where the key should end
                if current_node.is_end_of_key:
                    current_node.is_end_of_key = False # Mark as no longer end of a key
                    current_node.value = None          # Remove the value
                    self._compact_path_after_delete(path) # Perform compaction if needed
                    return True
                else:
                    return False # Key exists as a prefix/path, but not as a stored key

            first_char_remaining: str = remaining_key[0]
            child_node: Optional[RadixTreeNode] = current_node.children.get(first_char_remaining)

            if not child_node:
                return False # Key not found

            child_segment: str = child_node.key_segment
            if remaining_key.startswith(child_segment):
                path.append((current_node, first_char_remaining, child_node))
                current_node = child_node
                remaining_key = remaining_key[len(child_segment):]
            else:
                return False # Key not found (mismatch in segment)

    def _compact_path_after_delete(self, path: List[Tuple[RadixTreeNode, str, RadixTreeNode]]) -> None:
        """
        Helper method to compact nodes upwards along the path after a key is deleted.
        Merges nodes with a single child that are not key endpoints, and removes leaf nodes
        that are not key endpoints.
        """
        # Iterate from the parent of the (logically) deleted key's node up to the root's child
        for i in range(len(path) - 1, -1, -1):
            parent_node, char_leading_to_node, node_to_compact = path[i]

            # If node_to_compact is still an endpoint for another key OR has multiple children,
            # it's a significant node. No further compaction needed for this node itself or its ancestors on this path.
            if node_to_compact.is_end_of_key or len(node_to_compact.children) > 1:
                return # Stop compaction for this branch

            if len(node_to_compact.children) == 0:
                # Node is now a non-terminating "leaf" (no value, no children). Remove it from its parent.
                del parent_node.children[char_leading_to_node]
            
            elif len(node_to_compact.children) == 1:
                # Node is a non-terminating passthrough node with only one child. Merge it with that child.
                # sole_child_node = list(node_to_compact.children.values())[0] # Alternative
                sole_child_node: RadixTreeNode = next(iter(node_to_compact.children.values()))
                
                # The new segment for the sole_child_node is its original segment prepended with node_to_compact's segment.
                sole_child_node.key_segment = node_to_compact.key_segment + sole_child_node.key_segment
                
                # Parent_node now points directly to sole_child_node.
                # The key in parent_node.children (char_leading_to_node) remains the same,
                # as it's the first character of the (now combined) segment.
                parent_node.children[char_leading_to_node] = sole_child_node
            # If we reached here, parent_node was modified, continue up the path to check parent_node

    def starts_with(self, prefix: str) -> List[str]:
        """
        Returns a list of all keys in the tree that start with the given prefix.
        """
        results: List[str] = []
        if not prefix: # If prefix is empty, return all keys
            self._dfs_collect_keys(self.root, "", results)
            return results

        current_node: RadixTreeNode = self.root
        remaining_prefix: str = prefix
        # base_path_to_prefix_node is the full string from root to current_node
        base_path_to_prefix_node: str = "" 

        # Traverse to the node where the prefix path ends or is contained within an edge
        while remaining_prefix:
            first_char_of_rem_prefix: str = remaining_prefix[0]
            child_node: Optional[RadixTreeNode] = current_node.children.get(first_char_of_rem_prefix)

            if not child_node: 
                return [] # Prefix does not exist in the tree

            child_segment: str = child_node.key_segment

            if remaining_prefix.startswith(child_segment):
                # Prefix consumes the entire child segment, move to child
                base_path_to_prefix_node += child_segment
                remaining_prefix = remaining_prefix[len(child_segment):]
                current_node = child_node
            elif child_segment.startswith(remaining_prefix):
                # Child segment contains the rest of the prefix (e.g., prefix "ap", segment "apple")
                # The prefix path effectively ends "on" this edge. Collection starts from this child_node.
                base_path_to_prefix_node += child_segment 
                current_node = child_node 
                remaining_prefix = "" # Prefix fully matched within this segment
                break 
            else: # Mismatch, prefix not found
                return []
        
        # Collect all keys from current_node downwards
        self._dfs_collect_keys(current_node, base_path_to_prefix_node, results)
        return results

    def _dfs_collect_keys(self, node: RadixTreeNode, current_path_str: str, results_list: List[str]) -> None:
        """
        Performs a Depth-First Search from 'node' to collect all keys.
        'current_path_str' is the full string from the tree root to 'node'.
        """
        if node.is_end_of_key:
            results_list.append(current_path_str)
        
        for child_segment_start_char, child_node in node.children.items():
            # The path to the child is the current node's path + the child's own edge segment
            self._dfs_collect_keys(child_node, current_path_str + child_node.key_segment, results_list)

    def display_structure(self) -> None:
        """Prints a representation of the Radix Tree's structure and stored keys."""
        print("\nRadix Tree Structure (Key: Value, Node's own edge segment):")
        if not self.root.children and not self.root.is_end_of_key:
            print("  Tree is empty.")
            return
        self._display_recursive(self.root, "")

    def _display_recursive(self, node: RadixTreeNode, accumulated_key_to_node: str) -> None:
        """
        Recursive helper for display_structure.
        'accumulated_key_to_node' is the full string from root to 'node'.
        """
        # Root node itself doesn't have an "incoming edge segment" in the same way other nodes do.
        # Its key_segment is "", and accumulated_key_to_node is "" for the root.
        is_root = (node == self.root)
        
        if node.is_end_of_key:
            key_display = accumulated_key_to_node if accumulated_key_to_node else "(root for empty key)"
            print(f"  Key: '{key_display}', Value: {node.value} (Node segment: '{node.key_segment}')")
        elif not is_root: # Print intermediate path nodes (not keys themselves)
             print(f"  PathNode: '{accumulated_key_to_node}' (Node segment: '{node.key_segment}')")

        for child_char, child_node in sorted(node.children.items()):
            self._display_recursive(child_node, accumulated_key_to_node + child_node.key_segment)


# --- Demonstration with Indian Names ---
def demonstration_indian_names():
    print("--- Radix Tree Demonstration with Indian Names ---")
    rt = RadixTree()

    print("\n--- Inserting keys (Indian Names) ---")
    # Using a dictionary for key-value pairs to ensure unique keys for insertion
    names_data = {
        "Priya": 101, "Priyanka": 102, "Prisha": 103, "Pri": 100, # Added "Pri"
        "Rohan": 201, "Rohit": 202, "Rohini": 203,
        "Ananya": 301, "Anjali": 302, "Anand": 303, "Anil": 304, "An": 300, # Added "An"
        "Suresh": 401, "Suraj": 402, "Sunita": 403, "Suman": 404,
        "Vikram": 501, "Vikas": 502, "Vinay": 503, "Vidya": 504,
        "Raj": 601, "Ram": 602, "Dev": 603, "Deepa": 604
    }
    for name, id_val in names_data.items():
        rt.insert(name, id_val)
        print(f"Inserted '{name}': {id_val}")

    rt.display_structure()

    print("\n--- Searching keys ---")
    search_terms = ["Priyanka", "Rohit", "Anand", "An", "Pri", "Suresh", "Vik", "Anan", "Mohan", "Raj"]
    for term in search_terms:
        result = rt.search(term)
        print(f"Search for '{term}': {'Found, value = ' + str(result) if result is not None else 'Not found'}")

    print("\n--- Prefix Searching (startsWith) ---")
    prefixes = ["Pri", "Ro", "An", "Su", "Vi", "Deep", "Rama", "Xyz"]
    for p in prefixes:
        matches = sorted(rt.starts_with(p)) # Sort for consistent output
        print(f"Keys starting with '{p}': {matches}")

    print("\n--- Deleting keys ---")
    keys_to_delete = ["Rohini", "Anjali", "Suman", "NonExistent", "Raj", "Pri"]
    for k_del in keys_to_delete:
        if rt.delete(k_del):
            print(f"Deleted '{k_del}' successfully.")
        else:
            print(f"Failed to delete '{k_del}' (not found or already deleted).")
    
    print("\n--- Tree Structure after deletions (All Stored Keys via starts_with) ---")
    all_keys_after_delete = sorted(rt.starts_with(""))
    print("All keys in tree after deletions:", all_keys_after_delete)
    # rt.display_structure() # Optionally display detailed structure

    print("\n--- Searching after deletions ---")
    search_after_delete = ["Rohini", "Anjali", "Priya", "Pri", "Suresh", "Raj", "An"]
    for term in search_after_delete:
        result = rt.search(term)
        print(f"Search for '{term}' post-delete: {'Found, value = ' + str(result) if result is not None else 'Not found'}")
        
    print("\n--- Test edge case: re-inserting existing key / inserting prefix key ---")
    rt.insert("Priya", 999) 
    print(f"Search for 'Priya' after re-insert with new value: {rt.search('Priya')}")
    
    # "An" was deleted implicitly if it was just a path node, or explicitly if it was a key.
    # Re-inserting "An" to test:
    rt.insert("An", 888) 
    print(f"Search for 'An' after re-insert: {rt.search('An')}")
    
    rt.display_structure()


if __name__ == "__main__":
    demonstration_indian_names()


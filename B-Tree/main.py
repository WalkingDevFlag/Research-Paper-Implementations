# ----------------------------------------------------------------------------------
# B-Tree Implementation and Demonstration
#
# Problem:
# This script demonstrates a B-Tree data structure, used here for an in-memory
# index of an "Employee Database". It showcases efficient sorted data management,
# including insertions, deletions, and searches.
#
# Features Demonstrated:
# 1. B-Tree Node (keys, values, children, leaf status).
# 2. Insertion with node splitting.
# 3. Search.
# 4. Deletion with rebalancing (borrowing/merging).
# 5. Root management and height changes.
# 6. A simple Employee Database using the B-Tree for indexing.
# ----------------------------------------------------------------------------------

import bisect
from dataclasses import dataclass # For simpler Employee class

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Minimum degree
        self.leaf = leaf
        self.keys = []
        self.vals = [] # Shortened from values
        self.children = []

    def traverse(self, level=0, prefix="R:"): # Shortened prefix
        indent = "  " * level
        print(f"{indent}{prefix} {self.keys} L:{self.leaf}")
        if not self.leaf:
            for i, child in enumerate(self.children):
                child.traverse(level + 1, f"C{i}:")

    def search(self, k):
        i = bisect.bisect_left(self.keys, k)
        if i < len(self.keys) and self.keys[i] == k:
            return self.vals[i]
        return None if self.leaf else self.children[i].search(k)

    def insert_non_full(self, k, v):
        i = bisect.bisect_right(self.keys, k)
        if self.leaf:
            self.keys.insert(i, k)
            self.vals.insert(i, v)
        else:
            if len(self.children[i].keys) == (2 * self.t - 1):
                self.split_child(i) # Pass only index
                if k > self.keys[i]:
                    i += 1
            self.children[i].insert_non_full(k, v)

    def split_child(self, i): # Child y is self.children[i]
        y = self.children[i]
        z = BTreeNode(self.t, y.leaf) # New sibling node
        median_idx = self.t - 1
        
        self.keys.insert(i, y.keys[median_idx])
        self.vals.insert(i, y.vals[median_idx])
        
        z.keys = y.keys[self.t:]
        z.vals = y.vals[self.t:]
        y.keys = y.keys[:median_idx]
        y.vals = y.vals[:median_idx]
        
        if not y.leaf:
            z.children = y.children[self.t:]
            y.children = y.children[:self.t]
            
        self.children.insert(i + 1, z)

    def delete(self, k):
        idx = bisect.bisect_left(self.keys, k)

        if idx < len(self.keys) and self.keys[idx] == k: # Key k is in this node
            if self.leaf: self._remove_from_leaf(idx)
            else: self._remove_from_non_leaf(idx, k) # Pass k for clarity in recursive delete
        else: # Key k is not in this node, so it's in a child
            if self.leaf: return # Key not found

            target_child_idx = idx
            if len(self.children[target_child_idx].keys) < self.t:
                self._ensure_child_has_min_keys(target_child_idx)
            
            # Recurse on the appropriate child.
            # If _ensure_child_has_min_keys merged target_child_idx with its left sibling,
            # the effective index for recursion might shift. This condition handles it.
            if target_child_idx > len(self.keys): 
                self.children[target_child_idx - 1].delete(k)
            else:
                self.children[target_child_idx].delete(k)

    def _remove_from_leaf(self, idx):
        self.keys.pop(idx)
        self.vals.pop(idx)

    def _remove_from_non_leaf(self, idx, k_orig): # k_orig is the key to be deleted from tree
        # k_this_node = self.keys[idx] # Key in current node (which is k_orig)
        
        l_child, r_child = self.children[idx], self.children[idx+1]

        if len(l_child.keys) >= self.t: # Case 2a: l_child has enough keys
            pred_k, pred_v = self._get_pred(idx)
            self.keys[idx], self.vals[idx] = pred_k, pred_v
            l_child.delete(pred_k)
        elif len(r_child.keys) >= self.t: # Case 2b: r_child has enough keys
            succ_k, succ_v = self._get_succ(idx)
            self.keys[idx], self.vals[idx] = succ_k, succ_v
            r_child.delete(succ_k)
        else: # Case 2c: Both children have t-1 keys, merge them
            # Move key from self and all of r_child into l_child
            l_child.keys.append(self.keys.pop(idx))
            l_child.vals.append(self.vals.pop(idx))
            l_child.keys.extend(r_child.keys)
            l_child.vals.extend(r_child.vals)
            if not r_child.leaf: l_child.children.extend(r_child.children)
            
            self.children.pop(idx + 1) # Remove r_child
            l_child.delete(k_orig) # k_orig is now in l_child

    def _get_pred(self, idx):
        curr = self.children[idx]
        while not curr.leaf: curr = curr.children[-1]
        return curr.keys[-1], curr.vals[-1]

    def _get_succ(self, idx):
        curr = self.children[idx+1]
        while not curr.leaf: curr = curr.children[0]
        return curr.keys[0], curr.vals[0]

    def _ensure_child_has_min_keys(self, child_idx):
        # Checks if self.children[child_idx] is underfull (has t-1 keys).
        # If so, borrows or merges to give it at least t keys.
        l_sib_idx, r_sib_idx = child_idx - 1, child_idx + 1

        if child_idx != 0 and len(self.children[l_sib_idx].keys) >= self.t:
            self._borrow_from_left(child_idx)
        elif child_idx != len(self.children)-1 and len(self.children[r_sib_idx].keys) >= self.t:
            self._borrow_from_right(child_idx)
        else: # Merge
            if child_idx != 0: self._merge(child_idx - 1) # Merge with left sibling
            else: self._merge(child_idx) # Merge with right sibling

    def _borrow_from_left(self, child_idx):
        child, l_sib = self.children[child_idx], self.children[child_idx-1]
        parent_key_idx = child_idx - 1
        
        child.keys.insert(0, self.keys[parent_key_idx])
        child.vals.insert(0, self.vals[parent_key_idx])
        self.keys[parent_key_idx], self.vals[parent_key_idx] = l_sib.keys.pop(), l_sib.vals.pop()
        if not l_sib.leaf: child.children.insert(0, l_sib.children.pop())

    def _borrow_from_right(self, child_idx):
        child, r_sib = self.children[child_idx], self.children[child_idx+1]
        parent_key_idx = child_idx
        
        child.keys.append(self.keys[parent_key_idx])
        child.vals.append(self.vals[parent_key_idx])
        self.keys[parent_key_idx], self.vals[parent_key_idx] = r_sib.keys.pop(0), r_sib.vals.pop(0)
        if not r_sib.leaf: child.children.append(r_sib.children.pop(0))

    def _merge(self, merge_initiator_idx): # merge_initiator_idx is index of key in parent that moves down
        # Merges children[initiator_idx] and children[initiator_idx+1]
        l_child, r_child = self.children[merge_initiator_idx], self.children[merge_initiator_idx+1]
        
        l_child.keys.append(self.keys.pop(merge_initiator_idx))
        l_child.vals.append(self.vals.pop(merge_initiator_idx))
        l_child.keys.extend(r_child.keys)
        l_child.vals.extend(r_child.vals)
        if not r_child.leaf: l_child.children.extend(r_child.children)
        
        self.children.pop(merge_initiator_idx + 1)

class BTree:
    def __init__(self, t):
        if t < 2: raise ValueError("B-Tree degree 't' must be at least 2")
        self.root = BTreeNode(t, leaf=True)
        self.t = t

    def traverse(self):
        if self.root and self.root.keys: self.root.traverse()
        else: print("Tree is empty.")

    def search(self, k):
        return self.root.search(k) if self.root else None

    def insert(self, k, v):
        r = self.root
        if len(r.keys) == (2 * self.t - 1):
            s = BTreeNode(self.t, leaf=False)
            s.children.insert(0, r)
            s.split_child(0) # s is parent, old root r is child 0 of s
            
            i = 0
            if s.keys[0] < k: i += 1
            s.children[i].insert_non_full(k, v)
            self.root = s
        else:
            r.insert_non_full(k, v)

    def delete(self, k):
        if not self.root or not self.root.keys : # Check if tree is empty
            # print(f"Key {k} not found or tree empty.")
            return

        self.root.delete(k)
        if len(self.root.keys) == 0 and not self.root.leaf and self.root.children:
            self.root = self.root.children[0] # Shrink tree height
        elif len(self.root.keys) == 0 and self.root.leaf: # Tree became empty
            pass # self.root is an empty leaf, which is fine

# --- Employee Database Example (More Compact) ---
@dataclass
class Employee:
    emp_id: int
    name: str
    # dept: str # Simplified for brevity
    # salary: int
    def __str__(self): # Shorter string representation
        return f"ID:{self.emp_id}, Name:{self.name}"

class EmployeeDB: # Shortened name
    def __init__(self, t_degree=2):
        print(f"Initializing Employee DB (B-Tree t={t_degree})")
        self.index = BTree(t=t_degree)
        self.count = 0

    def add_emp(self, emp_id, name): # Shortened method name
        if self.index.search(emp_id) is not None:
            print(f"Error: Emp ID {emp_id} ({name}) exists.")
            return
        emp = Employee(emp_id, name)
        self.index.insert(emp_id, emp)
        self.count += 1
        print(f"Added: {emp}")

    def find_emp(self, emp_id):
        emp = self.index.search(emp_id)
        status = f"Found: {emp}" if emp else f"Emp ID {emp_id} not found."
        print(status)
        return emp

    def del_emp(self, emp_id): # Shortened method name
        print(f"\nAttempting delete: Emp ID {emp_id}")
        if self.index.search(emp_id) is None:
            print(f"Error: Emp ID {emp_id} not found for deletion.")
            return
        
        self.index.delete(emp_id)
        if self.index.search(emp_id) is None:
            self.count -= 1
            print(f"Deleted Emp ID {emp_id}. Count: {self.count}")
        else:
            print(f"Warn: Emp ID {emp_id} still found post-delete.")

    def print_struct(self, title="B-Tree Structure"):
        print(f"\n--- {title} ---")
        if self.count == 0: print("DB is empty.")
        else: self.index.traverse()
        print(f"--- Total Emps: {self.count} ---")

def demo(): # Shortened name
    print("--- B-Tree Demo: Employee DB ---")
    # t=2 means 2-3-4 Tree (min keys 1, max keys 3 per node)
    db = EmployeeDB(t_degree=2) 

    # Using Indian names
    employees = [
        (10, "Priya"), (20, "Rohan"), (30, "Aisha"), (40, "Vikram"), (50, "Neha"),
        (60, "Arjun"), (70, "Sanya"), (5, "Zoya"), (15, "Ishaan"), (25, "Diya")
    ]
    for emp_id, name in employees:
        db.add_emp(emp_id, name)
    
    db.print_struct("Initial B-Tree")

    db.find_emp(30)  # Aisha
    db.find_emp(18)  # Not found

    keys_to_del = [60, 30, 5] # Arjun, Aisha, Zoya
    for emp_id in keys_to_del:
        db.del_emp(emp_id)
    db.print_struct(f"B-Tree after deleting {len(keys_to_del)} emps")
    
    # Delete remaining to empty the tree
    print("\n--- Deleting all remaining ---")
    # Simple way to get remaining keys for demo (in real scenario, might need tree iteration)
    remaining_ids = [emp[0] for emp in employees if emp[0] not in keys_to_del]
    for emp_id in sorted(list(set(remaining_ids))): # ensure unique and sorted
        if db.find_emp(emp_id) is not None: # check if still exists
             db.del_emp(emp_id)

    db.print_struct("B-Tree after deleting all")
    if db.count == 0: print("DB successfully emptied.")

    print("\n--- Re-adding some employees ---")
    db.add_emp(110, "Kiran")
    db.add_emp(120, "Anjali")
    db.print_struct("B-Tree after re-adding")

if __name__ == "__main__":
    demo()

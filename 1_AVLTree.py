#!pip install graphviz

import graphviz

class Node:
    __slots__ = ('key', 'left', 'right', 'height')
    
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self, *args):
        self.root = None
        if args:
            for key in args:
                self.insert(key)
    
    def insert(self, key):
        self.root = self._insert(self.root, key)
    
    def _insert(self, node, key):
        if not node:
            return Node(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return self._balance(node)
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
    
    def _delete(self, node, key):
        if not node:
            return node
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                min_node = self._min_value_node(node.right)
                node.key = min_node.key
                node.right = self._delete(node.right, min_node.key)
        
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        return self._balance(node)
    
    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current
    
    def _height(self, node):
        return node.height if node else 0
    
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _balance(self, node):
        balance = self._balance_factor(node)
        
        if balance > 1 and self._balance_factor(node.left) >= 0:
            return self._rotate_right(node)
        
        if balance > 1 and self._balance_factor(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        if balance < -1 and self._balance_factor(node.right) <= 0:
            return self._rotate_left(node)
        
        if balance < -1 and self._balance_factor(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, curr):
        chng = curr.right
        tmp = chng.left
        
        chng.left = curr
        curr.right = tmp
        
        curr.height = 1 + max(self._height(curr.left), self._height(curr.right))
        chng.height = 1 + max(self._height(chng.left), self._height(chng.right))
        
        return chng
    
    def _rotate_right(self, curr):
        chng = curr.left
        tmp = chng.right
        
        chng.right = curr
        curr.left = tmp
        
        curr.height = 1 + max(self._height(curr.left), self._height(curr.right))
        chng.height = 1 + max(self._height(chng.left), self._height(chng.right))
        
        return chng
    
    def contains(self, key):
        return self._contains(self.root, key)
    
    def _contains(self, node, key):
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._contains(node.left, key)
        else:
            return self._contains(node.right, key)
    
    def order(self):
        result = []
        self._order(self.root, result)
        return result
    
    def _order(self, node, result):
        if node:
            self._order(node.left, result)
            result.append(node.key)
            self._order(node.right, result)
            
    def __str__(self):
        return f"AVL-tree = {self.order()}"
    
    def __repr__(self):
        return f"AVLTree{self.order()}"
       
    def is_balanced(self):
        return self._is_balanced(self.root)
    
    def _is_balanced(self, node):
        if not node:
            return True
        
        balance = self._balance_factor(node)
        return (abs(balance) <= 1 and 
                self._is_balanced(node.left) and 
                self._is_balanced(node.right))
        
    def visualize(self, filename='avl_tree'):
        dot = graphviz.Digraph(comment='AVL Tree')
        dot.attr('node', shape='circle')
        
        def add_nodes_edges(node, parent_id=None, label=''):
            if node is not None:
                node_id = str(id(node))
                dot.node(node_id, f'{node.key}\n(h={node.height})')
                if parent_id is not None:
                    dot.edge(parent_id, node_id, label=label)
                add_nodes_edges(node.left, node_id, 'L')
                add_nodes_edges(node.right, node_id, 'R')
        
        add_nodes_edges(self.root)
        dot.render(filename, view=True, cleanup=True)

avl1 = AVLTree(10, 43, 24, 45, 2)
print(avl1)

numbers = [5, 36, 74, 23, 43, 36, 85, 10]
avl2 = AVLTree(*numbers)
avl2.visualize()

avl3 = AVLTree()
avl3.insert(5)
avl3.insert(3)
avl3.insert(789)
print(avl3)





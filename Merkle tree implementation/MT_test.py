from typing import List
import typing
import hashlib


class Node:
    def __init__(self, left, right, hash_value: str,content=None)-> None:
        self.left: Node = left
        self.right: Node = right
        self.hash_value = hash_value
        self.content = content # only leaf nodes have this (ie transaction data)
    
def hash_MT(val: str)-> str:
    return hashlib.sha256(val.encode("utf-8")).hexdigest()

"""
The following will check if the tree contructed by "generate_tree" is correct for the four
node case example.

transactions = ["abc", "def", "ghi"]
"""

def MT_check_three_node_example(MT_tree):
    
    leaf1 = Node(None, None, hash_MT("abc"),"abc")
    leaf2 = Node(None, None, hash_MT("def"),"def")
    leaf3 = Node(None, None, hash_MT("ghi"),"ghi")
    leaf4 = Node(None, None, hash_MT("<None>"),"<None>")

    layer1Node1 = Node(leaf1, leaf2, hash_MT(leaf1.hash_value+leaf2.hash_value))
    layer1Node2 = Node(leaf3, leaf4, hash_MT(leaf3.hash_value+leaf4.hash_value))

    rootNode = Node(layer1Node1, layer1Node2, hash_MT(layer1Node1.hash_value+layer1Node2.hash_value))

    iter = MT_tree;
    passed = False
    errors = 0
    if iter != None:
        if iter.hash_value != rootNode.hash_value:
            errors += 1
        else:
            if iter.left != None:
                layer1_left = iter.left
                
                if (layer1_left.hash_value != layer1Node1.hash_value):
                    errors += 1
                    
                else:
                    tree_leaf1 = layer1_left.left
                    if tree_leaf1 != None:
                        if (tree_leaf1.hash_value != leaf1.hash_value):
                            errors += 1
                    else:
                        errors +=1
                        
                    tree_leaf2 = layer1_left.right
                    if tree_leaf2 != None:
                        if (tree_leaf2.hash_value != leaf2.hash_value):
                            errors += 1
                    else:
                        errors +=1
            else:
                errors += 1
                
            if iter.right != None:
                layer1_right = iter.right
                
                if (layer1_right.hash_value != layer1Node2.hash_value):
                    errors += 1
                    
                else:
                    tree_leaf1 = layer1_right.left
                    if tree_leaf1 != None:
                        if (tree_leaf1.hash_value != leaf3.hash_value):
                            errors += 1
                    else:
                        errors +=1
                        
                    tree_leaf2 = layer1_right.right
                    if tree_leaf2 != None:
                        if (tree_leaf2.hash_value != leaf4.hash_value):
                            errors += 1
                    else:
                        errors +=1
            else:
                errors += 1
        
    else:
        errors +=1
        
    if errors == 0:
        passed = True
    
    if (passed):
        print("Passed 3 node test case!")
    else:
        print("Failed 3 node test case!")
        print("There are at least " + str(errors) + " error(s) found")
        
        
"""
The following will check if the tree contructed by "generate_tree" is correct for the four
node case example.

transactions = ["abc", "def", "ghi", "jkl"]
"""

def MT_check_four_node_example(MT_tree):
    
    leaf1 = Node(None, None, hash_MT("abc"),"abc")
    leaf2 = Node(None, None, hash_MT("def"),"def")
    leaf3 = Node(None, None, hash_MT("ghi"),"ghi")
    leaf4 = Node(None, None, hash_MT("jkl"),"jkl")

    layer1Node1 = Node(leaf1, leaf2, hash_MT(leaf1.hash_value+leaf2.hash_value))
    layer1Node2 = Node(leaf3, leaf4, hash_MT(leaf3.hash_value+leaf4.hash_value))

    rootNode = Node(layer1Node1, layer1Node2, hash_MT(layer1Node1.hash_value+layer1Node2.hash_value))

    iter = MT_tree;
    passed = False
    errors = 0
    if iter != None:
        if iter.hash_value != rootNode.hash_value:
            errors += 1
        else:
            if iter.left != None:
                layer1_left = iter.left
                
                if (layer1_left.hash_value != layer1Node1.hash_value):
                    errors += 1
                    
                else:
                    tree_leaf1 = layer1_left.left
                    if tree_leaf1 != None:
                        if (tree_leaf1.hash_value != leaf1.hash_value):
                            errors += 1
                    else:
                        errors +=1
                        
                    tree_leaf2 = layer1_left.right
                    if tree_leaf2 != None:
                        if (tree_leaf2.hash_value != leaf2.hash_value):
                            errors += 1
                    else:
                        errors +=1
            else:
                errors += 1
                
            if iter.right != None:
                layer1_right = iter.right
                
                if (layer1_right.hash_value != layer1Node2.hash_value):
                    errors += 1
                    
                else:
                    tree_leaf1 = layer1_right.left
                    if tree_leaf1 != None:
                        if (tree_leaf1.hash_value != leaf3.hash_value):
                            errors += 1
                    else:
                        errors +=1
                        
                    tree_leaf2 = layer1_right.right
                    if tree_leaf2 != None:
                        if (tree_leaf2.hash_value != leaf4.hash_value):
                            errors += 1
                    else:
                        errors +=1
            else:
                errors += 1
        
    else:
        errors +=1
        
    if errors == 0:
        passed = True
    
    if (passed):
        print("Passed 4 node test case!")
    else:
        print("Failed 4 node test case!")
        print("There are at least " + str(errors) + " error(s) found")

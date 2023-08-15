import hashlib
from enum import Enum

def hash_bMPT(val: str)-> str:
    return hashlib.sha3_256(val.encode("utf-8")).hexdigest()

class MPT_Type(Enum):
    root = 0
    extension = 1
    branch = 2
    leaf = 3


# The hash_value of the root is same hash of its child (unless its an empty tree)
class MPT_Root(object):
    def __init__(self, next_node=None, hash_value=None):
        self.mpt_type = MPT_Type.root
        self.next_node = next_node
        self.hash_value = hash_value

class MPT_Ext_Node(object):
    def __init__(self, shared_nibble, next_node=None, hash_value=None):
        self.mpt_type = MPT_Type.extension
        self.shared_nibble = shared_nibble
        self.next_node = next_node
        self.hash_value = hash_value

class MPT_Branch_Node(object):
    def __init__(self, index0=None, index1=None, hash_value=None):
        self.mpt_type = MPT_Type.branch
        self.index0 = index0
        self.index1 = index1
        self.hash_value = hash_value


class MPT_Leaf_Node(object):
    def __init__(self, key_end, value, hash_value=None):
        self.mpt_type = MPT_Type.leaf
        self.key_end = key_end
        self.value = value
        self.hash_value = hash_value
        
def get_nodes(input_tree, nodes=[]):
    if (input_tree == None):
        return nodes
    else:
        if input_tree.mpt_type.value == MPT_Type.root.value:
            return [input_tree.hash_value]+get_nodes(input_tree.next_node)
        
        if input_tree.mpt_type.value == MPT_Type.extension.value:
            return [input_tree.hash_value]+get_nodes(input_tree.next_node,nodes)
        
        if input_tree.mpt_type.value == MPT_Type.branch.value:
            return ([input_tree.hash_value]+get_nodes(input_tree.index0)+get_nodes(input_tree.index1))
            
        if input_tree.mpt_type.value == MPT_Type.leaf.value:
            return [input_tree.hash_value]


def get_node_type(input_tree, nodes=[]):
    if (input_tree == None):
        return nodes
    else:
        if input_tree.mpt_type.value == MPT_Type.root.value:
            return ["root"]+get_node_type(input_tree.next_node)
        
        if input_tree.mpt_type.value == MPT_Type.extension.value:
            return ["ext"]+get_node_type(input_tree.next_node,nodes)
        
        if input_tree.mpt_type.value == MPT_Type.branch.value:
            return (["branch"]+get_node_type(input_tree.index0)+get_node_type(input_tree.index1))
            
        if input_tree.mpt_type.value == MPT_Type.leaf.value:
            return ["leaf"]


"""
The key-value pairs in this trie are:
    [["1101111011", "abc"], ["0101000011", "def"], ["0101010101", "ghi"]]
"""
def bMPt_three_node_test(input_tree):
    leaf1 = MPT_Leaf_Node("1101111011", "abc", hash_bMPT("abc"))
    leaf2 = MPT_Leaf_Node("00011", "def", hash_bMPT("def"))
    leaf3 = MPT_Leaf_Node("10101", "ghi", hash_bMPT("ghi"))
    
    branch2 = MPT_Branch_Node(leaf2, leaf3, hash_bMPT(leaf2.hash_value+leaf3.hash_value))
    ext2 = MPT_Ext_Node("01010", branch2, hash_bMPT(branch2.hash_value))
    branch3 = MPT_Branch_Node(ext2, leaf1, hash_bMPT(ext2.hash_value+leaf1.hash_value))
    
    root1 = MPT_Root(branch3, branch3.hash_value)
    
    treeNodes = get_nodes(input_tree)
    treeNodeType = get_node_type(input_tree)

    if (len(treeNodes) != 7):
        print("Incorrect number of Nodes found!")
        print("Failed 3 node test case!")
    else: 
        errors = 0
        correctNodes = [root1.hash_value, root1.hash_value, ext2.hash_value,
                        branch2.hash_value, leaf2.hash_value, leaf3.hash_value, 
                        leaf1.hash_value]
        correctNodeTypes = ['root', 'branch', 'ext', 'branch', 'leaf', 'leaf', 'leaf']
        for i in range(7):
            if correctNodes[i] != treeNodes[i]:
                print("wrong at"+str(i))
                print(correctNodes[i] )
                print(treeNodes[i] )
                errors +=1
            if correctNodeTypes[i] != treeNodeType[i]:
                errors +=1
                print("wrong att"+str(i))
                
        passed= False
        if errors == 0:
            passed = True
        
        if (passed):
            print("Passed 3 node test case!")
        else:
            print("Failed 3 node test case!")
            print("There are at least " + str(errors) + " error(s) found")
            
"""
The key-value pairs in this trie are:
    [["1101111011", "abc"], ["0101000011", "def"], ["0101010101", "ghi"], ["0101010111", "jkl"]]
"""
def bMPt_four_node_test(input_tree):
    leaf1 = MPT_Leaf_Node("1101111011", "abc", hash_bMPT("abc"))
    leaf2 = MPT_Leaf_Node("00011", "def", hash_bMPT("def"))
    leaf3 = MPT_Leaf_Node("01", "ghi", hash_bMPT("ghi"))
    leaf4 = MPT_Leaf_Node("11", "jkl", hash_bMPT("jkl"))
    
    branch1 = MPT_Branch_Node(leaf3, leaf4, hash_bMPT(leaf3.hash_value+leaf4.hash_value))
    ext1 = MPT_Ext_Node("101", branch1, hash_bMPT(branch1.hash_value))
    branch2 = MPT_Branch_Node(leaf2, ext1, hash_bMPT(leaf2.hash_value+ext1.hash_value))
    ext2 = MPT_Ext_Node("01010", branch2, hash_bMPT(branch2.hash_value))
    branch3 = MPT_Branch_Node(ext2, leaf1, hash_bMPT(ext2.hash_value+leaf1.hash_value))
    
    root1 = MPT_Root(branch3, branch3.hash_value)


    treeNodes = get_nodes(input_tree)
    treeNodeType = get_node_type(input_tree)
    if (len(treeNodes) != 10):
        print("Incorrect number of Nodes found!")
        print("Failed 4 node test case!")
    else:
        errors = 0
        correctNodes = [root1.hash_value, root1.hash_value, ext2.hash_value,
                        branch2.hash_value, leaf2.hash_value, ext1.hash_value,
                        branch1.hash_value, leaf3.hash_value, leaf4.hash_value,
                        leaf1.hash_value]
        correctNodeTypes = ['root', 'branch', 'ext', 'branch', 'leaf', 'ext', 
                            'branch', 'leaf', 'leaf', 'leaf']
        for i in range(10):
            if correctNodes[i] != treeNodes[i]:
                print("wrong at"+str(i))
                print(correctNodes[i] )
                print(treeNodes[i] )
                errors +=1
            if correctNodeTypes[i] != treeNodeType[i]:
                errors +=1
                print("wrong att"+str(i))
                
        passed= False
        if errors == 0:
            passed = True
        
        if (passed):
            print("Passed 4 node test case!")
        else:
            print("Failed 4 node test case!")
            print("There are at least " + str(errors) + " error(s) found")
    
from asyncio.windows_events import NULL
import hashlib
from enum import Enum
from multiprocessing.dummy import Array
from unittest import result

from bMPT_test import *

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


"""
4.1 Insert an element into a Merkle Patricia Trie
As a warm up exercise, you will be adding an element to an existing binary Merkle
Patricia trie (bMP trie). Remember that extension nodes should be used as much as possible to 
make the trie as compact as possible.

You may assume that all keys have a length of 10 binary digits.

The existing bMP trie has the form of:
            Root Node
               |
            Branch Node
          /        \
      Ext Node    Leaf Node    
      01010       key_end: 
        |         1101111011
    Branch Node    value: "abc"
   /          \
Leaf Node     Leaf Node
key_end:      key_end:
 00011         10101
value:"def"   value:"ghi"

Remember to update the hashes of parent nodes!

Add the key-value pair ["1101000000", "jkl"]
"""
def add_to_merkle_patricia():
    leaf1 = MPT_Leaf_Node("00011", "def", hash_bMPT("def"))
    leaf2 = MPT_Leaf_Node("10101", "ghi", hash_bMPT("ghi"))
    leaf3 = MPT_Leaf_Node("1101111011", "abc", hash_bMPT("abc"))
    
    branch1 = MPT_Branch_Node(leaf1, leaf2, hash_bMPT(leaf1.hash_value+leaf2.hash_value))
    ext1 = MPT_Ext_Node("01010", branch1,  hash_bMPT(branch1.hash_value))
    
    branch2 = MPT_Branch_Node(ext1, leaf3, hash_bMPT(ext1.hash_value+leaf3.hash_value))
    
    # The root node's hash value is either the same as its child if there are 
    # children or hash_bMPT("<None>") if the tree is empty
    rootNode = MPT_Root(branch2, branch2.hash_value)
    
#######  YOUR CODE GOES HERE                              ######
    leaf4 = MPT_Leaf_Node("000000","jkl",hash_bMPT("jkl"))
    branch3 = MPT_Branch_Node(rootNode.next_node.index1,leaf4, hash_bMPT(rootNode.next_node.index1.hash_value+leaf4.hash_value))
    ext2 = MPT_Ext_Node("1101",branch3, hash_bMPT(branch3.hash_value))
    #leafnode3
    rootNode.next_node = MPT_Branch_Node(ext1,ext2,hash_bMPT(ext1.hash_value+ext2.hash_value))
    rootNode = MPT_Root(rootNode.next_node,rootNode.next_node.hash_value)
    rootNode.next_node.index1.next_node.index0.key_end = 111011
    
   
    
    return rootNode
add_to_merkle_patricia()

"""
4.2 Edit an element into a Merkle Patricia Trie
As a second warm up exercise, you will be editing an element to an existing binary Merkle
Patricia trie (bMP trie). Remember that extension nodes should be used as much as possible to 
make the trie as compact as possible.

You may assume that all keys has the length of 10 binary digits.

The existing bMP trie has the form of:
            Root Node
               |
            Branch Node
          /        \
      Ext Node    Leaf Node    
      01010       key_end: 
        |         1101111011
    Branch Node    value: "abc"
   /          \
Leaf Node     Leaf Node
key_end:      key_end:
 00011         10101
value:"def"   value:"ghi"

Remember to update the hashes of parent nodes!

Edit the key-value pair ("0101000011", "def") to ("0101000011", "cat")
"""
def edit_merkle_patricia():
    leaf1 = MPT_Leaf_Node("00011", "def", hash_bMPT("def"))
    leaf2 = MPT_Leaf_Node("10101", "ghi", hash_bMPT("ghi"))
    leaf3 = MPT_Leaf_Node("1101111011", "abc", hash_bMPT("abc"))
    
    branch1 = MPT_Branch_Node(leaf1, leaf2, hash_bMPT(leaf1.hash_value+leaf2.hash_value))
    ext1 = MPT_Ext_Node("01010", branch1,  hash_bMPT(branch1.hash_value))
    
    branch2 = MPT_Branch_Node(ext1, leaf3, hash_bMPT(ext1.hash_value+leaf3.hash_value))
    
    # The root node's hash value is either the same as its child if there are 
    # children or hash_bMPT("<None>") if the tree is empty
    rootNode = MPT_Root(branch2, branch2.hash_value)
    
#######  YOUR CODE GOES HERE                              ######
    rootNode.next_node.index0.next_node.index0.value = "cat"
    return rootNode


"""
4.3 Remove an element into a Merkle Patricia Trie
As a final warm up exercise, you will be removing an element to an existing binary Merkle
Patricia trie (bMP trie). Remember that extension nodes should be used as much as possible to 
make the trie as compact as possible.

You may assume that all keys has the length of 10 binary digits.

The existing bMP trie has the form of:
            Root Node
               |
            Branch Node
          /        \
      Ext Node    Leaf Node    
      01010       key_end: 
        |         1101111011
    Branch Node    value: "abc"
   /          \
Leaf Node     Leaf Node
key_end:      key_end:
 00011         10101
value:"def"   value:"ghi"

Remember to update the hashes of parent nodes!

Remove the key-value pair ("0101010101", "ghi")
"""
def remove_merkle_patricia():
    leaf1 = MPT_Leaf_Node("00011", "def", hash_bMPT("def"))
    leaf2 = MPT_Leaf_Node("10101", "ghi", hash_bMPT("ghi"))
    leaf3 = MPT_Leaf_Node("1101111011", "abc", hash_bMPT("abc"))
    
    branch1 = MPT_Branch_Node(leaf1, leaf2, hash_bMPT(leaf1.hash_value+leaf2.hash_value))
    ext1 = MPT_Ext_Node("01010", branch1,  hash_bMPT(branch1.hash_value))
    
    branch2 = MPT_Branch_Node(ext1, leaf3, hash_bMPT(ext1.hash_value+leaf3.hash_value))
    
    # The root node's hash value is either the same as its child if there are 
    # children or hash_bMPT("<None>") if the tree is empty
    rootNode = MPT_Root(branch2, branch2.hash_value)
    
#######  YOUR CODE GOES HERE                              ######
    # ghi = rootNode.next_node.index0.next_node.index1 
    return rootNode

#################################################################################


"""
4.4 Generating a Merkle Patricia Trie
In this problem, you will be implementing a function to construct a binary Merkle Patricia 
Tree (bMPT). The input will be a list of key-value pairs. 

Remember that extension nodes should be used as much as possible to make the 
trie as compact as possible.

You may assume that all keys has the length of 10 binary digits.

--------------------------------------------------------

The recommended implementation is to add elements into the bMPT. Adding the first node
is straight forward. Adding additional nodes will require traversing down the trie based
on the key.

The following are examples of adding nodes into a trie.

    Starting out, its just a root node
                Root Node
                    |
                  Null

    We then add the first leaf node.
                Root Node
                    |
                Leaf Node
          key_end: 1101111011
                value: "abc"
                  
    Now we add a second node. We will be creating a branch node where the keys 
    first differ.
If there is a common prefix, create an extension node first.

    We then add the first leaf node.
                Root Node
                    |
              Branch Node
             /           \
    Leaf Node            Leaf Node
    key_end: 0101000011  key_end: 1101111011
    value: "def"         value: "abc"

    Adding a third node is very similar to the second. This time we will need an 
    extension node.
                Root Node
                    |
              Branch Node
              /        \
         Ext Node    Leaf Node    
          01010       key_end: 
           |         1101111011
      Branch Node    value: "abc"
     /          \
Leaf Node     Leaf Node
key_end:      key_end:
 00011         10101
value:"def"   value:"ghi"

    We continue to add a fourth node.
    
             Root Node
                    |
              Branch Node
              /        \
         Ext Node    Leaf Node    
          01010       key_end: 
           |         1101111011
      Branch Node    value: "abc"
     /          \
Leaf Node     Ext Node
key_end:        101
 00011           |
value:"def"      |
            Branch Node
             /      \
            /        \
        Leaf Node     Leaf Node 
        key_end:       key_end:
           01            11
      value:"ghi"      value:"jkl"
             

The input will be a list of key-value pairs where each key is string
composed of 10 binary digits.
For example, [["1101111011", "abc"], ["0101000011", "def"]]

The output should be the root of the constructed tree.
"""
def generate_merkle_patricia(key_value_list):
#######  YOUR CODE GOES HERE                              ######
#######     Change the return value                       ######
  result = []
  temp = ""
  for i in key_value_list:
        leaf = MPT_Leaf_Node(i[0], i[1], hash_bMPT(i[1]))
        result.append(leaf)
        
  
  root = MPT_Root(result[0],result[0].hash_value)
  result.pop(0)
  
  for k in result:
      
        temp = k.key_end  
        if root.next_node.mpt_type == MPT_Type.branch:
            if k.key_end[0] == "0":
                brancharr = []
                brancharr.append(root.next_node.index1)
                countBranch = 1
                tempBranch = root.next_node.index0
                
                 
                if tempBranch.mpt_type == MPT_Type.extension:    
                    while(tempBranch.next_node.mpt_type == MPT_Type.branch):
                      countBranch = countBranch+1
                      if tempBranch.shared_nibble == k.key_end[0:len(tempBranch.shared_nibble)]:
                       shared_num = []
                       shared_num.append(tempBranch.shared_nibble)
                       k.key_end = k.key_end[len(tempBranch.shared_nibble):]
                       tempBranch = tempBranch.next_node
                       if k.key_end[0] == "1":
                           brancharr.append(tempBranch.index0)
                           tempBranch = tempBranch.index1
                           if tempBranch.mpt_type == MPT_Type.leaf:
                               index0count = 0 
                               for m in range(len(k.key_end)):
                                 if k.key_end[m] == tempBranch.key_end[m]:
                                  index0count = index0count+1
                                 else:
                                  break  
                               shared_nib = k.key_end[0:index0count]
                               tempBranch.key_end = tempBranch.key_end[index0count:]
                               k.key_end = k.key_end[index0count:]
              
                               
                                             
                               branch2 = MPT_Branch_Node(tempBranch,k, hash_bMPT(tempBranch.hash_value + k.hash_value))
                               ext1 = MPT_Ext_Node(shared_nib,branch2, hash_bMPT(branch2.hash_value))
                               
                               branch4 = MPT_Branch_Node(None,None,None)
                               extnode = MPT_Ext_Node(None,None,None)
                               
                              
                               
                               for i in range(countBranch):
                                   
                                   branch3 = brancharr.pop()
                                   
                                   if branch3.key_end[0] == "0":
                                       branch4 = MPT_Branch_Node(branch3,ext1,hash_bMPT(branch3.hash_value + ext1.hash_value))
                                       ext1 = MPT_Ext_Node(shared_num.pop(), branch4, hash_bMPT(branch4.hash_value))
                                      
                                   else:
                                       branch4 = MPT_Branch_Node(ext1,branch3, hash_bMPT(ext1.hash_value + branch3.hash_value))
                                          
                                   
                               
                               
                               
                               
                               root = MPT_Root(branch4, branch4.hash_value)
                           
                               return root
                           
                               break
                            
                    
                if tempBranch.mpt_type == MPT_Type.leaf:
                       index0count = 0 
                       for m in range(len(k.key_end)):
                        if k.key_end[m] == tempBranch.key_end[m]:
                           index0count = index0count+1
                        else:
                         break  
                       shared_nib = k.key_end[0:index0count]
                       tempBranch.key_end = tempBranch.key_end[index0count:]
                       k.key_end = k.key_end[index0count:]
              
                       branch2 = MPT_Branch_Node(tempBranch,k, hash_bMPT(tempBranch.hash_value + k.hash_value))
                       ext1 = MPT_Ext_Node(shared_nib,branch2, hash_bMPT(branch2.hash_value))
                       root.next_node =MPT_Branch_Node(ext1,root.next_node.index1, hash_bMPT(ext1.hash_value+root.next_node.index1.hash_value))
                       root = MPT_Root(root.next_node, root.next_node.hash_value)
                      
            else:
                brancharr = []
                brancharr.append(root.next_node.index0)
            
                countBranch = 1
                tempBranch = root.next_node.index1
                
                
                if tempBranch.mpt_type == MPT_Type.extension:    
                    while(tempBranch.next_node.mpt_type == MPT_Type.branch):
                      countBranch = countBranch+1
                      
                      if tempBranch.shared_nibble == k.key_end[0:len(tempBranch.shared_nibble)]:
                       shared_num = []
                        
                       shared_num.append(tempBranch.shared_nibble)
                       k.key_end = k.key_end[len(tempBranch.shared_nibble):]
                       tempBranch = tempBranch.next_node
                       if k.key_end[0] == "1":
                           brancharr.append(tempBranch.index0)
                           tempBranch = tempBranch.index1
                           if tempBranch.mpt_type == MPT_Type.leaf:
                              
                               index0count = 0 
                               for m in range(len(k.key_end)):
                                 if k.key_end[m] == tempBranch.key_end[m]:
                                  index0count = index0count+1
                                 
                                 else:
                                  break  
                               shared_nib = k.key_end[0:index0count]
                               tempBranch.key_end = tempBranch.key_end[index0count:]
                               k.key_end = k.key_end[index0count:]
              
                               
                                             
                               branch2 = MPT_Branch_Node(tempBranch,k, hash_bMPT(tempBranch.hash_value + k.hash_value))
                               ext1 = MPT_Ext_Node(shared_nib,branch2, hash_bMPT(branch2.hash_value))
                               
                               branch4 = MPT_Branch_Node(None,None,None)
                               extnode = MPT_Ext_Node(None,None,None)
                              
                               for i in range(countBranch):
                                   
                                   branch3 = brancharr.pop()
                                   
                                   if i == 0:
                                       branch4 = MPT_Branch_Node(branch3,ext1,hash_bMPT(branch3.hash_value + ext1.hash_value))
                                       ext1 = MPT_Ext_Node(shared_num.pop(), branch4, hash_bMPT(branch4.hash_value))
                                     
                                     
                                       
                                      
                                   else:
                                        branch4 = MPT_Branch_Node(branch3,ext1, hash_bMPT(ext1.hash_value + branch3.hash_value))
                                        break
                                   
                               
                               
                               
                               
                               root = MPT_Root(branch4, branch4.hash_value)
                           
                              
                               return root
                           
                               break
                            
                    
                if tempBranch.mpt_type == MPT_Type.leaf:
                       index0count = 0 
                      
                       for m in range(len(k.key_end)):
                        if temp[m] == tempBranch.key_end[m]:
                           
                        
                           index0count = index0count+1
                        else:
                         break  
                       shared_nib = k.key_end[0:index0count]
                       tempBranch.key_end = tempBranch.key_end[index0count:]
                       k.key_end = k.key_end[index0count:]
                    
                       branch2 = MPT_Branch_Node(tempBranch,k, hash_bMPT(tempBranch.hash_value + k.hash_value))
                       ext1 = MPT_Ext_Node(shared_nib,branch2, hash_bMPT(branch2.hash_value))
                       root.next_node =MPT_Branch_Node(root.next_node.index0,ext1,hash_bMPT(root.next_node.index1.hash_value+ ext1.hash_value))
                       root = MPT_Root(root.next_node, root.next_node.hash_value)             
              
        if root.next_node.mpt_type == MPT_Type.leaf:
          
          count = 0
          for j in range(len(k.key_end)):
              if k.key_end[j] == root.next_node.key_end[j]:
                 
                  count = count + 1
                  
              else:
                    if temp[0] == "0":
                        
                        branch1 = MPT_Branch_Node(k,root.next_node, hash_bMPT(k.hash_value + root.next_node.hash_value))
                        root = MPT_Root(branch1, branch1.hash_value)
                        
                    else:
                        
                        branchs = MPT_Branch_Node(root.next_node,k,hash_bMPT(root.next_node.hash_value+ k.hash_value))
                        root = MPT_Root(branchs, branchs.hash_value)
                      
                      
              break     
      
                         
       
  return root
"""
Here is a small 3 value-pair test for generate_merkle_patricia
"""
test_key_value = [["1101111011", "abc"], ["0101000011", "def"], ["0101010101", "ghi"]]
tree = generate_merkle_patricia(test_key_value)


bMPt_three_node_test(tree)


"""
Here is a small 4 value-pair test for generate_merkle_patricia
"""
test_key_value = [["1101111011", "abc"], ["0101000011", "def"], ["0101010101", "ghi"], ["0101010111", "jkl"]]
tree = generate_merkle_patricia(test_key_value)

bMPt_four_node_test(tree)



"""
4.5 Generating a Proof for Merkle Patricia Tries
In this section, you will be implementing a function to produce the proof of a transaction. 
The function will take two inputs, a key-value pair and the trie that contains it. 
The output of this function should be a list of hashes that a verify will use to check 
that a transaction was recorded in a tree.


             RootNode
                    |
              BranchNode1
              /        \
         ExtNode1     LeafNode1  
          01010       key_end: 
           |         1101111011
      BranchNode2    value: "abc"
     /          \
LeafNode2      ExtNode2
key_end:        101
 00011           |
value:"def"      |
            BranchNode3
             /      \
            /        \
        LeafNode3     LeafNode4
        key_end:       key_end:
           01            11
      value:"ghi"      value:"jkl"
             



Given the 4 leaf example from above, the proof for ["1101111011", "abc"] (LeafNode1) is:

proof_value=[ExtNode1.hash_value]
proof_branch=[0]

For ["0101000011", "abc"] (LeafNode2):
    proof_value=[ExtNode2.hash_value, "EXT", LeafNode1.hash_value]
    proof_branch=[1, 0, 1]
 
For ["0101010101", "abc"] (LeafNode3):
    proof_value=[LeafNode4.hash_value, "EXT", LeafNode2.hash_value, "EXT", 
                 LeafNode1.hash_value]
    proof_branch=[1, 0, 0, 0,1]
    
For ["0101010111", "abc"] (LeafNode4):
    proof_value=[LeafNode3.hash_value, "EXT", LeafNode2.hash_value, "EXT", 
                 LeafNode1.hash_value]
    proof_branch=[0, 0, 0, 0,1]

This is very similar to the Merkle Tree proof. However, the Extension Node will always
only have one child, so it is important to denote that as the above example shows. The
value for the "EXT" value in the proof_branch can be 0 or 1. The second array 
denotes if the hash value should be used as the first or second part of the concatenation. 
"0" means the start, "1" means the end (equivalently, the left or right child).

This is because the root node (and its hash) is pubic knowledge. The proof allows a verifier
to compute if the transaction is in the tree:
 
To verify the proof for LeafNode3, the verifier will compute:
    
H1 = Hash(Hash("ghi")||proof_value[0])
H2 = Hash(H1)
H3 = Hash(proof_value[2]||H2)
H4 = Hash(H3)
H5 = Hash(H4||proof_value[4])

Check if H5 == tree.hash_value


--------------------------------------------------------
The input "trie" should be the root node of the trie.
The input "key_value_pair" should just a the key and value, such as ["1101111011", "abc"]

The output should be two lists, the proof_value and the proof_branch. Remember that 
in the proof_branch, "0" means that the given value in the proof branch should be at 
the start of the concatation and "1" means that the value in the proof branch should 
be at the end of the concatation.

"EXT" denotes an extension node exists, as there is not a second child to concatenate.
See the above examples on proper usage.
"""
def generate_merkle_patricia_proof(trie, key_value_pair):
#######  YOUR CODE GOES HERE                                                            K                       ######
#######     Change the return value                       ######
    returnVal = []
   
    returnBranch = []
    final =[]
    if trie.next_node.mpt_type == MPT_Type.branch:
        
        tempBranch = trie.next_node
        tempKey_value = key_value_pair[0]
        if tempKey_value[0] == "1":
            returnVal.append(tempBranch.index0.hash_value)
            returnBranch.append(0)
            tempBranch = tempBranch.index1
            if tempBranch.mpt_type == MPT_Type.leaf:
                if(tempBranch.key_end == tempKey_value):
                    final = []
                    final.append(returnVal)
                    final.append(returnBranch)
                   
                    return final
                if tempBranch.mpt_type == MPT_Type.extension:
                 returnVal.insert(0,"EXT")
                 shared_Number = 0
                 tempString = ""
                 while(tempBranch != MPT_Type.leaf):
                    tempstring = tempString + tempBranch.shared_nibble
                    shared_Number = shared_Number+ len(tempBranch.shared_nibble)
                    tempBranch = tempBranch.next_node
                   
                    check_so_far = tempKey_value[shared_Number:]
                 
                    if check_so_far[0] =="0":
                        returnVal.insert(0,tempBranch.index1.hash_value)
                        tempBranch = tempBranch.index0
                        
                        
                    else:
                        returnVal.insert(0,tempBranch.index0.hash_value)
                        
                        tempBranch = tempBranch.index1    
                    
                    if tempBranch.mpt_type == MPT_Type.leaf:
                      
                        return returnVal
                    else:
                        returnVal.insert(0,"EXT") 
        else:
            returnVal.append(tempBranch.index1.hash_value)
            returnBranch.insert(0,1)
            tempBranch = tempBranch.index0
            if tempBranch.mpt_type == MPT_Type.leaf:
                if(tempBranch.key_end == tempKey_value):
                    final = []
                    final.append(returnVal)
                    final.append(returnBranch)
                    
                    return final
            if tempBranch.mpt_type == MPT_Type.extension:
                returnVal.insert(0,"EXT")
                returnBranch.insert(0,0)
                shared_Number = 0
                tempString = ""
                while(tempBranch != MPT_Type.leaf):
                    tempstring = tempString + tempBranch.shared_nibble
                    shared_Number = shared_Number+ len(tempBranch.shared_nibble)
                    tempBranch = tempBranch.next_node
                   
                    check_so_far = tempKey_value[shared_Number:]
                 
                    if check_so_far[0] =="0":
                        returnVal.insert(0,tempBranch.index1.hash_value)
                        
                   
                        tempBranch = tempBranch.index0
                        returnBranch.insert(0,1)
                        
                        
                    else:
                        returnVal.insert(0,tempBranch.index0.hash_value)
                        returnBranch.insert(0,0)
                        
                        tempBranch = tempBranch.index1    
                    
                    if tempBranch.mpt_type == MPT_Type.leaf:
                        
                        final.append(returnVal)
                        final.append(returnBranch)
                      
                        return final
                    else:
                        returnVal.insert(0,"EXT")
                        returnBranch.insert(0,0)
                    
                        

    
    return None 


k = generate_merkle_patricia_proof(tree,["0101010101","ghi"])


"""
4.6 Verify a Proof for Merkle Patricia Tries
Given a Merkle tree and a proof of membership, implement a function to verify it. The input
will be a tree, a transaction, and the proof, and the function should return True or False.

Refer to the previous problem's comments for more details.
--------------------------------------------------------
The input "trie" should be the root node of the trie.
The input "proof_value" should be the hashes used in the proof.
The input "proof_branch" should denote which child the proof_value is on.
The input "key_value_pair" should just be the string of the the key and value.

The output should be true or false
"""
def verify_merkle_patricia_proof(trie, proof_value, proof_branch, key_value_pair):
#######  YOUR CODE GOES HERE                              ######
#######     Change the return value                       ######

    merkle_root = trie.hash_value
    
    target_hash = hash_bMPT(key_value_pair[1])
    target = key_value_pair[1]
    
    if proof_branch[0] == 0: 
     hash_value = hash_bMPT(proof_value[0]+target_hash)
   
    else:
       hash_value = hash_bMPT(target_hash+proof_value[0])
       
    proof_branch.pop(0)
    final_value = ""
    temp = hash_value
    proof_value.pop(0)
  
    if len(proof_value) == 0:
        
   
     return hash_value == merkle_root
    else:
       count = 0
       proof_hash = target_hash
       for p in proof_value:
           if p == "EXT":
           
             temp = hash_bMPT(temp)
             count = count+1
            
               
           else: 
             if proof_branch[count] == 0:  
               final_value = hash_bMPT(p + temp)
              
             
               temp = final_value
               count = count+1
             else:
               
               final_value = hash_bMPT(temp + p)
             
               temp = final_value
               count = count+1
    
    return merkle_root == final_value
verify_merkle_patricia_proof(tree,k[0],k[1],["0101010101","ghi"])
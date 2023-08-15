from typing import List
import typing
import hashlib

from MT_test import *

class Node:
    def __init__(self, left, right, hash_value: str,content=None)-> None:
        self.left: Node = left
        self.right: Node = right
        self.hash_value = hash_value
        self.content = content # only leaf nodes have this (ie transaction data)
    
def hash_MT(val: str)-> str:
    return hashlib.sha256(val.encode("utf-8")).hexdigest()

"""
Problem 3.1: generate_tree
In this problem, you will be implementing a function to construct a Merkle Tree. The input
will be the transaction data in the form of an array of strings. Recall that all of the data
in a Merkle tree, such as the transactions, are stored in the leaves while the other nodes
are comprised of only hashes. 

--------------------------------------------------------

The input will a list of strings such as the following:
    
transactions = ["abc", "def", "ghi", "jkl"]

The tree constructed would look like the following:
    
                    H1234=Hash[H12||H34] 
               /                        \
     H12=Hash[H1||H2]               H34=Hash[H3||H4]
    /           \                     /           \
H1=Hash["abc"]  H2=Hash["def"]   H3=Hash["ghi"]   H4=Hash["jkl"]


Where || denotes concatenation.

Given the above transactions list, generate_tree should generate a tree as the following:

leaf1 = Node(None, None, hash_MT("abc"),"abc")
leaf2 = Node(None, None, hash_MT("def"),"def")
leaf3 = Node(None, None, hash_MT("ghi"),"ghi")
leaf4 = Node(None, None, hash_MT("jkl"),"jkl")

layer1Node1 = Node(leaf1, leaf2, hash_MT(leaf1.hash_value+leaf2.hash_value))
layer1Node2 = Node(leaf3, leaf4, hash_MT(leaf3.hash_value+leaf4.hash_value))

rootNode = Node(layer1Node1, layer1Node2, hash_MT(layer1Node1.hash_value+layer1Node2.hash_value))

--------------------------------------------------------

If the number of transactions is not an even power of two, we will do the following:

transactions = ["abc"]
 H[H["abc"]||H["<None>"]]
     /           \
 H["abc"]       H["None"]
 
leaf1 = Node(None, None, hash_MT("abc"),"abc")
leaf2 = Node(None, None, hash_MT("<None>"), "<None>")
rootNode = Node(leaf1, leaf2, hash_MT(leaf1.hash_value+leaf2.hash_value))

--------------------------------------------------------
The input "transactionList" should be a list of transcations.
An example is  ["abc", "def", "ghi", "jkl"]

The output should be the root node of the constructed tree.

"""
def generate_tree(transactionList):
    leafNodes=[]
    root = ""
    for transaction in transactionList:
        leafNodes.append(Node(None, None, hash_MT(transaction),transaction))
    
#leaf1 = Node(None, None, hash_MT("abc"),"abc")
#leaf2 = Node(None, None, hash_MT("def"),"def")
#leaf3 = Node(None, None, hash_MT("ghi"),"ghi")
#leaf4 = Node(None, None, hash_MT("jkl"),"jkl")
#layer1Node1 = Node(leaf1, leaf2, hash_MT(leaf1.hash_value+leaf2.hash_value))
#layer1Node2 = Node(leaf3, leaf4, hash_MT(leaf3.hash_value+leaf4.hash_value))
#rootNode = Node(layer1Node1, layer1Node2, hash_MT(layer1Node1.hash_value+layer1Node2.hash_value))
#######  YOUR CODE GOES HERE                              ######
#######     Change the return value                       ###### 

    while len(leafNodes)!=1:
        temp = []
        for i in range(0,len(leafNodes),2):
            node1 = leafNodes[i]
            if i+1 < len(leafNodes):
                node2 = leafNodes[i+1]
                concatenatedHash = node1.hash_value + node2.hash_value
                parentNode = Node(node1,node2,hash_MT(concatenatedHash))
                temp.append(parentNode)
            else:
                node2 = Node(None, None, hash_MT("<None>"),"<None>")
                concatenatedHash = node1.hash_value + node2.hash_value
                parentNode = Node(node1,node2,hash_MT(concatenatedHash))
                temp.append(parentNode)
                
                
        leafNodes = temp
            
    print(leafNodes[0])
    return leafNodes[0]
     
 

"""
Here are 2 small tests for generate_tree
"""

transactions = ["abc", "def", "ghi"]
MT_tree = generate_tree(transactions)
MT_check_three_node_example(MT_tree)


transactions = ["abc", "def", "ghi", "jkl"]
MT_tree = generate_tree(transactions)
MT_check_four_node_example(MT_tree)




"""
3.2 Generating a Proof of Membership in a Merkle Tree
In this section, you will be implementing a function to produce the proof of a transaction. 
The function will take two inputs, a transaction and the Merkle tree that contains it. 
The output of this function should be a list of hashes that a verify will use to check 
that a transaction was recorded in a tree.


                    H1234=H[H12||H34] 
               /                         \
     H12=H[H1||H2]                H34=H[H3||H4]
    /           \                 /           \
H1=H["abc"]   H2=H["def"]     H3=H["ghi"]     H4=H["jkl"]



Given the 4 leaf example from above, the proof for leaf1 (H1) is:

proof_value=[leaf2.hash_value, layer1Node2.hash_value]
proof_branch=[1, 1]

Note: leaf2 is the node with H2 and layer1Node2 is the node with H34

------------------------------

For leaf3 (H3), the proof would be:

proof_value=[leaf4.hash_value, layer1Node1.hash_value]
proof_branch=[1, 0]   

Note: leaf4 is the node with H4 and layer1Node1 is the node with H12 

The second array denotes if the hash value should be used as the first or second part of
of the concatenation. "0" means the start, "1" means the end (equivalently, the left or
right child).

This is because the root node (and its hash) is pubic knowledge. The proof allows a verifier
to compute if the transaction is in the tree:
 
The verifier computes:
    
H1 = Hash(Hash(transaction)||proof_value[0])
H2 = Hash(H1||proof_value[1])

Check if H2 == tree.hash_value

--------------------------------------------------------

transactions = ["abc"]
 H[H["abc"]||H["<None>"]]
     /           \
 H["abc"]       None
 
For the single transaction Merkle tree example from above, the proof would be:
    
proof_value=[hash_MT("<None>")]
proof_branch=[1]

The verifier computers:
    
H1 = Hash(Hash(transaction) || hash_MT("<None>"))

Check if H1 == tree.hash_value

--------------------------------------------------------
The input "tree" should be the root node of the tree.z
The input "transaction" should just be the string of the transaction

The output should be two lists, the proof_value and the proof_branch. Remember that 
in the proof_branch, "0" means that the given value in the proof branch should be at 
the start of the concatenation and "1" means that the value in the proof branch should 
be at the end of the concatenation.
"""
def generate_proof(tree, transaction):
#######  YOUR CODE GOES HERE                              ######
#######     Change the return value                       ######
    branchvalleft = []
    branchvalright=[]
    final =[]
    if tree.left.left == None:
      if tree.left.content == transaction:
            final = []
            final.append(tree.right)
      else:
            final = []
            final.append(tree.left) 
            
    templeftarray = []
    temprightarray = []
    templeft = tree.left
    templeftarray.append(tree.right.hash_value)
    branchvalleft.append(1)
    tempright = tree.right
    temprightarray.append(tree.left.hash_value)
    branchvalright.append(0)
    prev = templeft
    prevright = tree.right
    while(prev.left != None):
      
      templeft = prev.left
      if (templeft.content == transaction):
          templeftarray.insert(0,prev.right.hash_value)
          branchvalleft.insert(0,1)
          final.append(templeftarray)
          final.append(branchvalleft)
          print(final)
          return final
      right = prev.right
      if (right.content == transaction):
          templeftarray.insert(0,prev.left.hash_value)
          branchvalleft.insert(0,0)
          final.append(templeftarray)
          final.append(branchvalleft)
          print(final)
          return final
      prev = prev.left
      
      while(prevright.left!=None):
          
        templeft = prevright.left
        if (templeft.content == transaction):
          temprightarray.insert(0,prevright.right.hash_value)
          branchvalright.insert(0,1)
          final.append(temprightarray)
          final.append(branchvalright)
          print(final)
          return final
        tempright = prevright.right
        if (tempright.content == transaction):
          temprightarray.insert(0,prevright.left.hash_value)
          branchvalright.insert(0,0)
          final.append(temprightarray)
          final.append(branchvalright)
          print(final)
          return final
        prevright = prevright.left
    
   
    return tree.left.content

k = generate_proof(MT_tree,"abc")



"""
3.3 Verify a Proof for Merkle Tree
Given a Merkle tree and a proof of membership, implement a function to verify it. The input
will be a tree, a transaction, and the proof, and the function should return True or False.

Refer to the previous problem's comments for more details.
--------------------------------------------------------
The input "tree" should be the root node of the tree.
The input "proof_value" should be the hashes used in the proof.
The input "proof_branch" should denote which child the proof_value is on.
The input "transaction" should just be the string of the transaction

The output should be true or false
"""
def verify_proof(tree, proof_value, proof_branch, transaction):
#######  YOUR CODE GOES HERE                              ######
#######     Change the return value                       ######

    merkle_root = tree.hash_value
    
    target_hash = hash_MT(transaction)
    hash_value = hash_MT(target_hash+proof_value[0])
    final_value = ""
    temp = hash_value
    proof_value.pop(0)
    print(len(proof_value))
    if len(proof_value) == 0:
        return target_hash == merkle_root
    else:
       proof_hash = target_hash
       for p in proof_value:
           
           final_value = hash_MT(temp + p)
           temp = final_value
           
    
    print(tree.right.hash_value)
    print(proof_value[0])
    print(merkle_root == final_value)  
    print(merkle_root)
    print(final_value)  
    return merkle_root == final_value

verify_proof(MT_tree, k[0], k[1],"abc")
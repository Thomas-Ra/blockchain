import copy, json

from classes.blockchain import makeBlock
from classes.transactions import makeTransaction
from classes.validations import checkBlockValidity, checkChain

def chainFromFile(chain, state):
    """ method to load a blockchain from a file
    TODO: implement this method, needs some work on the file handling
    """
    chainAsText = json.dumps(chain, sort_keys = True)
    checkChain(json.loads(chainAsText))

def addNode(chain, state):
    """ method to add a node to the blockchain
    e.g. used in conjunction with the chainFromFile method"""
    nodeBlockChain = copy.copy(chain)
    nodeBlockTxns = [makeTransaction() for i in range(5)]
    newBlock = makeBlock(nodeBlockTxns, nodeBlockChain)

    print("Blockchain on node A is currently %s blocks long" % len(nodeBlockChain))
    try:
        print("New Block Received; checking validity...")
        state = checkBlockValidity(newBlock, nodeBlockChain[-1], state) # Update the state- this will throw an error if the block is invalid!
        nodeBlockChain.append(newBlock)
    except:
        print("Invalid block; ignoring and waiting for the next block...")

    print("Blockchain on node A is now %s blocks long" % len(nodeBlockChain))

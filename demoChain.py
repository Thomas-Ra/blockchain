import copy
import json
import sys
from classes.blockchain import hashMe, makeBlock
from classes.transactions import makeTransaction, isValidTxn, updateState
from classes.validations import checkBlockValidity, checkChain

#create a set of transactions
txnBuffer = [makeTransaction() for i in range(30)]

#do various transactions with a fix amount of money
state = {u'Alice':50, u'Bob':50}

# building genesis block that isnt linked to any other block (= starting block)
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0, u'parentHash':None, u'txnCount':1, u'txns':genesisBlockTxns}
genesisHash = hashMe(genesisBlockContents)
genesisBlock = {u'hash':genesisHash, u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys = True)

chain = [genesisBlock]

blockSizeLimit = 5 # determines how many transactions one block will contain

txnBuffer = [makeTransaction() for i in range(30)]

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn, state) # This will return False if txn is invalid
        
        if validTxn: # If we got a valid state, not 'False'
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on
        
## Make a block
myBlock = makeBlock(txnList, chain)
chain.append(myBlock)

# chain[0]
# chain[1]

print("\n", chain[0], "\n")
print("\n", chain[1], "\n")
print("\n", state, "\n")

checkChain(chain)

chainAsText = json.dumps(chain, sort_keys = True)
checkChain(json.loads(chainAsText))

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


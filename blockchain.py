import hashlib
import json
import sys

from transactions import makeTransaction, isValidTxn, updateState

def hashMe(msg=""):
    """helper function for wrapping hashing algo"""
    if type(msg) != str:
        msg = json.dumps(msg, sort_keys = True)
    if sys.version_info.major == 2:
        return (hashlib.sha256(msg).hexdigest(),'utf-8')
    else:
        return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()

def makeBlock(txns, chain):
    """each block collects a set of transactions, 
    has a header and will be hashed and linked to the blockchain"""
    parentBlock   = chain[-1]
    parentHash    = parentBlock[u'hash']
    blockNumber   = parentBlock[u'contents'] [u'blockNumber'] +1
    txnCount      = len(txns)
    blockContents = {u'blockNumber': blockNumber, u'parentHash': parentHash, u'txnCount': txnCount, 'txns': txns}
    blockHash     = hashMe(blockContents)
    block         = {u'hash': blockHash, u'contents': blockContents}

    return block

state = {u'Alice':50, u'Bob':50}

# building genesis block that isnt linked to any other block (= starting block)
genesisBlockTxns = [state]
genesisBlockContents = {u'blockNumber':0,u'parentHash':None,u'txnCount':1,u'txns':genesisBlockTxns}
genesisHash = hashMe(genesisBlockContents)
genesisBlock = {u'hash':genesisHash,u'contents':genesisBlockContents}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)

chain = [genesisBlock]

blockSizeLimit = 5 # determines how many transactions one block will contain

txnBuffer = [makeTransaction() for i in range(30)]

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)
    
    ## Gather a set of valid transactions for inclusion
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn,state) # This will return False if txn is invalid
        
        if validTxn:           # If we got a valid state, not 'False'
            txnList.append(newTxn)
            state = updateState(newTxn,state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue  # This was an invalid transaction; ignore it and move on
        
## Make a block
myBlock = makeBlock(txnList,chain)
chain.append(myBlock)

chain[0]
chain[1]

print("\n", chain[0], "\n")
print("\n", chain[1], "\n")
print("\n", state, "\n")


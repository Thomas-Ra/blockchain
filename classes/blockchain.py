import hashlib, json, sys

from classes.transactions import isValidTxn, updateState, makeTransaction

def printChain(state, chain):
    """helper function to print the blockchain"""
    for i in range(len(chain)):
        print("blockNumber: ", i)
        print(chain[i])
        print("\n")
    print(state)

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

def generateGenesisBlock(state):
    """ method to generate the genesis block of the blockchain
    the genesis block is the first block of the blockchain and is not linked to any other block
    """ 
    genesisBlockTxns = [state]
    genesisBlockContents = {u'blockNumber':0, u'parentHash':None, u'txnCount':1, u'txns':genesisBlockTxns}
    genesisHash = hashMe(genesisBlockContents)
    genesisBlock = {u'hash':genesisHash, u'contents':genesisBlockContents}
    genesisBlockStr = json.dumps(genesisBlock, sort_keys = True)
    return genesisBlock

def processTransactions(txnBuffer, blockSizeLimit, state):
    """ method to gather a set of valid transactions for inclusion in the next block
    """
    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn, state)
                    
        if validTxn:
            txnList.append(newTxn)
            state = updateState(newTxn, state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue
                
    return txnList, state


def makeBlockWithRandomTxns(state, chain, blockSizeLimit):
    """ method to create a block with a set of transactions
    create a set of transactions
    should be the same as the blocksize limit so that the transactions fit into one block
    otherwise you will need to create more blocks
    """
    txnBuffer = [makeTransaction() for i in range(blockSizeLimit)] 
    txnList, state = processTransactions(txnBuffer, blockSizeLimit, state)

    myBlock = makeBlock(txnList, chain) # make a block
    chain.append(myBlock) # make the block part of the blockchain
    # printChain(state, chain)
    return state

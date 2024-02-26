import json
from classes.blockchain import hashMe
from classes.transactions import isValidTxn

def checkBlockHash(block):
    """ Check whether block hash is valid
    If not valid, raise an exception
    """
    expectedHash = hashMe(block['contents'])
    if block['hash'] != expectedHash:
        raise Exception('Invalid block hash' %block['contents']['blockNumber'])
    return

def checkBlockValidity(block, parent, state):
    """Check whether block is valid
    If not valid, raise an exception
    a block is valid if:
    - the block number is one higher than the parent block
    - the block parent hash is the same as the parent hash
    - the transactions in the block are valid
    - the block hash is valid 
    - the block state is valid
    """
    parentNumber = parent['contents']['blockNumber']
    parentHash = parent['hash']
    blockNumber = block['contents']['blockNumber']
    
    # Check if the block number is one higher than the parent block
    if blockNumber != (parentNumber + 1):
        raise Exception('Invalid block number at block' %blockNumber)
    
    # Check if the block parent hash is the same as the parent hash
    if block['contents']['parentHash'] != parentHash:
        raise Exception('Invalid block parent hash at block:' %blockNumber)
    
    for txn in block['contents']['txns']:
        # Check if the transaction is valid
        if isValidTxn(txn,state):
            # Update the state
            state = updateState(txn,state)
        else:
            raise Exception('Invalid transaction in block' %(blockNumber, txn))

    # Check if the block hash is valid
    checkBlockHash(block)
    
    return state

def checkChain(chain):
    """Check whether the whole chain is valid (the first block needs a special treatment)
    The chain itself is valid if:
    - all transactions in the blocks are valid
    - there is no overdraft
    - the blocks are linked by their hashes
    Returns a dictionary of all account balances
    If not valid, return False
    """

    if type(chain) == str:
        try:
            chain = json.loads(chain)
            assert( type(chain) == list)
        except: # TODO: Specify the exception 
            return False
    elif type(chain) != list:
        return False
    
    # Check that each transaction is valid on the blockchain
    # Check that each block hash is valid for the contents of the block
    # First block has to be treated differently
    state = {}
    for txn in chain[0]['contents']['txns']:
        state = updateState(txn, state)
        checkBlockHash(chain[0])
        parent = chain[0]

    # Check the remaining blocks
    for block in chain[1:]:
        state = checkBlockValidity(block, parent, state)
        parent = block
    
    return state

def updateState(txn, state):
    """Update the state
    """
    # Update the state
    state = state.copy()
    
    for key in txn.keys():
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    
    return state
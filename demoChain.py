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

print("\nAlice and Bob start both with 50 money! First transaction Alice gives 3 money to bob.")
print(isValidTxn({u'Alice': -3, u'Bob': 3},state))
print("Transaction is valid. Alice has enough money to cover it.")

print("\nAlice wants to give an unequal amount of money to bob.")
print(isValidTxn({u'Alice': -4, u'Bob': 3},state))  # But we can't create or destroy tokens!
print("Transaction fails. Unequal money transfer are not eligble.")

print("\nAlice wants to give 6 money to bob.")
print(isValidTxn({u'Alice': -6, u'Bob': 6},state))  # We also can't overdraft our account.
print("Transaction fails. Alice has not enough funds.")

print("\nA new user is created. The amount of money from all three equals the start amount (10).")
print(isValidTxn({u'Alice': -4, u'Bob': 2,'Lisa':2},state)) # Creating new users is valid
print("New users can be created. Only 10 money is in the system.")

print("\nBob magically gets an additional money to his funds.")
print(isValidTxn({u'Alice': -4, u'Bob': 3,'Lisa':2},state)) # But the same rules still apply!
print("Fails. Sum of all money would be 11 and not 10.")

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


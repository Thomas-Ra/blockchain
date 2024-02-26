from classes.blockchain import generateGenesisBlock, makeBlockWithRandomTxns, printChain
from classes.validations import checkChain

state = {u'Alice':50, u'Bob':50} # do various transactions with a fix amount of money
blockSizeLimit = 5 # determines how many transactions one block will contain
generatedBlocks = 5 # how many blocks will be generated
maxTnxsValue = 3 # maximum value of each random transaction
# see random.seed() in classes/transactions.py; set to 0 to get the same random transactions

genesisBlock = generateGenesisBlock(state)
chain = [genesisBlock] # initialize the blockchain with the genesis block

for _ in range(generatedBlocks):
    state = makeBlockWithRandomTxns(state, chain, blockSizeLimit, maxTnxsValue)
    checkChain(chain)

printChain(state, chain)

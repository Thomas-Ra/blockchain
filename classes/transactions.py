import random
random.seed(0)

def makeTransaction(maxValue = 3):
    """ method to generate exchanges between two (and only two) personas
    depostits will be positive, withdrawls negative
    no money can be created or destroyed
    """

    #choose either -1 or 1
    sign = int(random.getrandbits(1))*2 - 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays

    return {u'Alice': alicePays, u'Bob': bobPays}

def updateState (txn, state):
    """ method to validate the transactions
    a user can only make a withdrawl with enough funds to cover it
    """

    state = state.copy()

    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state

def isValidTxn(txn, state):
    """Check whether an transaction is valid
    If not valid, return False
    the sum of all withdrawls and deposits have to be zero (no money is generated out of thin air)
    """
    if sum(txn.values()) != 0:
        return False
    
    #check if a user tries to spend money he dosent has
    for key in txn.keys():
        if key in state.keys():
            acctBalance =  state[key]
        else:
            acctBalance = 0
        if(acctBalance +  txn[key]) < 0:
            return False
        
    return True

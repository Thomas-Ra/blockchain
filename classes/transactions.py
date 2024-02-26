import random

random.seed(0)

def makeTransaction(maxValue):
    """ method to generate exchanges between two (and only two) personas
    depostits will be positive, withdrawls negative
    no money can be created or destroyed
    """

    #choose either -1 or 1
    sign = int(random.getrandbits(1)) * 2 - 1
    amount = random.randint(1, maxValue)
    alicePays = sign * amount
    bobPays = -1 * alicePays

    # print("Alice pays: ", alicePays, "Bob pays: ", bobPays)

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

#create a set of transactions
# txnBuffer = [makeTransaction() for i in range(30)]

"""testing the method to generate transactions
state = {u'Alice':5, u'Bob':5}
print("\nAlice and Bob start both with 5 money! First transaction Alice gives 3 money to bob.")
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
"""
import hashlib
import json
import sys

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

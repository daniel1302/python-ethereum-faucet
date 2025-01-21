from web3 import Web3, utils
from faucet.settings import APP_SETTINGS
import re 
import threading
from eth_account import Account
from web3.gas_strategies.time_based import fast_gas_price_strategy

w3 = Web3(Web3.HTTPProvider(APP_SETTINGS['RPC_ADDRESS']))
w3.eth.set_gas_price_strategy(fast_gas_price_strategy)

nonce_cache = 0
lock = threading.Lock()

def is_address_valid(address):
    addr_re = re.compile(r"^0x[a-f0-9]{40}$", re.IGNORECASE)
    return re.search(addr_re, address) != None


def get_wallet_for_private_key(private_key):
    account = Account.from_key(private_key)
    
    return account.address

def get_transaction(whale_private_key, amount_wei, receiver_address):
    global nonce_cache
    global lock

    account = Account.from_key(whale_private_key)
    with lock:
        # There may be some transactions in the cache that are not 
        # reflected in the node we are connected to yet.
        if nonce_cache < 1:
            nonce_cache = w3.eth.get_transaction_count(account.address)
        else:
            nonce_cache = nonce_cache + 1
    
    tx = {
        'chainId': w3.eth.chain_id,
        'nonce': nonce_cache,  
        'to': receiver_address,
        'value': amount_wei,
        'gasPrice': w3.eth.generate_gas_price()*3,
        'gas': 3000000,
    }
    
    # gas = w3.eth.estimate_gas(tx)
    
    signed = w3.eth.account.sign_transaction(tx, whale_private_key)
    
    return signed

def send_transaction(signed_tx):
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt
import os
from dotenv import load_dotenv
import json 
from web3 import Web3
from solcx import compile_standard
import solcx

load_dotenv()

solcx.install_solc('0.8.4')

with open("./contracts/SimpleStorage.sol", 'r') as f:
	simple_storage_file = f.read()


compiled = compile_standard({
	"language": "Solidity",
	"sources": {"SimpleStorage": {"content": simple_storage_file}},
	"settings": {"outputSelection": {
		"*": {"*": ['abi', 'metadata', 'evm.bytecode', 'evm.sourcemap']}
	}}
}, solc_version="0.8.4")

with open("compiled_code.json", 'w') as f: 
	json.dump(compiled, f)


# get bytecode
bytecode = compiled['contracts']['SimpleStorage']['SimpleStorage']['evm']['bytecode']['object']
# get abit
abi = compiled['contracts']['SimpleStorage']['SimpleStorage']['abi']

# Infura Rinkeby
w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/1153bc6fcb0a44b0858e6972eceae2d2'))
my_address = os.environ.get('MY_ADDRESS')
private_key = os.environ.get('PRIVATE_KEY')
chain_id = 4

# create contract
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latest transaction
nonce = w3.eth.getTransactionCount(my_address)
print(nonce)

available_accounts = w3.eth.accounts
# w3.eth.default_account = w3.eth.accounts[0]

# 1. build transaction
transaction = SimpleStorage.constructor().buildTransaction({"chainId": chain_id, "from": my_address, "nonce": nonce})

# 2. sign transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# 3. send transaction
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
# send with wait period
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)


# Working with contracts --> need abi, contract address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# call --> simulate making call and getting a return value
# transact --> actually making state change

print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(1999).call())
# call again --> no state change because we just use call()
print(simple_storage.functions.retrieve().call())

# make transaction
# 1. create
store_transaction = simple_storage.functions.store(1999).buildTransaction({
	"chainId": chain_id, "from": my_address, "nonce": nonce + 1
})
# 2. sign
signed_store_transaction = w3.eth.account.sign_transaction(store_transaction, private_key)
# 3. send
send_store_transaction = w3.eth.send_raw_transaction(signed_store_transaction.rawTransaction)
# 4. get receipt
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_transaction)
print(transaction_receipt)
print(simple_storage.functions.retrieve().call())

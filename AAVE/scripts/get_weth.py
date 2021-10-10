from brownie import interface, network, config
from scripts.utils import get_account

def get_weth():
	account = get_account()
	# can use get_contract() but here we'll get it from config
	weth = interface.IWeth(config['networks'][network.show_active()]['weth_token'])
	# make a deposit
	tx = weth.deposit({"from": account, "value": 1e15})
	tx.wait(1)
	print(f"Received {1e15} WETH")
	return tx


def main():
	get_weth()
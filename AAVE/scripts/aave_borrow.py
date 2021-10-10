from functools import total_ordering
from web3 import Web3
from brownie import config, network, interface
from .utils import get_account
from .get_weth import get_weth

AMOUNT = Web3.toWei(0.0000001, "ether")

def main():
	account = get_account()
	erc20_address = config["networks"][network.show_active()]["weth_token"]
	# get weth
	if network.show_active() in ["mainnet-fork-alchemy"]:
		weth_amount = get_weth()
	# we need ABI, Address from AAVE
	lending_pool = get_lending_pool()

	# Approve sending out ERC20 tokens
	approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)

	# Deposit
	print('Depositing..')
	tx = lending_pool.deposit(erc20_address, AMOUNT, account.address, 0, {"from": account})
	tx.wait(1)
	print('Deposited!')

	borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)

def get_borrowable_data(lending_pool, account):
	# from aaave docs
	 (total_collateral_eth, 
	 total_debt_eth, 
	 available_borrow_eth, 
	 current_liquidation_threshold,
	 ltv,
	 health_factor) = lending_pool.getUserAccountData(account.address)

	 available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
	 total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
	 total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
	 print(f"You have {total_collateral_eth} ETH deposited.")
	 print(f"You have borrowd {total_debt_eth} ETH.")
	 print(f"You can borrow {available_borrow_eth} ETH.")
	 return (float(available_borrow_eth), float(total_debt_eth))



	 

def approve_erc20(amount, spender, erc20_address, account):
	print("Approving ERC20 Token...")
	# need ABI, Address
	erc20 = interface.IERC20(erc20_address)
	tx = erc20.approve(spender, amount, {"from": account})
	tx.wait(1)
	print("Approved.")
	return tx


def get_lending_pool():
	# So this is a contract, therefore we need ABI and Address (we can copy and paste from actual contract,
	# but we'll use interface)
	lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
	config["networks"][network.show_active()]["lending_pool_addresses_provider"]
	)
	# address --> interfaces/ILendingPoolAddressesProvider.sol
	lending_pool_address = lending_pool_addresses_provider.getLendingPool()
	# ABI --> interfaces/ILendingPool.sol
	lending_pool = interface.ILendingPool(lending_pool_address)
	return lending_pool

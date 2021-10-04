import decimal
import logging
from os import link
from toolz.itertoolz import get
from web3 import Web3
from brownie import accounts, config, network, MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken

DECIMALS = 8
INITIAL_VALUE = 20000000000

FORKED_LOCAL_ENV = ['mainnet-fork', 'mainnet-fork-alchemy']
LOCAL_DEVS = ['development', 'ganache-local']

logger = logging.getLogger(__name__)


def get_account(index=None, id=None):
	if index:
		return accounts[index]
	if id:
		return accounts.load(id)
	if network.show_active() in LOCAL_DEVS or network.show_active() in FORKED_LOCAL_ENV:
		return accounts[0]
	return accounts.add(config['wallets']['from_key'])

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator,
					"vrf_coordinator": VRFCoordinatorMock,
					"link_contract": LinkToken}

def get_contract(contract_name):
	"""
	Grab contract addresses from brownie config if defined, otherwise deploy mocks and return mock contract
	Args:
		contract_name (string)
	Returns:
		brownie.network.contract.ProjectContract: The most recent deployed one, i.e., MockV3Aggreator[-1]
	"""
	contract_type = contract_to_mock[contract_name]
	if network.show_active() not in LOCAL_DEVS:
		if len(contract_type) <= 0:  # equivalent to MockV3Aggregator.length
			deploy_mocks()
		contract = contract_type[-1]  # equivalent to MockV3Aggregator[-1]
	else:
		# Address
		contract_address = config['networks'][network.show_active()][contract_name]
		# ABI
		contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
	return contract


def deploy_mocks(decimal=DECIMALS, initial_value=INITIAL_VALUE):
	account = get_account()
	MockV3Aggregator.deploy(decimal, initial_value, {"from": account})
	logger.debug("MockV3Aggregator Deployed!")
	link_token = LinkToken.deploy({"from": account})
	logger.debug("LinkToken Deployed!")
	VRFCoordinatorMock.deploy(link_token.address, {"from": account})
	logger.debug("VRFCoordinator Deployed!")


def fund_with_link(contract_address, account=None, link_token=None, amount=10000000000000000):  # 0.1 LINK
	account = account if account else get_account()
	link_token = link_token if link_token else get_contract("link_contract")
	tx = LinkToken.transfer(contract_address, amount, {"from": account})
	tx.wait(1)
	logger.debug("Contract funded with LINK!")
	return tx
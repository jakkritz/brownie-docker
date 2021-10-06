import logging
from web3 import Web3
from brownie import accounts, config, network, Contract

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


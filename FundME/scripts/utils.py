import logging
from web3 import Web3
from brownie import accounts, config, network, MockV3Aggregator

DECIMALS = 8
STARTING_PRICE = 200000000000 

FORKED_LOCAL_ENV = ['mainnet-fork', 'mainnet-fork-alchemy']
LOCAL_DEVS = ['development', 'ganache-local']

logger = logging.getLogger(__name__)

def get_account():
    if network.show_active() in LOCAL_DEVS or network.show_active() in FORKED_LOCAL_ENV:
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, 
            Web3.toWei(STARTING_PRICE, "ether"), 
            {"from": get_account()}
        )  # toWei == add 18 decimals
        logger.debug("... mocks deployed!")
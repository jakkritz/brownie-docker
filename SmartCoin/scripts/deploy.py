import logging
from toolz.itertoolz import get
from web3 import Web3
from brownie import config, network, SmartToken
from scripts.utils import get_account

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-32s %(levelname)-8s\n%(message)s",
    filename="deploy.log",
    filemode="w",
    datefmt="%m-%d-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


initial_supply = Web3.toWei(1000, 'ether')


def deploy_token():
	account = get_account()
	smart_token = SmartToken.deploy(initial_supply, {"from": account})
	print(smart_token.name())


def main():
	deploy_token()
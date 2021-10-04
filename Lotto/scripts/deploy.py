import logging
from brownie import Lottery, config, network
from brownie.network import account
from toolz.itertoolz import get
from scripts.utils import get_account, get_contract

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-32s %(levelname)-8s\n%(message)s",
    filename="deploy.log",
    filemode="w",
    datefmt="%m-%d-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


def deploy_lottery():
	# account = get_account(id='testaccount')
	account = get_account()
	lottery = Lottery.deploy(
		get_contract("eth_usd_price_feed").address, 
		get_contract("vrf_coordinator").address,
		get_contract("link_contract").address,
		config["networks"][network.show_active()].get("fee"),
		config["networks"][network.show_active()].get("keyhash"),
		{'from': account},
		publish_source=config['networks'][network.show_active()].get("verify", False))

def start_lottery():
	account = get_account()
	lottery = Lottery[-1]
	start_lotto_tx = lottery.startLottery({"from": account})
	start_lotto_tx.wait(1)
	logger.debug("Lottery has started...")

def enter_lottery():
	account = get_account()
	lottery = Lottery[-1]
	value = lottery.getEntranceFee() + 100  # plus tips
	enter_lotto_tx = lottery.enter({"from": account, "value": value})
	enter_lotto_tx.wait(1)
	logger.debug("Entered Lottery!")


def end_lottery():
	account = get_account()
	lottery = Lottery[-1]
	# fund contracts with LINK
	# draw winners
	# end lotto
	lottery.endLottery()
	logger.debug("Entered Lottery!")


def main():
	deploy_lottery()
	start_lottery()
	enter_lottery()
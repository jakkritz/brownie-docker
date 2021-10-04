import time
import logging
from web3 import Web3
from brownie import Lottery, config, network
from scripts.utils import get_account, get_contract, fund_with_link

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
	logger.debug("Lottery Deployed!")
	return lottery

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
	tx = fund_with_link(lottery.address)
	tx.wait(1)
	# draw winners
	# end lotto
	end_tx = lottery.endLottery({'from': account, 'gas': 1000000, 'gasPrice': Web3.toWei(2, 'gwei')})
	end_tx.wait(1)
	logger.debug("Entered Lottery!")
	# sleep to wait form randomness number from link
	time.sleep(60)
	logger.debug(f"Recent winner is {lottery.recentWinner()} !!!")


def main():
	deploy_lottery()
	start_lottery()
	enter_lottery()
	end_lottery()
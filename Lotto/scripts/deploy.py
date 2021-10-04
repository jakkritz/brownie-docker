from brownie import Lottery, config, network
from toolz.itertoolz import get
from scripts.utils import get_account, get_contract

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

def main():
	deploy_lottery()
# current eth = 3,427.36 USD
# minimum in eth = 50 / 3,427.36 = 0.01458848793

from web3 import Web3
from brownie import Lottery, accounts, network, config


def test_entrance_fee():

    print(network.show_active().upper())

    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()].get("eth_usd_price_feed"),
        {"from": account},
    )

    print(f'Current Price = {Web3.toWei(lottery.getEntranceFee(), "ether")}')

    assert lottery.getEntranceFee() > Web3.toWei(0.013, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.015, "ether")

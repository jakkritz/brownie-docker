# current eth = 3,427.36 USD
# minimum in eth = 50 / 3,427.36 = 0.01458848793

from web3 import Web3
from brownie import Lottery, accounts, network, config
from scripts.deploy import deploy_lottery

def test_deploy_lottery():
    # Arrange
    lottery = deploy_lottery()
    # Act
    entrance_fee = lottery.getEntranceFee()
    # Assert
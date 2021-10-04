# current eth = 3,427.36 USD
# minimum in eth = 50 / 3,427.36 = 0.01458848793

from web3 import Web3
from brownie import Lottery, accounts, network, config
from scripts.deploy import deploy_lottery

def test_deploy_lottery():
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 3,345.19 usd to eth
    # 50 usd = 3345.19/50 = 0.01494595
    expected_entrance_fee = Web3.toWei(0.15, 'ether')
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee
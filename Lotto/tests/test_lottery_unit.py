# current eth = 3,427.36 USD
# minimum in eth = 50 / 3,427.36 = 0.01458848793

import pytest
from web3 import Web3
from brownie import Lottery, accounts, network, config, exceptions
from scripts.deploy import deploy_lottery
from scripts.utils import LOCAL_DEVS, get_account


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_DEVS:
        pytest.skip("Only for local dev.")
    # Arrange
    lottery = deploy_lottery()
    # Act
    # 3,345.19 usd to eth
    # 50 usd = 3345.19/50 = 0.01494595
    # FIXME: 0.015 != 0.025
    expected_entrance_fee = Web3.toWei(0.015, 'ether')
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_start_unless_started():
    if network.show_active() not in LOCAL_DEVS:
        pytest.skip("Only for local dev.")
    
    lottery = deploy_lottery()

    with pytest.raises(expected_exception=exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), 
                       "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lotto():
    if network.show_active() not in LOCAL_DEVS:
        pytest.skip("Only for local dev.")
    
    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account

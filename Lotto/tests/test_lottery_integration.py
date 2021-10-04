# current eth = 3,427.36 USD
# minimum in eth = 50 / 3,427.36 = 0.01458848793

import time
import pytest
from web3 import Web3
from brownie import Lottery, accounts, network, config
from scripts.deploy import deploy_lottery
from scripts.utils import LOCAL_DEVS, fund_with_link, get_account, get_contract

def test_can_pick_winner():
    if network.show_active() in LOCAL_DEVS:
        pytest.skip("Only testing on TESTNETs")
    
    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})

    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})

    fund_with_link(lottery.address)

    tx = lottery.endLottery({"from": account})

    time.sleep(60)

    requestId = tx.events["RequestedRandomness"]["requestId"]

    SEED = 999

    get_contract("vrf_coordinator").callBackWithRandomness(requestId, SEED, lottery.address, {"from": address})

    # 999 % 3 = 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0



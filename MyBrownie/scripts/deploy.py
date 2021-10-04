import os
import sys
from brownie import accounts, config, network, SimpleStorage


def get_account():
    # switch local/infura account
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])


def deploy_simple_storage():
    # brownie accounts new testaccount
    # brownie accounts list
    # brownie accounts delete testaccount
    # account = accounts.load("testaccount")

    # use .env
    # account = accounts.add(os.environ.get("PRIVATE_KEY"))

    # use brownie-config.yaml
    account = get_account()
    account_dict = {"from": account}
    simple_storage = SimpleStorage.deploy(account_dict)
    simple_storage.retrieve()
    print(simple_storage.retrieve())
    transaction = simple_storage.store(1983929, account_dict)
    transaction.wait(1)
    print(simple_storage.retrieve())


def main():
    deploy_simple_storage()

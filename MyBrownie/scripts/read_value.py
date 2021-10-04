from brownie import accounts, config, SimpleStorage


def read_contract():
    latest_simple_storage = SimpleStorage[-1]
    print(latest_simple_storage.retrieve())


def main():
    read_contract()

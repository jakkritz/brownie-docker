from brownie import SimpleStorage, accounts

# brownie test
# brownie test -s
# brownie test -k test_deploy
# brownie test --pdb


def test_deploy():
    # arrange
    account = accounts[0]
    account_dict = {"from": account}
    # act
    simple_storage = SimpleStorage.deploy(account_dict)
    start_value = simple_storage.retrieve()
    # assert
    expected = 0
    assert start_value == expected


def test_update_value():
    # arrange
    account = accounts[0]
    account_dict = {"from": account}
    # act
    simple_storage = SimpleStorage.deploy(account_dict)
    simple_storage.store(9929, account_dict)
    update_value = simple_storage.retrieve()
    # assert
    expected = 9929
    assert update_value == expected

import logging
from brownie import FundMe
from scripts.utils import get_account

logger = logging.getLogger(__name__)


def fund():
	fund_me = FundMe[-1]
	account = get_account()
	entrance_fee = fund_me.getEntranceFee()
	logger.debug(f'Entrance Fee = {entrance_fee}.')
	fund_me.fund({'from': account, 'value': entrance_fee})


def withdraw():
	fund_me = FundMe[-1]
	account = get_account()
	fund_me.withdraw({'from': account})
	logger.debug(f'Withdrawn from {account.address}')


def main():
	fund()
	withdraw()

import logging
from brownie import FundMe, config, network, MockV3Aggregator
from scripts.utils import FORKED_LOCAL_ENV, get_account, deploy_mocks, LOCAL_DEVS


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-32s %(levelname)-8s %(message)s",
    filename="deploy.log",
    filemode="w",
    datefmt="%m-%d-%Y %H:%M:%S",
)
logger = logging.getLogger(__name__)


def deploy_fund_me():
    account = get_account()
    account_dict = {"from": account}
    # AggregatorV3Interface chainInterface = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
    if network.show_active() not in LOCAL_DEVS:
        logger.debug(f"Deploying on {network.show_active}")
        chainlink_interface = config["networks"][network.show_active()].get(
            "eth_usd_price_feed_chainlink_interface"
        )
    else:  # deploy mocks
        logger.debug(f"Deploying on {network.show_active().upper()}")
        deploy_mocks()

        # get address from deployed mocks
        chainlink_interface = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        chainlink_interface,
        account_dict,
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    logger.debug(f"Contract: FundMe has been deployed: {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()

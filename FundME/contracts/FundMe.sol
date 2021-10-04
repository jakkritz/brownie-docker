// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract FundMe {
	mapping(address => uint256) public addressToAmountFunded;
	address public owner;
	address[] public funders;
	AggregatorV3Interface public chainInterface;

	constructor(address _chainInterface) {
		chainInterface = AggregatorV3Interface(_chainInterface);
	    owner = msg.sender;
	}

	modifier onlyOwner {
	    require(msg.sender == owner);
	    _;
	}

	function fund() public payable {
	    uint256 minimumUSDAmount = 50 * 10 ** 18;
	    require(getConversionRate(msg.value) >= minimumUSDAmount, "Minimum amount is 50 USD!!!");
		addressToAmountFunded[msg.sender] += msg.value;
		funders.push(msg.sender);
	}

	/**
     * Network: Kovan
     * Aggregator: ETH/USD
     * Address: 0x9326BFA02ADD2366b30bacB125260Af641031331
     */
	function getVersion() public view returns (uint256) {
		// AggregatorV3Interface chainInterface = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
		uint256 version = chainInterface.version();
		return version;
	}

	function getLatestPrice() public view returns (uint256) {
	    // AggregatorV3Interface chainInterface = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
	    (, int256 answer, , , ) = chainInterface.latestRoundData();
	    return uint256(answer);
	}

	function getConversionRate(uint256 ethAmount) public view returns (uint256) {
	    uint256 latestPrice = getLatestPrice();
	    uint256 amountInUSD = (ethAmount * latestPrice) / 1000000000000000000;
	    return amountInUSD;

	}

	function withdraw() public onlyOwner payable {
	    payable(owner).transfer(address(this).balance);
	    for(uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
	        address funder = funders[funderIndex];
	        addressToAmountFunded[funder] = 0;
	    }
	    funders = new address[](0);
	}

	function getEntranceFee() public view returns (uint256) {
		uint256 minimumUSD = 50 * 10 ** 18;
		uint256 price = getLatestPrice();
		uint256 precision = 1 * 10 ** 18;
		return (minimumUSD * precision) / price;
	}

}
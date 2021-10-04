// SPDX-License-Identifier: MIT

pragma solidity ^0.8.4;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Lottery is VRFConsumerBase, Ownable {
	address payable[] public players;
	address payable public recentWinner;
	uint256 public usdEntryFee;
	uint256 public randomness;
	AggregatorV3Interface internal ethUsdPriceFeed;
	enum LOTTERY_STATE {
		OPEN,
		CLOSED,
		CALCULATING_WINNER
	}
	LOTTERY_STATE public lottery_state;

	uint256 public fees;
	bytes32 public keyhash;



	constructor(address _priceFeedAddress, address _vrfCoordinator, address _link, uint256 _fees, bytes32 _keyhash) 
		public 
		VRFConsumerBase(_vrfCoordinator, _link) {
			usdEntryFee = 50 * 10**18;
			ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
			lottery_state = LOTTERY_STATE.CLOSED;
			fees = _fees;
			keyhash = _keyhash;
	}

	function enter() public payable{
		// Must be open
		require(lottery_state == LOTTERY_STATE.OPEN, "Lottery is not in open state");
		// 50USD Minimum
		require(msg.value >= getEntranceFee(), "Minimum is 50 USD to Enter!");
		players.push(payable(msg.sender));

	}

	function getEntranceFee() public view returns (uint256) {
		(, int256 answer, , , ) = ethUsdPriceFeed.latestRoundData();
		uint256 adjustedPrice = uint256(answer) * 10**10;  // chainlink returns 8 decimal points, we need to convert it to 10e18
		uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
		return costToEnter;
	}

	function startLottery() public onlyOwner {
		require(lottery_state == LOTTERY_STATE.CLOSED, "Can't start lottery yet.");
		lottery_state = LOTTERY_STATE.OPEN;

	}

	function endLottery() public onlyOwner {
		// Create Random Number (bad way)
		// uint256(
		// 	keccak256(
		// 		abi.encodePacked(
		// 			nonce, 
		// 			msg.sender, 
		// 			block.difficulty, 
		// 			block.timestamp))) % players.length;
		// Use better method --> VRF Chainlink

		lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
		bytes32 requestId = requestRandomness(keyhash, fees);
	}

	function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
		require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, "Not Yet!");
		require(_randomness > 0, "Random Number Not Found!");
		uint256 indexOfWinner = _randomness % players.length;
		recentWinner = players[indexOfWinner];
		recentWinner.transfer(address(this).balance);
		// reset
		players = new address payable[](0);
		lottery_state = LOTTERY_STATE.CLOSED;
		randomness = _randomness;
	}
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract SimpleStorage {
	// init to 0
	uint256 favoriteNumber;
	struct People {
		uint256 favoriteNumber;
		string name;
	}

	People public person = People(101, "Jakkrit");

	People[] public people;

	mapping (string=>uint256) public nameToFavoriteNumber;

	function addPerson(string memory _name, uint256 _favoriteNumber) public {
		people.push(People(_favoriteNumber, _name));
		nameToFavoriteNumber[_name] = _favoriteNumber;
	}

	function store(uint256 _favoriteNumber) public returns (uint256) {
		favoriteNumber = _favoriteNumber;
		return _favoriteNumber;
	}

    // view ==> no state change made
    // pure ==> math, no state change made
	function retrieve() public view returns (uint256) {
		return favoriteNumber;
	}
}
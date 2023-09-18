// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.8.2 <0.9.0;

import "@openZeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract NFTFactory is ERC721URIStorage {
    uint256 public tokenCounter;
    address public factoryOwner;

    modifier onlyOwner {
        require(msg.sender == factoryOwner, "not owner");
        _;
    }
    constructor(string memory name, string memory symbol) ERC721(name, symbol) {
        factoryOwner = msg.sender;
    }

    function createCollectible(string memory tokenURI) public onlyOwner() {
        _safeMint(msg.sender, tokenCounter);
        _setTokenURI(tokenCounter, tokenURI);
        tokenCounter += 1;
    }
    function setOwner(address newOwner) public onlyOwner() {
        factoryOwner = newOwner;
    }


    

}
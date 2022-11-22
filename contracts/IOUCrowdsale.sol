pragma solidity ^0.5.5;

import "./IOU.sol";
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "@openzeppelin/contracts/crowdsale/Crowdsale.sol";
//import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "@openzeppelin/contracts/crowdsale/emission/MintedCrowdsale.sol";

// Bootstrap the IOUCrowdsale contract by inheriting the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract IOUCrowdsale is Crowdsale, MintedCrowdsale {
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint256 rate, // rate in TKNbits
        address payable wallet, // sale beneficiary
        IOUCoin token // the IOUCoin itself that the IOUCrowdsale will work with
    ) public Crowdsale(rate, wallet, token) {
        // constructor can stay empty
    }
}

contract IOUCrowdsaleDeployer {
    // Create an `address public` variable called `IOU_token_address`.
    address public iou_token_address;
    // Create an `address public` variable called `IOU_crowdsale_address`.
    address public iou_crowdsale_address;

    // Add the constructor.
    constructor(
        string memory name,
        string memory symbol,
        address payable wallet // this address will receive all Ether raised by the crowdsale
    ) public {
        // Create a new instance of the KaseiCoin contract.
        IOUCoin token = new IOUCoin(name, symbol, 0);

        // Assign the token contract’s address to the `iou_token_address` variable.
        iou_token_address = address(token);

        // Create a new instance of the `IOUCrowdsale` contract
        IOUCrowdsale iou_crowdsale = new IOUCrowdsale(1, wallet, token);

        // Aassign the `IOUCrowdsale` contract’s address to the `iou_crowdsale_address` variable.
        iou_crowdsale_address = address(iou_crowdsale);

        // Set the `IOUCrowdsale` contract as a minter
        token.addMinter(iou_crowdsale_address);

        // Have the `IOUCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}

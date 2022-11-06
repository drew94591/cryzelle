// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.7.5;

contract Loan {
    address payable accountOne;
    address payable accountTwo;
    address public lastToWithdraw;
    uint256 public lastWithdrawAmount;
    uint256 public contractBalance;

    constructor() {}

    function withdraw(uint256 amount, address payable recipient) public {
        require(
            recipient == accountOne || recipient == accountTwo,
            "You don't own this account!"
        );
        require(amount <= address(this).balance, "Insufficient funds!");

        if (lastToWithdraw != recipient) {
            lastToWithdraw = recipient;
        }

        recipient.transfer(amount);

        lastWithdrawAmount = amount;

        contractBalance = address(this).balance;
    }

    function deposit() public payable {
        contractBalance = address(this).balance;
    }

    function setAccounts(address payable account1, address payable account2)
        public
    {
        accountOne = account1;
        accountTwo = account2;
    }

    fallback() external payable {}

    receive() external payable {}
}

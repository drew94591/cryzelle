//var IOU = artifacts.require("./IOUCoin");

//module.exports = function (deployer)
//{
//    deployer.deploy(IOU, "Aracade", "ARCD", 1);
//};

//var crowdsale = artifacts.require("./IOUCrowdsale");
//const wallet_address = '0x625557F467B5A51ba473dd2394d85C733fBBf797';
//module.exports = function (deployer)
//{
//    deployer.deploy(crowdsale, 1, wallet_address, IOU);
//};

var IOUDeployer = artifacts.require("./IOUCrowdsaleDeployer");
const wallet_address = '0x625557F467B5A51ba473dd2394d85C733fBBf797';
module.exports = function (deployer)
{
    deployer.deploy(IOUDeployer, "Aracade", "ARCD", wallet_address);
};
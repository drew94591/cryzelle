var IOU = artifacts.require("./IOU.sol");

module.exports = function (deployer)
{
    deployer.deploy(IOU);
};


//var crowdsale = artifacts.require("./IOUCrowdsale");

//module.exports = function (deployer)
//{
//    deployer.deploy(crowdsale);
//};
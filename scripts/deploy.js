const hre = require("hardhat");

async function main() {
    console.log("🚀 Deploying MRVRegistry contract...");

    // Get contract factory
    const MRVRegistry = await hre.ethers.getContractFactory("MRVRegistry");

    // Deploy contract
    const mrvRegistry = await MRVRegistry.deploy();

    await mrvRegistry.waitForDeployment();

    const address = await mrvRegistry.getAddress();

    console.log("✅ MRVRegistry deployed to:", address);
    console.log("\n📝 Save this address to your .env file:");
    console.log(`CONTRACT_ADDRESS=${address}`);
    console.log("\n🔍 You can verify the contract on Etherscan (if on testnet/mainnet):");
    console.log(`npx hardhat verify --network <network> ${address}`);
}

// Execute deployment
main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });

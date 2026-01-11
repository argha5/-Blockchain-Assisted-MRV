// Configuration for MRV Verification Dashboard
// Update these values after deploying the smart contract

const CONFIG = {
    // Blockchain RPC URL (default: localhost)
    RPC_URL: "http://127.0.0.1:8545",

    // MRVRegistry contract address (update after deployment)
    CONTRACT_ADDRESS: "0x5FbDB2315678afecb367f032d93F642f64180aa3",

    // Contract ABI
    CONTRACT_ABI: [
        {
            "inputs": [
                { "name": "mrvId", "type": "string" },
                { "name": "hash", "type": "bytes32" }
            ],
            "name": "registerMRV",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [{ "name": "mrvId", "type": "string" }],
            "name": "getMRVHash",
            "outputs": [
                { "name": "", "type": "bytes32" },
                { "name": "", "type": "uint256" },
                { "name": "", "type": "address" }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [{ "name": "mrvId", "type": "string" }],
            "name": "isMRVRegistered",
            "outputs": [{ "name": "", "type": "bool" }],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                { "name": "mrvId", "type": "string" },
                { "name": "expectedHash", "type": "bytes32" }
            ],
            "name": "verifyMRVHash",
            "outputs": [{ "name": "valid", "type": "bool" }],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{ "name": "mrvId", "type": "string" }],
            "name": "getMRVRecord",
            "outputs": [
                {
                    "components": [
                        { "name": "hash", "type": "bytes32" },
                        { "name": "timestamp", "type": "uint256" },
                        { "name": "submitter", "type": "address" },
                        { "name": "exists", "type": "bool" }
                    ],
                    "name": "record",
                    "type": "tuple"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "anonymous": false,
            "inputs": [
                { "indexed": true, "name": "mrvId", "type": "string" },
                { "indexed": false, "name": "hash", "type": "bytes32" },
                { "indexed": false, "name": "timestamp", "type": "uint256" },
                { "indexed": true, "name": "submitter", "type": "address" }
            ],
            "name": "MRVRegistered",
            "type": "event"
        },
        {
            "anonymous": false,
            "inputs": [
                { "indexed": true, "name": "mrvId", "type": "string" },
                { "indexed": true, "name": "querier", "type": "address" }
            ],
            "name": "MRVQueried",
            "type": "event"
        }
    ]
};

"""
Blockchain integration module for MRV hash anchoring.
"""

import os
from typing import Optional, Dict, Any
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()


class BlockchainConnector:
    """Handles blockchain interactions for MRV hash anchoring."""
    
    def __init__(
        self,
        rpc_url: Optional[str] = None,
        contract_address: Optional[str] = None,
        private_key: Optional[str] = None
    ):
        """
        Initialize blockchain connector.
        
        Args:
            rpc_url: Blockchain RPC URL (default: localhost)
            contract_address: MRVRegistry contract address
            private_key: Private key for transactions
        """
        self.rpc_url = rpc_url or os.getenv("BLOCKCHAIN_RPC_URL", "http://127.0.0.1:8545")
        self.contract_address = contract_address or os.getenv("CONTRACT_ADDRESS")
        self.private_key = private_key or os.getenv("PRIVATE_KEY")
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.contract = None
        self.account = None
        
        # Load contract if address provided
        if self.contract_address:
            self._load_contract()
        
        # Load account if private key provided
        if self.private_key:
            self.account = self.w3.eth.account.from_key(self.private_key)
    
    def _load_contract(self):
        """Load smart contract instance."""
        # Contract ABI - simplified for MRVRegistry
        contract_abi = [
            {
                "inputs": [
                    {"name": "mrvId", "type": "string"},
                    {"name": "hash", "type": "bytes32"}
                ],
                "name": "registerMRV",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"name": "mrvId", "type": "string"}],
                "name": "getMRVHash",
                "outputs": [
                    {"name": "", "type": "bytes32"},
                    {"name": "", "type": "uint256"},
                    {"name": "", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [{"name": "mrvId", "type": "string"}],
                "name": "isMRVRegistered",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "mrvId", "type": "string"},
                    {"indexed": False, "name": "hash", "type": "bytes32"},
                    {"indexed": False, "name": "timestamp", "type": "uint256"},
                    {"indexed": True, "name": "submitter", "type": "address"}
                ],
                "name": "MRVRegistered",
                "type": "event"
            }
        ]
        
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=contract_abi
        )
    
    def is_connected(self) -> bool:
        """
        Check if connected to blockchain.
        
        Returns:
            True if connected
        """
        try:
            return self.w3.is_connected()
        except Exception:
            return False
    
    def anchor_hash(self, mrv_id: str, hash_value: str) -> Optional[str]:
        """
        Anchor MRV hash on blockchain.
        
        Args:
            mrv_id: MRV ID
            hash_value: SHA-256 hash (hex string)
            
        Returns:
            Transaction hash or None if failed
        """
        if not self.is_connected():
            print("⚠️  Warning: Not connected to blockchain. Skipping hash anchoring.")
            return None
        
        if not self.contract or not self.account:
            print("⚠️  Warning: Contract or account not configured. Skipping hash anchoring.")
            return None
        
        try:
            # Convert hex hash to bytes32
            hash_bytes = bytes.fromhex(hash_value)
            
            # Build transaction
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            transaction = self.contract.functions.registerMRV(
                mrv_id,
                hash_bytes
            ).build_transaction({
                'from': self.account.address,
                'nonce': nonce,
                'gas': 200000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.private_key
            )
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt['status'] == 1:
                tx_hash_hex = tx_hash.hex()
                print(f"✅ Hash anchored on blockchain: {tx_hash_hex[:10]}...")
                return tx_hash_hex
            else:
                print("❌ Transaction failed")
                return None
                
        except Exception as e:
            print(f"❌ Failed to anchor hash: {e}")
            return None
    
    def get_hash(self, mrv_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve MRV hash from blockchain.
        
        Args:
            mrv_id: MRV ID
            
        Returns:
            Dictionary with hash, timestamp, and submitter
        """
        if not self.is_connected() or not self.contract:
            return None
        
        try:
            result = self.contract.functions.getMRVHash(mrv_id).call()
            hash_bytes, timestamp, submitter = result
            
            # Check if registered
            if timestamp == 0:
                return None
            
            return {
                "hash": hash_bytes.hex(),
                "timestamp": timestamp,
                "submitter": submitter
            }
        except Exception as e:
            print(f"❌ Failed to retrieve hash: {e}")
            return None
    
    def verify_hash(self, mrv_id: str, expected_hash: str) -> bool:
        """
        Verify MRV hash against blockchain.
        
        Args:
            mrv_id: MRV ID
            expected_hash: Expected SHA-256 hash (hex string)
            
        Returns:
            True if hash matches
        """
        blockchain_data = self.get_hash(mrv_id)
        if blockchain_data is None:
            return False
        
        return blockchain_data["hash"] == expected_hash

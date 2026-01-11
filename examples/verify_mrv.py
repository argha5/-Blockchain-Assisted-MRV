"""
Command-line MRV verification tool

Usage:
    python verify_mrv.py <mrv_id> <json_file>
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mrv_wrapper.utils import compute_hash
from mrv_wrapper.blockchain import BlockchainConnector


def verify_mrv(mrv_id: str, json_file: str):
    """
    Verify MRV record against blockchain.
    
    Args:
        mrv_id: MRV identifier
        json_file: Path to MRV JSON file
    """
    print("="*60)
    print("MRV VERIFICATION")
    print("="*60)
    
    # Load JSON file
    print(f"\n📄 Loading: {json_file}")
    with open(json_file, 'r') as f:
        mrv_data = json.load(f)
    
    # Compute hash
    local_hash = compute_hash(mrv_data)
    print(f"✅ Computed hash: {local_hash}")
    
    # Connect to blockchain
    print(f"\n🔗 Connecting to blockchain...")
    blockchain = BlockchainConnector()
    
    if not blockchain.is_connected():
        print("❌ Error: Not connected to blockchain")
        print("   Make sure Hardhat node is running:")
        print("   npx hardhat node")
        return
    
    print("✅ Connected to blockchain")
    
    # Retrieve blockchain record
    print(f"\n🔍 Querying MRV ID: {mrv_id}")
    blockchain_data = blockchain.get_hash(mrv_id)
    
    if blockchain_data is None:
        print("❌ MRV ID not found on blockchain")
        return
    
    blockchain_hash = blockchain_data["hash"]
    timestamp = blockchain_data["timestamp"]
    submitter = blockchain_data["submitter"]
    
    from datetime import datetime
    dt = datetime.fromtimestamp(timestamp)
    
    print(f"✅ MRV found on blockchain")
    print(f"   Hash:      {blockchain_hash}")
    print(f"   Timestamp: {dt.isoformat()}")
    print(f"   Submitter: {submitter}")
    
    # Verify hash
    print(f"\n🔐 Verifying integrity...")
    if local_hash == blockchain_hash:
        print("✅ VALID - Hashes match!")
        print("   Data integrity verified")
    else:
        print("❌ TAMPERED - Hash mismatch!")
        print(f"   Local:      {local_hash}")
        print(f"   Blockchain: {blockchain_hash}")
    
    print("="*60)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python verify_mrv.py <mrv_id> <json_file>")
        print("\nExample:")
        print("  python verify_mrv.py MRV-abc123 mrv_data/MRV-abc123.json")
        sys.exit(1)
    
    mrv_id = sys.argv[1]
    json_file = sys.argv[2]
    
    verify_mrv(mrv_id, json_file)

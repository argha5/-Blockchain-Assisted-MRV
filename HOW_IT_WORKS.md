# 🔁 How It Works — File-by-File Execution Story

> **Complete execution flow with actual code — showing which file runs when, what it does, and how data flows**

This guide explains the **exact execution order** of the Blockchain-Assisted MRV system, not just theory.

---

## 📚 Table of Contents

1. [Quick Overview](#quick-overview)
2. [Execution Flow](#execution-flow)
3. [Verification Flow](#verification-flow)
4. [Code Deep Dive](#code-deep-dive)
5. [What Happens Under the Hood](#what-happens-under-the-hood)

---

## Quick Overview

### The Big Picture

```
User runs Python script
    ↓
MRVTracker wraps training
    ↓
CodeCarbon measures energy
    ↓
MRV JSON created
    ↓
Hash computed
    ↓
Saved to file
    ↓
Hash sent to blockchain
    ↓
✅ Immutable proof created
```

---

## Execution Flow

### 🟢 STEP 1 — User Runs ML Training Script

**File:** [`examples/simple_example.py`](file:///c:/GreenComputing/examples/simple_example.py)

#### Code:

```python
from mrv_wrapper import MRVTracker
import time

def my_training_function():
    """Simulate training workload."""
    print("Training started...")
    
    # Simulate training epochs
    for epoch in range(10):
        time.sleep(0.5)  # Simulate computation
        print(f"Epoch {epoch+1}/10 completed")
    
    print("Training completed!")

# Use MRV tracker
with MRVTracker(
    experiment_name="simple_example",
    model_name="MyModel",
    dataset_name="MyDataset",
    epochs=10,
    batch_size=32,
    framework="PyTorch"
) as tracker:
    my_training_function()

# MRV data automatically saved
print(f"\n✅ MRV ID: {tracker.mrv_id}")
```

#### What happens:

1. **Import**: `from mrv_wrapper import MRVTracker` loads the tracker module
2. **Context manager**: `with MRVTracker(...) as tracker:` creates a tracking context
3. **Training runs**: Your normal code executes inside the context
4. **Metadata provided**: Experiment name, model, dataset passed to tracker
5. **Auto-completion**: When context exits, MRV is automatically generated

📌 **This is the entry point** — everything starts here!

---

### 🟢 STEP 2 — MRVTracker Initializes

**File:** [`mrv_wrapper/tracker.py`](file:///c:/GreenComputing/mrv_wrapper/tracker.py)

#### Code:

```python
class MRVTracker:
    def __init__(
        self,
        experiment_name: str,
        model_name: str = "Unknown",
        dataset_name: str = "Unknown",
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        framework: Optional[str] = None,
        storage_dir: str = "mrv_data",
        registry_url: Optional[str] = None,
        blockchain_enabled: bool = True,
        auto_anchor: bool = True
    ):
        # Store experiment metadata
        self.experiment_name = experiment_name
        self.model_name = model_name
        self.dataset_name = dataset_name
        self.epochs = epochs
        self.batch_size = batch_size
        self.framework = framework
        
        # Initialize components
        self.storage = MRVStorage(storage_dir)
        self.blockchain_enabled = blockchain_enabled
        self.auto_anchor = auto_anchor
        
        # Blockchain connector
        if blockchain_enabled:
            self.blockchain = BlockchainConnector()
        
        # State variables
        self.emissions_tracker = None
        self.mrv_data = None
        self.mrv_id = None
        self.tx_hash = None
```

#### What happens:

1. **Stores metadata**: All experiment parameters saved
2. **Creates storage**: `MRVStorage` object for file I/O
3. **Blockchain setup**: If enabled, creates `BlockchainConnector`
4. **State initialization**: Variables set to `None` (filled later)

📌 **Nothing is tracked yet** — just setup!

---

### 🟢 STEP 3 — Context Manager Starts (`__enter__`)

**File:** [`mrv_wrapper/tracker.py`](file:///c:/GreenComputing/mrv_wrapper/tracker.py)

#### Code:

```python
def __enter__(self):
    """Start tracking when entering context."""
    self.start()
    return self

def start(self):
    """Start emission tracking."""
    print("🌱 Starting MRV tracking...")
    
    # Start timestamp
    self.start_time = time.time()
    self.start_time_iso = get_current_timestamp()
    
    # Start CodeCarbon tracker
    self.emissions_tracker = EmissionsTracker()
    self.emissions_tracker.start()
    
    print("📊 Tracking emissions with CodeCarbon...")
```

#### What happens:

1. **`with` statement triggers** `__enter__` method
2. **Start timestamp recorded**: `self.start_time = time.time()`
3. **CodeCarbon initialized**: `EmissionsTracker()` created
4. **Tracking begins**: `emissions_tracker.start()` called
5. **Returns self**: Allows `as tracker:` binding

📌 **CodeCarbon is now measuring!**

#### What CodeCarbon Does (External Library):

```python
# CodeCarbon (external library)
class EmissionsTracker:
    def start(self):
        # Monitor CPU power usage
        self.cpu_monitor = CPUMonitor()
        
        # Monitor GPU power usage (if available)
        self.gpu_monitor = GPUMonitor()
        
        # Start background thread
        self.tracking_thread = Thread(target=self._track)
        self.tracking_thread.start()
    
    def _track(self):
        while tracking:
            # Sample power every second
            cpu_power = measure_cpu_power()
            gpu_power = measure_gpu_power()
            total_power += (cpu_power + gpu_power)
```

📌 **Energy is measured continuously** during training

---

### 🟢 STEP 4 — User's Training Code Executes

**Back to:** [`examples/simple_example.py`](file:///c:/GreenComputing/examples/simple_example.py)

#### Code:

```python
def my_training_function():
    for epoch in range(10):
        time.sleep(0.5)  # Your actual model training here
        print(f"Epoch {epoch+1}/10 completed")
```

#### What happens:

- **Normal execution**: Your code runs unchanged
- **Background tracking**: CodeCarbon measures energy
- **No interference**: Tracking is transparent

📌 **This is where the actual ML work happens!**

---

### 🔴 STEP 5 — Context Manager Exits (`__exit__`)

**File:** [`mrv_wrapper/tracker.py`](file:///c:/GreenComputing/mrv_wrapper/tracker.py)

#### Code:

```python
def __exit__(self, exc_type, exc_val, exc_tb):
    """Stop tracking and save MRV data when exiting context."""
    self.stop()
    return False
```

#### What happens:

- **`with` block ends** → `__exit__` is called
- **`stop()` method triggered** → MRV generation starts
- **Exception handling**: If training crashes, still saves data

📌 **The magic happens in `stop()`!**

---

### 🟢 STEP 6 — Stop Tracking & Generate MRV

**File:** [`mrv_wrapper/tracker.py`](file:///c:/GreenComputing/mrv_wrapper/tracker.py)

#### Code (Simplified):

```python
def stop(self):
    """Stop emission tracking and generate MRV record."""
    
    # 1. Stop CodeCarbon
    print("📊 Stopping MRV tracking...")
    emissions = self.emissions_tracker.stop()
    self.end_time = get_current_timestamp()
    
    # 2. Extract emissions data
    self.emissions_data = {
        "energy_kwh": round(emissions, 6) if emissions else 0.0,
        "co2_kg": 0.0,
        "duration_seconds": self._calculate_duration()
    }
    
    # 3. Generate MRV record
    self._generate_mrv_record()
    
    # 4. Save locally
    self.mrv_id = self.storage.save_mrv(self.mrv_data)
    
    # 5. Anchor hash on blockchain
    if self.blockchain_enabled and self.auto_anchor:
        mrv_hash = compute_hash(self.mrv_data)
        self.tx_hash = self.blockchain.anchor_hash(self.mrv_id, mrv_hash)
    
    # 6. Print summary
    self._print_summary()
```

#### What happens (detailed):

**Part 1: Stop CodeCarbon**
```python
emissions = self.emissions_tracker.stop()
# Returns total energy consumed in kWh
# Example: 0.000117
```

**Part 2: Calculate Duration**
```python
def _calculate_duration(self):
    return round(time.time() - self.start_time, 2)
# Example: 10.50 seconds
```

**Part 3: Generate MRV JSON**
```python
def _generate_mrv_record(self):
    self.mrv_data = {
        "schema_version": "0.1",
        "mrv_id": self.storage.generate_mrv_id(),  # MRV-{uuid}
        "experiment": {
            "experiment_name": self.experiment_name,
            "model_name": self.model_name,
            "dataset_name": self.dataset_name
        },
        "training": {
            "epochs": self.epochs,
            "batch_size": self.batch_size,
            "framework": self.framework
        },
        "hardware": get_hardware_info(),  # CPU, GPU, RAM
        "energy_emissions": {
            "measurement_tool": "CodeCarbon",
            "energy_kwh": self.emissions_data["energy_kwh"],
            "co2_kg": self.emissions_data["co2_kg"],
            "duration_seconds": self.emissions_data["duration_seconds"]
        },
        "timestamps": {
            "start_time": self.start_time_iso,
            "end_time": self.end_time
        }
    }
```

📌 **Complete MRV JSON is now in memory!**

---

### 🟢 STEP 7 — Collect Hardware Information

**File:** [`mrv_wrapper/utils.py`](file:///c:/GreenComputing/mrv_wrapper/utils.py)

#### Code:

```python
def get_hardware_info() -> Dict[str, Any]:
    """Collect all hardware information."""
    
    # CPU info
    cpu_info = get_cpu_info()
    # Uses: platform.processor()
    # Example: "Intel64 Family 6 Model 140"
    
    # GPU info  
    gpu_info = get_gpu_info()
    # Uses: GPUtil.getGPUs()
    # Example: "NVIDIA GeForce RTX 3090"
    
    # RAM info
    ram_gb = get_ram_info()
    # Uses: psutil.virtual_memory().total
    # Example: 16 GB
    
    return {
        "cpu_type": cpu_info["cpu_type"],
        "cpu_cores": cpu_info["cpu_cores"],
        "gpu_type": gpu_info["gpu_type"],
        "num_gpus": gpu_info["num_gpus"],
        "ram_gb": ram_gb,
        "gpu_memory_gb": gpu_info.get("gpu_memory_gb", 0)
    }
```

#### Libraries used:

```python
import platform  # CPU model
import psutil    # CPU cores, RAM
import GPUtil    # GPU detection
```

#### Example output:

```json
{
  "cpu_type": "Intel64 Family 6 Model 140 Stepping 1",
  "cpu_cores": 8,
  "gpu_type": "NVIDIA GeForce MX350",
  "num_gpus": 1,
  "ram_gb": 16,
  "gpu_memory_gb": 2
}
```

📌 **Hardware snapshot ensures reproducibility!**

---

### 🟢 STEP 8 — Compute SHA-256 Hash

**File:** [`mrv_wrapper/utils.py`](file:///c:/GreenComputing/mrv_wrapper/utils.py)

#### Code:

```python
def compute_hash(data: Dict[str, Any]) -> str:
    """
    Compute SHA-256 hash of MRV JSON data.
    
    Args:
        data: MRV JSON dictionary
        
    Returns:
        Hexadecimal hash string
    """
    # Ensure deterministic JSON serialization
    json_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
    
    # Compute SHA-256
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
```

#### Why `sort_keys=True`?

**Without sorting:**
```python
{"b": 2, "a": 1}  → hash1
{"a": 1, "b": 2}  → hash2  # Different hash!
```

**With sorting:**
```python
{"b": 2, "a": 1}  → sorted → {"a": 1, "b": 2} → hash1
{"a": 1, "b": 2}  → sorted → {"a": 1, "b": 2} → hash1  # Same hash!
```

#### Example:

```python
mrv_data = {"mrv_id": "MRV-abc", "energy_kwh": 0.5}

# Serialize
json_str = '{"energy_kwh":0.5,"mrv_id":"MRV-abc"}'

# Hash
hash = "213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1"
```

📌 **This hash is the cryptographic fingerprint!**

---

### 🟢 STEP 9 — Save MRV JSON to File

**File:** [`mrv_wrapper/storage.py`](file:///c:/GreenComputing/mrv_wrapper/storage.py)

#### Code:

```python
class MRVStorage:
    def __init__(self, storage_dir: str = "mrv_data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)  # Create folder if missing
    
    def generate_mrv_id(self) -> str:
        """Generate unique MRV ID."""
        return f"MRV-{uuid.uuid4()}"
        # Example: "MRV-fc25ba52-f439-4834-be2b-2dbae1e03437"
    
    def save_mrv(self, mrv_data: Dict[str, Any], mrv_id: Optional[str] = None) -> str:
        """Save MRV data to local file."""
        
        # Use existing or generated ID
        if mrv_id is None:
            mrv_id = mrv_data.get("mrv_id") or self.generate_mrv_id()
        
        # Create filename
        filename = f"{mrv_id}.json"
        filepath = self.storage_dir / filename
        
        # Write JSON (sorted keys for consistency)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mrv_data, f, indent=2, sort_keys=True)
        
        print(f"✅ MRV data saved: {filepath}")
        return mrv_id
```

#### What happens:

1. **Folder check**: Creates `mrv_data/` if it doesn't exist
2. **ID generation**: `uuid.uuid4()` creates unique identifier
3. **File write**: JSON saved with pretty formatting (`indent=2`)
4. **Sorted keys**: Ensures hash consistency

#### Result:

```
mrv_data/
 └── MRV-fc25ba52-f439-4834-be2b-2dbae1e03437.json
```

#### File contents:

```json
{
  "energy_emissions": {
    "co2_kg": 0.0,
    "duration_seconds": 10,
    "energy_kwh": 0.000117,
    "measurement_tool": "CodeCarbon"
  },
  "experiment": {
    "dataset_name": "MyDataset",
    "experiment_name": "simple_example",
    "model_name": "MyModel"
  },
  ...
}
```

📌 **Human-readable, shareable file created!**

---

### 🟢 STEP 10 — Anchor Hash on Blockchain

**File:** [`mrv_wrapper/blockchain.py`](file:///c:/GreenComputing/mrv_wrapper/blockchain.py)

#### Code:

```python
def anchor_hash(self, mrv_id: str, hash_value: str) -> Optional[str]:
    """Anchor MRV hash on blockchain."""
    
    # 1. Check connection
    if not self.is_connected():
        print("⚠️  Warning: Not connected to blockchain.")
        return None
    
    try:
        # 2. Convert hex hash to bytes32
        hash_bytes = bytes.fromhex(hash_value)
        # "213ad9a..." → b'\x21\x3a\xd9...'
        
        # 3. Get transaction nonce (transaction count)
        nonce = self.w3.eth.get_transaction_count(self.account.address)
        
        # 4. Build transaction
        transaction = self.contract.functions.registerMRV(
            mrv_id,      # "MRV-fc25ba52..."
            hash_bytes   # bytes32
        ).build_transaction({
            'from': self.account.address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # 5. Sign transaction with private key
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction,
            private_key=self.private_key
        )
        
        # 6. Send transaction to blockchain
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # 7. Wait for confirmation
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # 8. Check if successful
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
```

#### What happens (detailed):

**Step 2: Convert hash format**
```python
# From: "213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1"
# To: b'\x21\x3a\xd9\xa9\x2b\xa3\x75\x3d...' (32 bytes)
```

**Step 3: Get nonce**
```python
nonce = self.w3.eth.get_transaction_count(account)
# Returns: 0 (if first transaction from this account)
```

**Step 4: Build transaction**
```python
transaction = {
    'from': '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266',
    'to': '0x5FbDB2315678afecb367f032d93F642f64180aa3',  # Contract
    'nonce': 0,
    'gas': 200000,
    'gasPrice': 875000000,  # wei
    'data': '0x...'  # Encoded function call
}
```

**Step 5: Sign**
```python
# Digital signature proves you own the private key
# Without revealing the key itself
signed = sign(transaction, private_key)
```

**Step 6: Send**
```python
# Broadcast to blockchain network
tx_hash = send(signed_transaction)
# Returns: 0x4d8e1f2a3b9c...
```

**Step 7: Wait for confirmation**
```python
# On localhost: instant
# On Ethereum mainnet: ~15 seconds
receipt = wait_for_receipt(tx_hash)
```

📌 **Hash is now on blockchain — immutable forever!**

---

### 🟢 STEP 11 — Smart Contract Stores Hash

**File:** [`contracts/MRVRegistry.sol`](file:///c:/GreenComputing/contracts/MRVRegistry.sol)

#### Code:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MRVRegistry {
    
    // Data structure
    struct MRVRecord {
        bytes32 hash;       // SHA-256 hash
        uint256 timestamp;  // When registered
        address submitter;  // Who registered
        bool exists;        // Exists flag
    }
    
    // Storage: MRV ID → Record
    mapping(string => MRVRecord) private mrvRecords;
    
    // Event emitted when MRV registered
    event MRVRegistered(
        string indexed mrvId,
        bytes32 hash,
        uint256 timestamp,
        address indexed submitter
    );
    
    /**
     * @dev Register a new MRV record
     */
    function registerMRV(string memory mrvId, bytes32 hash) external {
        // Validation: cannot overwrite
        require(!mrvRecords[mrvId].exists, "MRV ID already registered");
        require(hash != bytes32(0), "Hash cannot be zero");
        
        // Store record
        mrvRecords[mrvId] = MRVRecord({
            hash: hash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            exists: true
        });
        
        // Emit event (public log)
        emit MRVRegistered(mrvId, hash, block.timestamp, msg.sender);
    }
    
    /**
     * @dev Get MRV record details
     */
    function getMRVHash(string memory mrvId) 
        external 
        returns (bytes32 hash, uint256 timestamp, address submitter) 
    {
        MRVRecord memory record = mrvRecords[mrvId];
        return (record.hash, record.timestamp, record.submitter);
    }
}
```

#### What the blockchain stores:

```
mrvRecords["MRV-fc25ba52-f439-4834-be2b-2dbae1e03437"] = {
    hash: 0x213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1,
    timestamp: 1736584707,  // Unix timestamp
    submitter: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266,
    exists: true
}
```

#### Key security features:

✅ **Immutability**: `require(!mrvRecords[mrvId].exists)` prevents overwrites  
✅ **Transparency**: `emit MRVRegistered(...)` creates public log  
✅ **Timestamp**: `block.timestamp` provides audit trail

📌 **Data is now permanently on blockchain!**

---

### 🟢 STEP 12 — User Gets Confirmation

**Back to:** [`examples/simple_example.py`](file:///c:/GreenComputing/examples/simple_example.py)

#### Code:

```python
# MRV data automatically saved
print(f"\n✅ MRV ID: {tracker.mrv_id}")
print(f"✅ MRV file saved at: mrv_data/{tracker.mrv_id}.json")
```

#### Output:

```
✅ MRV ID: MRV-fc25ba52-f439-4834-be2b-2dbae1e03437
✅ MRV file saved at: mrv_data/MRV-fc25ba52-f439-4834-be2b-2dbae1e03437.json
✅ Hash anchored on blockchain: 0x4d8e1f2a...
```

#### What the user now has:

1. ✅ **MRV ID**: `MRV-fc25ba52...`
2. ✅ **JSON file**: `mrv_data/MRV-fc25ba52....json`
3. ✅ **Blockchain proof**: Transaction hash `0x4d8e1f2a...`
4. ✅ **Verifiable claim**: Can be independently verified

📌 **Training complete with blockchain-backed proof!**

---

## Verification Flow

### 🟡 STEP 13 — User Wants to Verify

**File:** [`examples/verify_mrv.py`](file:///c:/GreenComputing/examples/verify_mrv.py)

#### Usage:

```bash
python examples/verify_mrv.py MRV-fc25ba52... mrv_data/MRV-fc25ba52....json
```

#### Code:

```python
import sys
import json
from mrv_wrapper.utils import compute_hash
from mrv_wrapper.blockchain import BlockchainConnector

def verify_mrv(mrv_id: str, json_file: str):
    # 1. Load JSON file
    print(f"📄 Loading: {json_file}")
    with open(json_file, 'r') as f:
        mrv_data = json.load(f)
    
    # 2. Compute local hash
    local_hash = compute_hash(mrv_data)
    print(f"✅ Computed hash: {local_hash[:10]}...")
    
    # 3. Connect to blockchain
    blockchain = BlockchainConnector()
    if not blockchain.is_connected():
        print("❌ Not connected to blockchain")
        return
    
    print("✅ Connected to blockchain")
    
    # 4. Retrieve stored hash
    blockchain_data = blockchain.get_hash(mrv_id)
    
    if blockchain_data is None:
        print("⚠️  NOT FOUND - MRV ID not registered on blockchain")
        return
    
    # 5. Compare hashes
    blockchain_hash = blockchain_data["hash"]
    
    print(f"🔐 Verifying integrity...")
    
    if local_hash == blockchain_hash:
        print("✅ VALID - Hashes match!")
        print(f"   Timestamp: {datetime.fromtimestamp(blockchain_data['timestamp'])}")
        print(f"   Submitter: {blockchain_data['submitter']}")
    else:
        print("❌ TAMPERED - Hash mismatch!")
        print(f"   Local:      {local_hash}")
        print(f"   Blockchain: {blockchain_hash}")

if __name__ == "__main__":
    verify_mrv(sys.argv[1], sys.argv[2])
```

---

### 🟢 STEP 14 — Local Hash Recomputed

**File:** [`mrv_wrapper/utils.py`](file:///c:/GreenComputing/mrv_wrapper/utils.py)

```python
local_hash = compute_hash(mrv_data)
# Same function as before
# Returns: "213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1"
```

📌 **If file was tampered, hash will be different!**

---

### 🟢 STEP 15 — Blockchain Queried

**File:** [`mrv_wrapper/blockchain.py`](file:///c:/GreenComputing/mrv_wrapper/blockchain.py)

#### Code:

```python
def get_hash(self, mrv_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve MRV hash from blockchain."""
    
    if not self.is_connected() or not self.contract:
        return None
    
    try:
        # Call smart contract (read-only, no gas cost)
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
```

#### What happens:

1. **Contract call**: `getMRVHash(mrv_id)` executed
2. **Read from storage**: Blockchain returns stored record
3. **Parse result**: Tuple unpacked to hash, timestamp, submitter

📌 **No gas cost** — reading is free!

---

### 🟢 STEP 16 — Hashes Compared

#### Code:

```python
if local_hash == blockchain_hash:
    print("✅ VALID - Hashes match!")
else:
    print("❌ TAMPERED - Hash mismatch!")
```

#### Possible outcomes:

**✅ VALID**
```
Local:      213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1
Blockchain: 213ad9a92ba3753dcf7ceb5a59d001e7755c0bffcc8f26baf1a1ad643cda58b1
Result: ✅ VALID - Data integrity verified
```

**❌ TAMPERED** (if someone changed the JSON)
```
Local:      a1b2c3d4...  (computed from modified file)
Blockchain: 213ad9a9...  (original hash)
Result: ❌ TAMPERED - File was modified!
```

**⚠️ NOT FOUND**
```
Blockchain: (no record found)
Result: ⚠️ NOT REGISTERED - MRV ID doesn't exist on chain
```

📌 **Cryptographic proof of integrity!**

---

## Code Deep Dive

### How Context Managers Work

#### Python Magic Methods:

```python
with MRVTracker(...) as tracker:
    train()

# Equivalent to:
tracker = MRVTracker(...)
tracker.__enter__()  # Called automatically
try:
    train()
finally:
    tracker.__exit__(None, None, None)  # Always called
```

#### Benefits:

✅ **Automatic cleanup**: `__exit__` always runs  
✅ **Exception safe**: Saves data even if training crashes  
✅ **Clean syntax**: No manual start/stop needed

---

### How SHA-256 Works

#### Cryptographic hash properties:

1. **Deterministic**: Same input → same hash (always)
2. **One-way**: Can't reverse (hash → original data)
3. **Collision-resistant**: Near-impossible to find two inputs with same hash
4. **Avalanche effect**: Tiny change → completely different hash

#### Example:

```python
data1 = '{"energy_kwh": 0.5}'
hash1 = "a1b2c3d4..."

data2 = '{"energy_kwh": 0.50001}'  # Tiny change!
hash2 = "9z8y7x6w..."  # Completely different!
```

📌 **This is why tampering is detectable!**

---

### How Blockchain Storage Works

#### Blockchain properties:

```
Block N
├── Transactions
│   ├── TX 1: registerMRV("MRV-abc", hash1)
│   ├── TX 2: registerMRV("MRV-xyz", hash2)
│   └── TX 3: ...
├── Block hash
└── Previous block hash (chain link)
```

#### Immutability mechanism:

1. **Merkle tree**: All transactions hashed together
2. **Block hash**: Hash of (transactions + previous block)
3. **Chain linking**: Changing old block breaks entire chain

📌 **Tampering requires rewriting entire blockchain!**

---

## What Happens Under the Hood

### Full Execution Timeline

```
0.0s  - User runs: python simple_example.py
0.1s  - MRVTracker.__init__() creates tracker object
0.2s  - with statement calls __enter__()
0.3s  - CodeCarbon tracker starts
0.3s  - my_training_function() begins
5.0s  - Training running... (energy being measured)
10.3s - Training completes
10.3s - with statement calls __exit__()
10.3s - stop() triggered
10.4s - CodeCarbon stopped, emissions retrieved
10.5s - Hardware info collected (CPU, GPU, RAM)
10.6s - MRV JSON assembled in memory
10.7s - SHA-256 hash computed
10.8s - JSON saved to mrv_data/MRV-....json
10.9s - Blockchain connection established
11.0s - Transaction built and signed
11.1s - Transaction sent to blockchain
11.2s - Waiting for confirmation...
11.3s - Transaction confirmed! (instant on localhost)
11.4s - Summary printed to user
11.5s - Script exits
```

### Memory Flow

```
Start:
  tracker.mrv_data = None
  tracker.mrv_id = None

After stop():
  tracker.mrv_data = {entire JSON dict}
  tracker.mrv_id = "MRV-fc25ba52..."
  tracker.tx_hash = "0x4d8e1f2a..."

End:
  User can access tracker.mrv_id
  File saved to disk
  Hash on blockchain
```

---

## File Dependency Chain

### Visual Flow:

```
simple_example.py
    │
    ├─→ mrv_wrapper/tracker.py
    │       │
    │       ├─→ codecarbon (external)
    │       ├─→ mrv_wrapper/utils.py
    │       ├─→ mrv_wrapper/storage.py
    │       └─→ mrv_wrapper/blockchain.py
    │               │
    │               └─→ web3 (external)
    │                       │
    │                       └─→ Blockchain RPC
    │                               │
    │                               └─→ MRVRegistry.sol
    │
    └─→ mrv_data/MRV-....json (output)
```

### Import Chain:

```python
# simple_example.py
from mrv_wrapper import MRVTracker

# mrv_wrapper/__init__.py
from .tracker import MRVTracker

# mrv_wrapper/tracker.py
from codecarbon import EmissionsTracker
from .utils import compute_hash, get_hardware_info
from .storage import MRVStorage
from .blockchain import BlockchainConnector

# mrv_wrapper/blockchain.py
from web3 import Web3

# mrv_wrapper/utils.py
import hashlib, json, psutil, GPUtil
```

---

## Summary: The Complete Picture

### What Each File Does:

| File | Purpose | Key Functions |
|------|---------|---------------|
| `simple_example.py` | **Entry point** | Wraps training with MRVTracker |
| `tracker.py` | **Orchestrator** | Coordinates all components |
| `utils.py` | **Utilities** | compute_hash(), get_hardware_info() |
| `storage.py` | **File I/O** | save_mrv(), load_mrv() |
| `blockchain.py` | **Web3 interface** | anchor_hash(), get_hash() |
| `MRVRegistry.sol` | **Smart contract** | registerMRV(), getMRVHash() |
| `verify_mrv.py` | **Verification** | Load JSON, compare hashes |

### Data Flow Summary:

```
Training Metadata → MRVTracker
CodeCarbon Data → emissions.json (in memory)
Hardware Info → utils.py → MRV JSON
MRV JSON → SHA-256 hash
JSON + Hash → Local file
Hash → Blockchain
Blockchain confirmation → User
```

### Why This Design Works:

1. **Separation of concerns**: Each file has one job
2. **Loose coupling**: Components are independent
3. **Extensible**: Easy to add new features
4. **Verifiable**: Anyone can check integrity
5. **Transparent**: All code is open source

---

## Next: Deep Dive Options

Want to explore more?

### 🧩 Sequence Diagrams
- Visual flow charts with timing
- UML diagrams of component interactions

### 📄 Paper-Ready Explanation
- Academic-style methodology section
- Formal algorithm descriptions

### 🔬 Algorithm Pseudocode
- Step-by-step algorithms
- Mathematical notation

### 🛠️ Simplified Beginner Version
- ELI5 (Explain Like I'm 5) version
- Analogies and metaphors

### 🔍 Advanced Topics
- Gas optimization strategies
- Multi-chain deployment
- Privacy-preserving MRV

---

**Built with 💚 for sustainable AI**

> For more details, see [ARCHITECTURE.md](ARCHITECTURE.md) or [README.md](README.md)

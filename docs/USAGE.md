# Detailed Usage Guide

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/blockchain-mrv-ml.git
cd blockchain-mrv-ml
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

### 3. Install Node.js Dependencies

```bash
npm install
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

---

## Quick Start

### Step 1: Start Local Blockchain

```bash
# Terminal 1: Start Hardhat node
npx hardhat node
```

This will start a local Ethereum node on `http://127.0.0.1:8545`.

### Step 2: Deploy Smart Contract

```bash
# Terminal 2: Deploy MRVRegistry contract
npx hardhat run scripts/deploy.js --network localhost
```

Copy the contract address and update `.env`:
```
CONTRACT_ADDRESS=0x5FbDB2315678afecb367f032d93F642f64180aa3
```

Also update `dashboard/config.js` with the contract address.

### Step 3: Run Example Training

```bash
# Run ResNet18 example
python examples/train_resnet.py

# Or run simple example
python examples/simple_example.py
```

### Step 4: Verify MRV Record

**Option A: Web Dashboard**
```bash
cd dashboard
python -m http.server 8080
# Open http://localhost:8080
# Upload the generated JSON and verify
```

**Option B: Command Line**
```bash
python examples/verify_mrv.py MRV-abc123 mrv_data/MRV-abc123.json
```

---

## Using MRV Tracker in Your Code

### Basic Usage

```python
from mrv_wrapper import MRVTracker

with MRVTracker(
    experiment_name="my_experiment",
    model_name="MyModel",
    dataset_name="MyDataset"
) as tracker:
    # Your training code here
    train_model()

# MRV data automatically saved
print(f"MRV ID: {tracker.mrv_id}")
```

### Advanced Usage

```python
from mrv_wrapper import MRVTracker

tracker = MRVTracker(
    experiment_name="resnet50_imagenet",
    model_name="ResNet50",
    dataset_name="ImageNet",
    epochs=100,
    batch_size=256,
    framework="PyTorch",
    storage_dir="my_mrv_data",  # Custom storage directory
    registry_url="https://api.mrv-registry.com",  # Optional registry
    blockchain_enabled=True,  # Enable blockchain
    auto_anchor=True  # Auto-anchor after training
)

# Manual start/stop
tracker.start()
train_model()
tracker.stop()

# Access data
mrv_data = tracker.get_mrv_data()
mrv_hash = tracker.get_hash()
mrv_id = tracker.mrv_id
tx_hash = tracker.tx_hash

# Verify on blockchain
is_valid = tracker.verify_on_blockchain()
```

### Without Blockchain

If you don't have a blockchain node running:

```python
with MRVTracker(
    experiment_name="my_experiment",
    blockchain_enabled=False  # Disable blockchain
) as tracker:
    train_model()

# MRV data still saved locally
```

---

## Testing

### Python Tests

```bash
pytest tests/
```

### Smart Contract Tests

```bash
npx hardhat test
```

### Integration Test

```bash
# Make sure Hardhat node is running first
python tests/test_integration.py
```

---

## Verification Dashboard

The web dashboard provides a user-friendly interface for MRV verification.

### Features

- **Blockchain Connection**: Connect to local or remote Ethereum nodes
- **MRV Upload**: Upload MRV JSON files
- **Hash Verification**: Compare local hash with blockchain hash
- **Visual Status**: Clear VALID/TAMPERED/NOT FOUND indicators
- **Data Viewer**: Inspect MRV JSON data

### Usage

1. Start dashboard:
   ```bash
   cd dashboard
   python -m http.server 8080
   ```

2. Open http://localhost:8080

3. Connect to blockchain (if not auto-connected)

4. Enter MRV ID and upload JSON file

5. Click "Verify Integrity"

---

## API Reference

### MRVTracker

**Constructor Parameters:**

- `experiment_name` (str): Name of experiment **(required)**
- `model_name` (str): Model name (default: "Unknown")
- `dataset_name` (str): Dataset name (default: "Unknown")
- `epochs` (int): Number of epochs (optional)
- `batch_size` (int): Batch size (optional)
- `framework` (str): ML framework (default: "Unknown")
- `storage_dir` (str): Storage directory (default: "mrv_data")
- `registry_url` (str): Registry API URL (optional)
- `blockchain_enabled` (bool): Enable blockchain (default: True)
- `auto_anchor` (bool): Auto-anchor hash (default: True)

**Methods:**

- `start()`: Start tracking
- `stop()`: Stop tracking and save MRV
- `get_mrv_data()`: Get MRV JSON dict
- `get_hash()`: Get SHA-256 hash
- `verify_on_blockchain()`: Verify against blockchain

**Properties:**

- `mrv_id`: Generated MRV identifier
- `tx_hash`: Blockchain transaction hash
- `mrv_data`: Complete MRV dictionary

---

## Configuration

### Environment Variables

```bash
# Blockchain
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
CONTRACT_ADDRESS=0x...
PRIVATE_KEY=0x...

# Optional Registry
REGISTRY_URL=http://localhost:5000
```

### Network Configuration

For different networks, update `.env`:

**Local (Hardhat):**
```
BLOCKCHAIN_RPC_URL=http://127.0.0.1:8545
```

**Sepolia Testnet:**
```
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/YOUR-PROJECT-ID
```

---

## Troubleshooting

### "Not connected to blockchain"

- Ensure Hardhat node is running: `npx hardhat node`
- Check RPC URL in `.env`
- Verify contract address is correct

### "MRV ID not found"

- The MRV was not registered on blockchain
- Blockchain was not enabled during training
- Wrong network/contract address

### "Hash mismatch"

- The MRV JSON file was modified after registration
- Indicates data tampering

### CodeCarbon not tracking

- Ensure psutil and GPUtil are installed
- CodeCarbon requires proper permissions for hardware access

---

## Best Practices

1. **Always enable blockchain** for verifiable claims
2. **Include MRV ID** in your research papers
3. **Publish MRV JSON** alongside code/models
4. **Use testnet** for experiments before mainnet
5. **Keep private keys secure** (never commit to Git)

---

## Paper Integration

Include this in your methodology section:

> We tracked and verified our training emissions using blockchain-assisted MRV 
> (Measurement-Reporting-Verification). Our training consumed X kWh of energy 
> and produced Y kg CO₂ (MRV ID: MRV-abc123). The integrity of this data can be 
> independently verified using the MRV JSON file and the blockchain-anchored hash.

---

For more information, see the [main README](../README.md).

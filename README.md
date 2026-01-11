# Blockchain-Assisted MRV for Machine Learning Workloads

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Bringing transparency and trust to ML carbon reporting through blockchain-based verification**

## 🌍 Overview

Machine learning training workloads are increasingly energy-intensive. While tools exist to measure ML carbon emissions, current reporting methods are:
- ✗ Self-reported and unverifiable
- ✗ Locally stored in mutable files
- ✗ Not aligned with formal MRV principles

This project introduces a **Blockchain-Assisted MRV (Measurement-Reporting-Verification)** framework that enables:
- ✓ Automatic emission tracking during ML training
- ✓ Standardized MRV reporting format
- ✓ Immutable blockchain-based integrity verification
- ✓ Public auditability of sustainability claims

## 🏗️ Architecture

```
┌─────────────────┐
│  ML Researcher  │
└────────┬────────┘
         │ trains with wrapper
         ▼
┌─────────────────────────────────┐
│      MRV Wrapper (Python)       │
│  • CodeCarbon integration       │
│  • Auto-generates MRV JSON      │
│  • Computes SHA-256 hash        │
└────────┬────────────────────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
┌────────────┐  ┌──────────────┐  ┌──────────────┐
│ Local File │  │   Database   │  │  Blockchain  │
│   (.json)  │  │  (Registry)  │  │ (Hash Only)  │
└────────────┘  └──────────────┘  └──────┬───────┘
                                          │
                        ┌─────────────────┘
                        ▼
                ┌──────────────────┐
                │ Verification     │
                │ Dashboard        │
                │ VALID/TAMPERED   │
                └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for smart contracts)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/argha5/Blockchain-Assisted-MRV.git
cd Blockchain-Assisted-MRV

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Install the MRV wrapper package
pip install -e .
```

### Usage Example

```python
from mrv_wrapper import MRVTracker

# Wrap your training code
with MRVTracker(
    experiment_name="resnet18_cifar10",
    model_name="ResNet18",
    dataset_name="CIFAR-10"
) as tracker:
    # Your training code here
    model = create_model()
    train(model, epochs=90)

# MRV JSON generated, hash anchored on blockchain
print(f"MRV ID: {tracker.mrv_id}")
print(f"Blockchain TX: {tracker.tx_hash}")
```

### Verification

```bash
# Start the verification dashboard
cd dashboard
python -m http.server 8080

# Open http://localhost:8080
# Enter MRV ID or upload JSON to verify integrity
```

## 📊 MRV JSON Schema

The system automatically generates standardized MRV records:

```json
{
  "schema_version": "0.1",
  "mrv_id": "MRV-a3f2e9d4-b1c8-4567-89ab-cdef01234567",
  "experiment": {
    "experiment_name": "resnet18_cifar10_baseline",
    "model_name": "ResNet18",
    "dataset_name": "CIFAR-10"
  },
  "training": {
    "epochs": 90,
    "batch_size": 128,
    "framework": "PyTorch"
  },
  "hardware": {
    "gpu_type": "NVIDIA RTX 3090",
    "num_gpus": 1,
    "cpu_type": "Intel i7-12700H",
    "ram_gb": 32
  },
  "energy_emissions": {
    "measurement_tool": "CodeCarbon",
    "energy_kwh": 0.87,
    "co2_kg": 0.42,
    "duration_seconds": 5400
  },
  "timestamps": {
    "start_time": "2026-01-11T08:00:00Z",
    "end_time": "2026-01-11T09:30:00Z"
  }
}
```

## 🔐 How Verification Works

1. **Measurement**: Wrapper tracks emissions during training
2. **Recording**: MRV JSON generated with all metadata
3. **Anchoring**: SHA-256 hash stored on blockchain (immutable)
4. **Verification**: Anyone can verify: `sha256(JSON) == hash_on_chain(mrv_id)`

**Verification States:**
- ✅ **VALID** - Hash matches blockchain
- ❌ **TAMPERED** - Hash mismatch (data modified)
- ⚠️ **NOT FOUND** - MRV ID not registered

## 📁 Project Structure

```
blockchain-mrv-ml/
├── mrv_wrapper/          # Python package
│   ├── tracker.py        # Core tracking logic
│   ├── blockchain.py     # Web3 integration
│   ├── storage.py        # Data persistence
│   └── utils.py          # Utilities
├── contracts/            # Smart contracts
│   └── MRVRegistry.sol   # Solidity contract
├── dashboard/            # Verification UI
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── api/                  # REST API
│   ├── server.py
│   └── database.py
├── examples/             # Usage examples
│   ├── train_resnet.py
│   └── verify_mrv.py
├── tests/                # Test suite
└── docs/                 # Documentation
```

## 🧪 Running Tests

```bash
# Python tests
pytest tests/

# Smart contract tests
npx hardhat test

# Integration tests
python tests/test_integration.py
```

## 🌐 Deployment

### Local Testnet (Development)

```bash
# Start Hardhat node
npx hardhat node

# Deploy contract
npx hardhat run scripts/deploy.js --network localhost
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment.

## 📚 Documentation

- [Usage Guide](docs/USAGE.md) - Detailed usage instructions
- [API Reference](docs/API.md) - REST API documentation
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines first.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📖 Citation

If you use this system in your research, please cite:

```bibtex
@article{blockchain-mrv-ml-2026,
  title={Blockchain-Assisted MRV for Machine Learning Workloads},
  author={Your Name},
  journal={Conference/Journal Name},
  year={2026}
}
```

## 🙏 Acknowledgments

- [CodeCarbon](https://github.com/mlco2/codecarbon) for emission tracking
- [Hardhat](https://hardhat.org/) for Ethereum development environment
- The Green AI research community

---

**Built with 💚 for sustainable AI**

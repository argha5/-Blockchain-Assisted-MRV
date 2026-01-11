# Quick Start Guide

Get started with blockchain-assisted MRV for ML workloads in 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 16+
- Git

## Installation (2 minutes)

```bash
# Clone repository
git clone https://github.com/argha5/Blockchain-Assisted-MRV.git
cd Blockchain-Assisted-MRV

# Install Python dependencies
pip install -r requirements.txt
pip install -e .

# Install Node.js dependencies
npm install

# Setup environment
cp .env.example .env
```

## Run Example (3 minutes)

### Terminal 1: Start Blockchain

```bash
npx hardhat node
```

Keep this running!

### Terminal 2: Deploy Contract

```bash
npx hardhat run scripts/deploy.js --network localhost
```

Copy the contract address from output and update `.env`:
```
CONTRACT_ADDRESS=<paste-address-here>
```

### Terminal 3: Run Training Example

```bash
python examples/simple_example.py
```

You'll see:
```
🌱 Starting MRV tracking...
...
✅ MRV ID: MRV-abc123...
✅ Hash anchored on blockchain
```

### Terminal 4: Verify

```bash
cd dashboard
python -m http.server 8080
```

Open http://localhost:8080:
1. Connect to blockchain
2. Upload `mrv_data/MRV-*.json`
3. Enter the MRV ID
4. Click "Verify Integrity"
5. See ✅ VALID status!

## What Just Happened?

1. ✅ Your code was tracked for emissions (CodeCarbon)
2. ✅ MRV JSON generated with metadata
3. ✅ SHA-256 hash computed
4. ✅ Hash anchored on blockchain (immutable)
5. ✅ Anyone can now verify integrity

## Next Steps

- Read [USAGE.md](docs/USAGE.md) for detailed guide
- Try [train_resnet.py](examples/train_resnet.py) for full ML example
- Integrate MRV tracker into your own projects
- Include MRV IDs in your research papers!

---

**Questions?** See [README.md](README.md) or open an issue.

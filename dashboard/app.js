// MRV Verification Dashboard Application Logic

let web3;
let contract;
let currentAccount;
let mrvData = null;

// SHA-256 hash computation
async function computeSHA256(data) {
    // Must match Python's json.dumps(data, sort_keys=True, separators=(',', ':'))
    // This requires recursively sorting keys and using compact separators
    // Removed destructive replacements that corrupted string values

    // Sort keys recursively to match Python's sort_keys=True
    function sortKeysRecursively(obj) {
        if (obj === null || typeof obj !== 'object' || obj instanceof Array) {
            return obj;
        }
        const sorted = {};
        Object.keys(obj).sort().forEach(key => {
            sorted[key] = sortKeysRecursively(obj[key]);
        });
        return sorted;
    }

    const sortedData = sortKeysRecursively(data);
    let normalizedJson = JSON.stringify(sortedData);
    // Python preserves .0 for whole number floats, JavaScript doesn't
    // Replace to match Python's json.dumps behavior
    normalizedJson = normalizedJson.replace(/"co2_kg":0,/g, '"co2_kg":0.0,');

    const msgBuffer = new TextEncoder().encode(normalizedJson);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Connect to blockchain
async function connectBlockchain() {
    try {
        // Initialize Web3
        web3 = new Web3(CONFIG.RPC_URL);

        // Test connection
        const isConnected = await web3.eth.net.isListening();

        if (!isConnected) {
            showError("Failed to connect to blockchain. Is Hardhat node running?");
            return;
        }

        // Get accounts
        const accounts = await web3.eth.getAccounts();
        currentAccount = accounts[0];

        // Initialize contract
        contract = new web3.eth.Contract(CONFIG.CONTRACT_ABI, CONFIG.CONTRACT_ADDRESS);

        // Update UI
        updateConnectionStatus(true);
        console.log("✅ Connected to blockchain");
        console.log("Account:", currentAccount);

    } catch (error) {
        console.error("Connection error:", error);
        showError("Blockchain connection failed: " + error.message);
        updateConnectionStatus(false);
    }
}

// Update connection status UI
function updateConnectionStatus(connected) {
    const statusBar = document.getElementById('statusBar');
    const statusText = document.getElementById('statusText');
    const connectBtn = document.getElementById('connectBtn');

    if (connected) {
        statusBar.classList.add('connected');
        statusText.textContent = 'Connected to Blockchain';
        connectBtn.textContent = 'Connected ✓';
        connectBtn.disabled = true;
        connectBtn.style.opacity = '0.7';
    } else {
        statusBar.classList.remove('connected');
        statusText.textContent = 'Not Connected';
        connectBtn.textContent = 'Connect to Blockchain';
        connectBtn.disabled = false;
        connectBtn.style.opacity = '1';
    }
}

// Handle file upload
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        try {
            mrvData = JSON.parse(e.target.result);
            console.log("✅ MRV data loaded:", mrvData);

            // Auto-fill MRV ID if present
            if (mrvData.mrv_id) {
                document.getElementById('mrvId').value = mrvData.mrv_id;
            }

            // Show preview
            showDataViewer(mrvData);

        } catch (error) {
            showError("Invalid JSON file: " + error.message);
        }
    };
    reader.readAsText(file);
}

// Show MRV data viewer
function showDataViewer(data) {
    const viewer = document.getElementById('dataViewer');
    const display = document.getElementById('mrvDataDisplay');

    display.textContent = JSON.stringify(data, null, 2);
    viewer.style.display = 'block';
}

// Verify MRV
async function verifyMRV() {
    const mrvId = document.getElementById('mrvId').value.trim();

    if (!mrvId) {
        showError("Please enter an MRV ID");
        return;
    }

    if (!mrvData) {
        showError("Please upload MRV JSON file");
        return;
    }

    if (!web3 || !contract) {
        showError("Please connect to blockchain first");
        return;
    }

    try {
        console.log("🔍 Verifying MRV:", mrvId);

        // Compute hash of uploaded JSON
        const localHash = await computeSHA256(mrvData);
        console.log("Local hash:", localHash);

        // Check if MRV is registered
        const isRegistered = await contract.methods.isMRVRegistered(mrvId).call();

        if (!isRegistered) {
            showResult('not-found', mrvId, null, null);
            return;
        }

        // Get blockchain record
        const record = await contract.methods.getMRVRecord(mrvId).call();
        const blockchainHash = record.hash.replace('0x', '');
        const timestamp = record.timestamp;
        const submitter = record.submitter;

        console.log("Blockchain hash:", blockchainHash);
        console.log("Timestamp:", new Date(Number(timestamp) * 1000).toISOString());
        console.log("Submitter:", submitter);

        // Verify hash
        const isValid = localHash === blockchainHash;

        if (isValid) {
            showResult('valid', mrvId, record, localHash);
        } else {
            showResult('tampered', mrvId, record, localHash);
        }

    } catch (error) {
        console.error("Verification error:", error);
        showError("Verification failed: " + error.message);
    }
}

// Show verification result
function showResult(status, mrvId, record, localHash) {
    const resultCard = document.getElementById('resultCard');
    const resultHeader = document.getElementById('resultHeader');
    const resultDetails = document.getElementById('resultDetails');

    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Clear previous classes
    resultHeader.className = `result-header ${status}`;

    // Set header content
    const statusIcons = {
        'valid': '✅',
        'tampered': '❌',
        'not-found': '⚠️'
    };

    const statusTexts = {
        'valid': 'VALID - Data Integrity Verified',
        'tampered': 'TAMPERED - Hash Mismatch Detected',
        'not-found': 'NOT FOUND - MRV ID Not Registered'
    };

    resultHeader.innerHTML = `
        <span style="font-size: 2rem;">${statusIcons[status]}</span>
        <span>${statusTexts[status]}</span>
    `;

    // Set details content
    if (status === 'not-found') {
        resultDetails.innerHTML = `
            <div class="result-row">
                <span class="result-label">MRV ID:</span>
                <span class="result-value">${mrvId}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Status:</span>
                <span class="result-value">Not registered on blockchain</span>
            </div>
        `;
    } else {
        const date = new Date(Number(record.timestamp) * 1000);
        const isValid = status === 'valid';

        resultDetails.innerHTML = `
            <div class="result-row">
                <span class="result-label">MRV ID:</span>
                <span class="result-value">${mrvId}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Blockchain Hash:</span>
                <span class="result-value">${record.hash.replace('0x', '')}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Computed Hash:</span>
                <span class="result-value">${localHash}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Registration Time:</span>
                <span class="result-value">${date.toLocaleString()}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Submitter:</span>
                <span class="result-value">${record.submitter}</span>
            </div>
            <div class="result-row">
                <span class="result-label">Match:</span>
                <span class="result-value" style="color: ${isValid ? 'var(--success)' : 'var(--error)'}">
                    ${isValid ? '✓ Hashes Match' : '✗ Hashes Do Not Match'}
                </span>
            </div>
        `;
    }
}

// Show error message
function showError(message) {
    alert('❌ Error: ' + message);
}

// Auto-connect on page load
window.addEventListener('load', async () => {
    console.log("🌱 MRV Verification Dashboard loaded");
    // Auto-connect if RPC is available
    try {
        await connectBlockchain();
    } catch (error) {
        console.log("Auto-connect failed, waiting for manual connection");
    }
});

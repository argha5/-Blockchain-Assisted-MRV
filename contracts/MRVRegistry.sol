// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title MRVRegistry
 * @dev Blockchain-based registry for MRV (Measurement-Reporting-Verification) records
 * @notice This contract stores cryptographic hashes of ML training emission reports
 * 
 * Key Features:
 * - Immutable hash storage (no overwrites allowed)
 * - Timestamp recording for audit trails
 * - Public verification interface
 * - Event logging for transparency
 */
contract MRVRegistry {
    
    // MRV Record structure
    struct MRVRecord {
        bytes32 hash;           // SHA-256 hash of MRV JSON
        uint256 timestamp;      // Block timestamp of registration
        address submitter;      // Address that submitted the MRV
        bool exists;            // Flag to check if record exists
    }
    
    // Mapping: MRV ID (string) → MRV Record
    mapping(string => MRVRecord) private mrvRecords;
    
    // Events
    event MRVRegistered(
        string indexed mrvId,
        bytes32 hash,
        uint256 timestamp,
        address indexed submitter
    );
    
    event MRVQueried(
        string indexed mrvId,
        address indexed querier
    );
    
    /**
     * @dev Register a new MRV record
     * @param mrvId Unique MRV identifier (e.g., "MRV-uuid")
     * @param hash SHA-256 hash of the MRV JSON data
     * 
     * Requirements:
     * - MRV ID must not already be registered (immutability)
     * - Hash must not be zero
     */
    function registerMRV(string memory mrvId, bytes32 hash) external {
        require(!mrvRecords[mrvId].exists, "MRV ID already registered");
        require(hash != bytes32(0), "Hash cannot be zero");
        
        // Store MRV record
        mrvRecords[mrvId] = MRVRecord({
            hash: hash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            exists: true
        });
        
        // Emit event
        emit MRVRegistered(mrvId, hash, block.timestamp, msg.sender);
    }
    
    /**
     * @dev Get MRV record details
     * @param mrvId MRV identifier to query
     * @return hash SHA-256 hash of the MRV data
     * @return timestamp Registration timestamp
     * @return submitter Address that registered the MRV
     */
    function getMRVHash(string memory mrvId) 
        external 
        returns (bytes32 hash, uint256 timestamp, address submitter) 
    {
        MRVRecord memory record = mrvRecords[mrvId];
        
        // Emit query event for analytics
        emit MRVQueried(mrvId, msg.sender);
        
        return (record.hash, record.timestamp, record.submitter);
    }
    
    /**
     * @dev Check if MRV ID is registered
     * @param mrvId MRV identifier to check
     * @return exists True if registered, false otherwise
     */
    function isMRVRegistered(string memory mrvId) external view returns (bool) {
        return mrvRecords[mrvId].exists;
    }
    
    /**
     * @dev Verify MRV hash matches blockchain record
     * @param mrvId MRV identifier
     * @param expectedHash Expected SHA-256 hash
     * @return valid True if hash matches, false otherwise
     */
    function verifyMRVHash(string memory mrvId, bytes32 expectedHash) 
        external 
        view 
        returns (bool valid) 
    {
        if (!mrvRecords[mrvId].exists) {
            return false;
        }
        
        return mrvRecords[mrvId].hash == expectedHash;
    }
    
    /**
     * @dev Get full MRV record (view-only for gas efficiency)
     * @param mrvId MRV identifier
     * @return record Complete MRV record struct
     */
    function getMRVRecord(string memory mrvId) 
        external 
        view 
        returns (MRVRecord memory record) 
    {
        return mrvRecords[mrvId];
    }
}

const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MRVRegistry", function () {
    let mrvRegistry;
    let owner;
    let addr1;
    let addr2;

    beforeEach(async function () {
        // Get signers
        [owner, addr1, addr2] = await ethers.getSigners();

        // Deploy contract
        const MRVRegistry = await ethers.getContractFactory("MRVRegistry");
        mrvRegistry = await MRVRegistry.deploy();
        await mrvRegistry.waitForDeployment();
    });

    describe("Registration", function () {
        it("Should register a new MRV record", async function () {
            const mrvId = "MRV-test-001";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            await expect(mrvRegistry.registerMRV(mrvId, hash))
                .to.emit(mrvRegistry, "MRVRegistered")
                .withArgs(mrvId, hash, await ethers.provider.getBlock('latest').then(b => b.timestamp + 1), owner.address);

            const isRegistered = await mrvRegistry.isMRVRegistered(mrvId);
            expect(isRegistered).to.be.true;
        });

        it("Should prevent duplicate MRV ID registration", async function () {
            const mrvId = "MRV-test-002";
            const hash1 = ethers.keccak256(ethers.toUtf8Bytes("data1"));
            const hash2 = ethers.keccak256(ethers.toUtf8Bytes("data2"));

            // First registration should succeed
            await mrvRegistry.registerMRV(mrvId, hash1);

            // Second registration should fail
            await expect(
                mrvRegistry.registerMRV(mrvId, hash2)
            ).to.be.revertedWith("MRV ID already registered");
        });

        it("Should reject zero hash", async function () {
            const mrvId = "MRV-test-003";
            const zeroHash = ethers.ZeroHash;

            await expect(
                mrvRegistry.registerMRV(mrvId, zeroHash)
            ).to.be.revertedWith("Hash cannot be zero");
        });
    });

    describe("Retrieval", function () {
        it("Should retrieve MRV hash correctly", async function () {
            const mrvId = "MRV-test-004";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            await mrvRegistry.registerMRV(mrvId, hash);

            const [retrievedHash, timestamp, submitter] = await mrvRegistry.getMRVHash(mrvId);

            expect(retrievedHash).to.equal(hash);
            expect(submitter).to.equal(owner.address);
            expect(timestamp).to.be.greaterThan(0);
        });

        it("Should return zero values for non-existent MRV ID", async function () {
            const mrvId = "MRV-nonexistent";

            const [hash, timestamp, submitter] = await mrvRegistry.getMRVHash(mrvId);

            expect(hash).to.equal(ethers.ZeroHash);
            expect(timestamp).to.equal(0);
            expect(submitter).to.equal(ethers.ZeroAddress);
        });

        it("Should correctly check MRV registration status", async function () {
            const mrvId = "MRV-test-005";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            // Check before registration
            expect(await mrvRegistry.isMRVRegistered(mrvId)).to.be.false;

            // Register
            await mrvRegistry.registerMRV(mrvId, hash);

            // Check after registration
            expect(await mrvRegistry.isMRVRegistered(mrvId)).to.be.true;
        });
    });

    describe("Verification", function () {
        it("Should verify correct hash", async function () {
            const mrvId = "MRV-test-006";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            await mrvRegistry.registerMRV(mrvId, hash);

            const isValid = await mrvRegistry.verifyMRVHash(mrvId, hash);
            expect(isValid).to.be.true;
        });

        it("Should reject incorrect hash", async function () {
            const mrvId = "MRV-test-007";
            const correctHash = ethers.keccak256(ethers.toUtf8Bytes("correct data"));
            const incorrectHash = ethers.keccak256(ethers.toUtf8Bytes("incorrect data"));

            await mrvRegistry.registerMRV(mrvId, correctHash);

            const isValid = await mrvRegistry.verifyMRVHash(mrvId, incorrectHash);
            expect(isValid).to.be.false;
        });

        it("Should return false for non-existent MRV ID", async function () {
            const mrvId = "MRV-nonexistent";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            const isValid = await mrvRegistry.verifyMRVHash(mrvId, hash);
            expect(isValid).to.be.false;
        });
    });

    describe("Get Full Record", function () {
        it("Should retrieve full MRV record", async function () {
            const mrvId = "MRV-test-008";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            await mrvRegistry.registerMRV(mrvId, hash);

            const record = await mrvRegistry.getMRVRecord(mrvId);

            expect(record.hash).to.equal(hash);
            expect(record.submitter).to.equal(owner.address);
            expect(record.timestamp).to.be.greaterThan(0);
            expect(record.exists).to.be.true;
        });
    });

    describe("Events", function () {
        it("Should emit MRVQueried event on hash retrieval", async function () {
            const mrvId = "MRV-test-009";
            const hash = ethers.keccak256(ethers.toUtf8Bytes("test data"));

            await mrvRegistry.registerMRV(mrvId, hash);

            await expect(mrvRegistry.connect(addr1).getMRVHash(mrvId))
                .to.emit(mrvRegistry, "MRVQueried")
                .withArgs(mrvId, addr1.address);
        });
    });
});

"""
Core MRV tracking module.
"""

import time
from typing import Optional, Dict, Any
from codecarbon import EmissionsTracker

from .utils import (
    compute_hash,
    get_current_timestamp,
    get_hardware_info,
    format_duration
)
from .storage import MRVStorage, save_to_registry
from .blockchain import BlockchainConnector


class MRVTracker:
    """
    Main MRV tracker for ML training workloads.
    
    Usage:
        with MRVTracker(experiment_name="my_experiment") as tracker:
            # Your training code here
            train_model()
        
        print(f"MRV ID: {tracker.mrv_id}")
    """
    
    def __init__(
        self,
        experiment_name: str,
        model_name: Optional[str] = None,
        dataset_name: Optional[str] = None,
        epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        framework: Optional[str] = None,
        storage_dir: str = "mrv_data",
        registry_url: Optional[str] = None,
        blockchain_enabled: bool = True,
        auto_anchor: bool = True
    ):
        """
        Initialize MRV tracker.
        
        Args:
            experiment_name: Name of the experiment
            model_name: Name of the model (optional)
            dataset_name: Name of the dataset (optional)
            epochs: Number of training epochs (optional)
            batch_size: Training batch size (optional)
            framework: ML framework used (optional, e.g., "PyTorch", "TensorFlow")
            storage_dir: Directory for MRV data storage
            registry_url: URL of centralized registry API (optional)
            blockchain_enabled: Enable blockchain anchoring
            auto_anchor: Automatically anchor hash on blockchain after training
        """
        self.experiment_name = experiment_name
        self.model_name = model_name or "Unknown"
        self.dataset_name = dataset_name or "Unknown"
        self.epochs = epochs
        self.batch_size = batch_size
        self.framework = framework or "Unknown"
        
        self.storage_dir = storage_dir
        self.registry_url = registry_url
        self.blockchain_enabled = blockchain_enabled
        self.auto_anchor = auto_anchor
        
        # Initialize components
        self.storage = MRVStorage(storage_dir=storage_dir)
        self.blockchain = BlockchainConnector() if blockchain_enabled else None
        self.emissions_tracker = None
        
        # State variables
        self.mrv_id = None
        self.tx_hash = None
        self.mrv_data = None
        self.start_time = None
        self.end_time = None
        self.emissions_data = None
    
    def __enter__(self):
        """Start tracking when entering context."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop tracking and save MRV data when exiting context."""
        self.stop()
        return False
    
    def start(self):
        """Start emission tracking."""
        print("🌱 Starting MRV tracking...")
        
        self.start_time = get_current_timestamp()
        
        # Start CodeCarbon tracker
        self.emissions_tracker = EmissionsTracker(
            project_name=self.experiment_name,
            measure_power_secs=15,  # Measure every 15 seconds
            save_to_file=False,  # We'll save to our own MRV format
            logging_logger=None  # Suppress CodeCarbon logs
        )
        self.emissions_tracker.start()
        
        print(f"📊 Tracking experiment: {self.experiment_name}")
    
    def stop(self):
        """Stop emission tracking and generate MRV record."""
        if self.emissions_tracker is None:
            print("⚠️  Warning: Tracker not started")
            return
        
        print("📊 Stopping MRV tracking...")
        
        # Stop emissions tracker
        emissions = self.emissions_tracker.stop()
        self.end_time = get_current_timestamp()
        
        # Store emissions data
        self.emissions_data = {
            "energy_kwh": round(emissions, 6) if emissions else 0.0,
            "co2_kg": 0.0,  # CodeCarbon returns combined value
            "duration_seconds": self._calculate_duration()
        }
        
        # Note: CodeCarbon's stop() returns emissions in kWh
        # For more accurate CO2, we'd need to access tracker.final_emissions_data
        # For now, using simplified approach
        
        # Generate MRV record
        self._generate_mrv_record()
        
        # Save locally
        self.mrv_id = self.storage.save_mrv(self.mrv_data)
        
        # Save to registry (optional)
        if self.registry_url:
            save_to_registry(self.mrv_data, self.registry_url)
        
        # Anchor hash on blockchain
        if self.blockchain_enabled and self.auto_anchor and self.blockchain:
            mrv_hash = compute_hash(self.mrv_data)
            self.tx_hash = self.blockchain.anchor_hash(self.mrv_id, mrv_hash)
        
        # Print summary
        self._print_summary()
    
    def _calculate_duration(self) -> int:
        """Calculate training duration in seconds."""
        if self.start_time and self.end_time:
            from datetime import datetime
            start = datetime.fromisoformat(self.start_time)
            end = datetime.fromisoformat(self.end_time)
            return int((end - start).total_seconds())
        return 0
    
    def _generate_mrv_record(self):
        """Generate MRV JSON record."""
        hardware_info = get_hardware_info()
        
        self.mrv_data = {
            "schema_version": "0.1",
            "mrv_id": self.storage.generate_mrv_id(),
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
            "hardware": {
                "gpu_type": hardware_info["gpu_type"],
                "num_gpus": hardware_info["num_gpus"],
                "cpu_type": hardware_info["cpu_type"],
                "ram_gb": hardware_info["ram_gb"]
            },
            "energy_emissions": {
                "measurement_tool": "CodeCarbon",
                "energy_kwh": self.emissions_data["energy_kwh"],
                "co2_kg": self.emissions_data["co2_kg"],
                "duration_seconds": self.emissions_data["duration_seconds"]
            },
            "timestamps": {
                "start_time": self.start_time,
                "end_time": self.end_time
            }
        }
    
    def _print_summary(self):
        """Print tracking summary."""
        print("\n" + "="*60)
        print("🌱 MRV TRACKING SUMMARY")
        print("="*60)
        print(f"Experiment:     {self.experiment_name}")
        print(f"Model:          {self.model_name}")
        print(f"Dataset:        {self.dataset_name}")
        print(f"Duration:       {format_duration(self.emissions_data['duration_seconds'])}")
        print(f"Energy:         {self.emissions_data['energy_kwh']:.6f} kWh")
        print(f"CO₂:            {self.emissions_data['co2_kg']:.6f} kg")
        print(f"\nMRV ID:         {self.mrv_id}")
        
        if self.tx_hash:
            print(f"Blockchain TX:  {self.tx_hash[:10]}...{self.tx_hash[-6:]}")
        
        print("="*60 + "\n")
    
    def get_mrv_data(self) -> Optional[Dict[str, Any]]:
        """
        Get generated MRV data.
        
        Returns:
            MRV JSON dictionary or None if not yet generated
        """
        return self.mrv_data
    
    def get_hash(self) -> Optional[str]:
        """
        Get SHA-256 hash of MRV data.
        
        Returns:
            Hash string or None if data not yet generated
        """
        if self.mrv_data:
            return compute_hash(self.mrv_data)
        return None
    
    def verify_on_blockchain(self) -> bool:
        """
        Verify MRV data against blockchain.
        
        Returns:
            True if hash matches blockchain record
        """
        if not self.blockchain or not self.mrv_data or not self.mrv_id:
            return False
        
        expected_hash = compute_hash(self.mrv_data)
        return self.blockchain.verify_hash(self.mrv_id, expected_hash)

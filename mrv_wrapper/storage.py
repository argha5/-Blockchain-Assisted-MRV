"""
Storage module for MRV data persistence.
"""

import json
import os
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class MRVStorage:
    """Handles storage and retrieval of MRV records."""
    
    def __init__(self, storage_dir: str = "mrv_data"):
        """
        Initialize MRV storage.
        
        Args:
            storage_dir: Directory to store MRV JSON files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
    
    def generate_mrv_id(self) -> str:
        """
        Generate unique MRV ID.
        
        Returns:
            MRV ID in format: MRV-{uuid}
        """
        return f"MRV-{uuid.uuid4()}"
    
    def save_mrv(self, mrv_data: Dict[str, Any], mrv_id: Optional[str] = None) -> str:
        """
        Save MRV data to local file.
        
        Args:
            mrv_data: MRV JSON dictionary
            mrv_id: Optional MRV ID (generated if not provided)
            
        Returns:
            MRV ID
        """
        if mrv_id is None:
            mrv_id = mrv_data.get("mrv_id") or self.generate_mrv_id()
        
        # Save to file
        filename = f"{mrv_id}.json"
        filepath = self.storage_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(mrv_data, f, indent=2, sort_keys=True)
        
        print(f"✅ MRV data saved: {filepath}")
        return mrv_id
    
    def load_mrv(self, mrv_id: str) -> Optional[Dict[str, Any]]:
        """
        Load MRV data from local file.
        
        Args:
            mrv_id: MRV ID
            
        Returns:
            MRV JSON dictionary or None if not found
        """
        filename = f"{mrv_id}.json"
        filepath = self.storage_dir / filename
        
        if not filepath.exists():
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_mrv_records(self) -> list:
        """
        List all MRV records in storage.
        
        Returns:
            List of MRV IDs
        """
        return [
            f.stem for f in self.storage_dir.glob("MRV-*.json")
        ]
    
    def export_mrv(self, mrv_id: str, output_path: str) -> bool:
        """
        Export MRV data to specific path.
        
        Args:
            mrv_id: MRV ID
            output_path: Target file path
            
        Returns:
            True if successful
        """
        mrv_data = self.load_mrv(mrv_id)
        if mrv_data is None:
            return False
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mrv_data, f, indent=2, sort_keys=True)
        
        return True


def save_to_registry(mrv_data: Dict[str, Any], registry_url: Optional[str] = None) -> bool:
    """
    Save MRV data to centralized registry (optional).
    
    Args:
        mrv_data: MRV JSON dictionary
        registry_url: URL of registry API (if None, skip)
        
    Returns:
        True if successful
    """
    if registry_url is None:
        # Skip registry upload if no URL provided
        return True
    
    try:
        import requests
        response = requests.post(
            f"{registry_url}/api/mrv",
            json=mrv_data,
            timeout=10
        )
        return response.status_code == 201
    except Exception as e:
        print(f"⚠️  Warning: Failed to save to registry: {e}")
        return False

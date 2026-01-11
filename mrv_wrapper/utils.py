"""
Utility functions for MRV wrapper.
"""

import hashlib
import json
import platform
import psutil
from datetime import datetime, timezone
from typing import Dict, Any, Optional

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


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
    return hashlib.sha256(json_str.encode('utf-8')).hexdigest()


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO 8601 format (UTC).
    
    Returns:
        ISO 8601 formatted timestamp
    """
    return datetime.now(timezone.utc).isoformat()


def get_cpu_info() -> Dict[str, Any]:
    """
    Get CPU information.
    
    Returns:
        Dictionary with CPU type and core count
    """
    return {
        "cpu_type": platform.processor() or "Unknown",
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True)
    }


def get_gpu_info() -> Dict[str, Any]:
    """
    Get GPU information.
    
    Returns:
        Dictionary with GPU type and count
    """
    if not GPU_AVAILABLE:
        return {
            "gpu_type": "None",
            "num_gpus": 0,
            "gpu_memory_gb": 0
        }
    
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            return {
                "gpu_type": "None",
                "num_gpus": 0,
                "gpu_memory_gb": 0
            }
        
        # Use first GPU for info
        gpu = gpus[0]
        return {
            "gpu_type": gpu.name,
            "num_gpus": len(gpus),
            "gpu_memory_gb": round(gpu.memoryTotal / 1024, 2)
        }
    except Exception:
        return {
            "gpu_type": "Unknown",
            "num_gpus": 0,
            "gpu_memory_gb": 0
        }


def get_ram_info() -> int:
    """
    Get total RAM in GB.
    
    Returns:
        Total RAM in GB (rounded)
    """
    return round(psutil.virtual_memory().total / (1024**3))


def get_hardware_info() -> Dict[str, Any]:
    """
    Collect all hardware information.
    
    Returns:
        Dictionary with CPU, GPU, and RAM information
    """
    cpu_info = get_cpu_info()
    gpu_info = get_gpu_info()
    
    return {
        "cpu_type": cpu_info["cpu_type"],
        "cpu_cores": cpu_info["cpu_cores"],
        "gpu_type": gpu_info["gpu_type"],
        "num_gpus": gpu_info["num_gpus"],
        "ram_gb": get_ram_info(),
        "gpu_memory_gb": gpu_info.get("gpu_memory_gb", 0)
    }


def validate_mrv_json(data: Dict[str, Any]) -> bool:
    """
    Validate MRV JSON schema.
    
    Args:
        data: MRV JSON dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "schema_version",
        "mrv_id",
        "experiment",
        "training",
        "hardware",
        "energy_emissions",
        "timestamps"
    ]
    
    # Check top-level fields
    for field in required_fields:
        if field not in data:
            return False
    
    # Check nested fields
    if "experiment_name" not in data["experiment"]:
        return False
    if "energy_kwh" not in data["energy_emissions"]:
        return False
    if "start_time" not in data["timestamps"]:
        return False
    
    return True


def format_duration(seconds: float) -> str:
    """
    Format duration in human-readable format.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted string (e.g., "1h 30m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)

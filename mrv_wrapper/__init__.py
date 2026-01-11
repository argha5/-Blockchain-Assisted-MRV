"""
MRV Wrapper - Blockchain-Assisted MRV for Machine Learning Workloads

This package provides automatic emission tracking, standardized MRV reporting,
and blockchain-based integrity verification for ML training workloads.
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .tracker import MRVTracker
from .utils import compute_hash, validate_mrv_json

__all__ = ["MRVTracker", "compute_hash", "validate_mrv_json"]

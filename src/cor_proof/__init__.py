"""
COR Proof — Chain-of-Reasoning Proof
Open Standard — Level 1 (Universal Structure Layer)

Python reference implementation for structural validation of COR Proof L1 artifacts.

This package validates structure only. It does not verify truth, factual accuracy,
safety, compliance, or model quality.

Maintained by OmnySync Group LLC as part of the Stake The Truth initiative.
https://github.com/OmnySync-Group/cor-proof
"""

__version__ = "0.1.0"
__author__ = "OmnySync Group LLC"
__license__ = "Apache-2.0"

from cor_proof.schema import load_schema
from cor_proof.validate import validate, ValidationResult

__all__ = [
    "__version__",
    "load_schema",
    "validate",
    "ValidationResult",
]

"""arya-contracts — authorize contract types for ARYA Labs safety kernel.

Exports 5 types extracted from QantmOrchstrtr-RSI (ARY-1882):
- NanoImplKind, NanoArtifactSpec, NanoDecisionSpec (from packages/core/nano.py)
- KernelPolicyDecision, KernelDenyReason (from apps/safety_kernel/policy.py)

Zero non-stdlib dependencies. Python 3.11+.
"""

from arya_contracts._policy import KernelDenyReason, KernelPolicyDecision
from arya_contracts._specs import NanoArtifactSpec, NanoDecisionSpec, NanoImplKind

__version__ = "0.1.0"
__all__ = [
    "NanoArtifactSpec",
    "NanoDecisionSpec",
    "NanoImplKind",
    "KernelPolicyDecision",
    "KernelDenyReason",
]

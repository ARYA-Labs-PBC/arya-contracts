"""Safety kernel policy decision types — extracted from apps/safety_kernel/policy.py (ARY-1882).

These types define the contract surface for authorization decisions in the ARYA Labs
Safety Kernel. Zero non-stdlib dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class KernelDenyReason(str, Enum):
    """Canonical reason codes returned by the Safety Kernel policy engine.

    These values correspond to the ``reason`` field on ``KernelPolicyDecision``
    as emitted by ``apps/safety_kernel/policy.py::decide_authorization``.
    """

    # ---- production default-deny ----
    PROD_REQUIRES_ALLOW_SUBJECTS = "prod_requires_allow_subjects"
    PROD_REQUIRES_ALLOW_ACTIONS = "prod_requires_allow_actions"

    # ---- subject checks ----
    SUBJECT_DENYLIST = "subject_denylist"
    SUBJECT_NOT_IN_ALLOWLIST = "subject_not_in_allowlist"

    # ---- action checks ----
    ACTION_DENYLIST = "action_denylist"
    ACTION_NOT_IN_ALLOWLIST = "action_not_in_allowlist"

    # ---- artifact / promotion checks ----
    ARTIFACT_REQUIRES_PRIVILEGED_CALLER = "artifact_requires_privileged_caller"
    MISSING_ARTIFACT_KIND = "missing_artifact_kind"
    ARTIFACT_KIND_NOT_PROMOTABLE = "artifact_kind_not_promotable"

    # ---- code modification checks ----
    CODE_MODIFICATION_REQUIRES_SIO = "code_modification_requires_sio"
    CODE_MODIFICATION_IMMUTABLE_MODULE = "code_modification_immutable_module"
    CODE_MODIFICATION_IMMUTABLE_FUNCTION = "code_modification_immutable_function"
    CODE_MODIFICATION_MISSING_VERIFICATION = "code_modification_missing_verification"
    CODE_MODIFICATION_VERIFICATION_FAILED = "code_modification_verification_failed"
    CODE_MODIFICATION_REQUIRES_OPERATOR_ATTESTATION = (
        "code_modification_requires_operator_attestation"
    )

    # ---- evolutionary operation checks ----
    EVOLUTIONARY_OPERATION_REQUIRES_AUTHORIZED_SUBJECT = (
        "evolutionary_operation_requires_authorized_subject"
    )
    EVOLUTIONARY_OPERATION_MISSING_TARGET_MODULE = (
        "evolutionary_operation_missing_target_module"
    )
    EVOLUTIONARY_TARGET_OUTSIDE_SEARCH_SPACE = "evolutionary_target_outside_search_space"
    EVOLUTIONARY_CODE_MATCHES_DENIED_PATTERN = "evolutionary_code_matches_denied_pattern"
    EVOLUTIONARY_TARGET_IMMUTABLE_MODULE = "evolutionary_target_immutable_module"
    EVOLUTIONARY_TARGET_IMMUTABLE_FUNCTION = "evolutionary_target_immutable_function"
    EVOLUTIONARY_REQUIRES_OPERATOR_ATTESTATION = (
        "evolutionary_requires_operator_attestation"
    )
    EVOLUTIONARY_INVALID_VERIFICATION_FORMAT = "evolutionary_invalid_verification_format"
    EVOLUTIONARY_VERIFICATION_FAILED = "evolutionary_verification_failed"
    EVOLUTIONARY_ALLOWED = "evolutionary_allowed"

    # ---- self-improvement checks ----
    SELF_IMPROVEMENT_REQUIRES_AUTHORIZED_SUBJECT = (
        "self_improvement_requires_authorized_subject"
    )
    SELF_IMPROVEMENT_SAFETY_CRITICAL_REQUIRES_ATTESTATION = (
        "self_improvement_safety_critical_requires_attestation"
    )
    SELF_IMPROVEMENT_REQUIRES_OPERATOR_ATTESTATION = (
        "self_improvement_requires_operator_attestation"
    )
    SELF_IMPROVEMENT_INVALID_SAFETY_INVARIANTS = (
        "self_improvement_invalid_safety_invariants"
    )
    SELF_IMPROVEMENT_SAFETY_INVARIANTS_FAILED = "self_improvement_safety_invariants_failed"
    SELF_IMPROVEMENT_ALLOWED = "self_improvement_allowed"

    # ---- generic allow ----
    ALLOWED = "allowed"


@dataclass(frozen=True, slots=True)
class KernelPolicyDecision:
    """Result of a kernel policy authorization decision.

    Copied verbatim from apps/safety_kernel/policy.py (ARY-1882).
    """

    allowed: bool
    reason: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        """Convert decision to dictionary for serialization."""
        return {
            "allowed": bool(self.allowed),
            "reason": str(self.reason),
            "metadata": dict(self.metadata),
        }

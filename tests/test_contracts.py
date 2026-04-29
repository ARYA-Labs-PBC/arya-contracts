"""Tests for arya-contracts package — ARY-1882.

Verifies all 5 exported types are importable and have expected fields/values.
"""

from __future__ import annotations

import dataclasses

import pytest

from arya_contracts import (
    KernelDenyReason,
    KernelPolicyDecision,
    NanoArtifactSpec,
    NanoDecisionSpec,
    NanoImplKind,
)
from arya_contracts import __version__


# ---------------------------------------------------------------------------
# Package smoke test
# ---------------------------------------------------------------------------


def test_version() -> None:
    assert __version__ == "0.1.0"


# ---------------------------------------------------------------------------
# NanoImplKind
# ---------------------------------------------------------------------------


def test_nano_impl_kind_values() -> None:
    assert NanoImplKind.RULES == "rules"
    assert NanoImplKind.FORMULA == "formula"
    assert NanoImplKind.LINEAR == "linear"
    assert NanoImplKind.TABULAR == "tabular"
    assert NanoImplKind.TINY_NN == "tiny_nn"


def test_nano_impl_kind_is_str_enum() -> None:
    assert isinstance(NanoImplKind.RULES, str)


def test_nano_impl_kind_all_members() -> None:
    members = {m.value for m in NanoImplKind}
    assert members == {"rules", "formula", "linear", "tabular", "tiny_nn"}


# ---------------------------------------------------------------------------
# NanoArtifactSpec
# ---------------------------------------------------------------------------


def test_nano_artifact_spec_fields() -> None:
    spec = NanoArtifactSpec(kind="rules", size_budget_bytes=1024)
    assert spec.kind == "rules"
    assert spec.size_budget_bytes == 1024
    assert spec.deterministic is True
    assert spec.notes is None


def test_nano_artifact_spec_optional_fields() -> None:
    spec = NanoArtifactSpec(
        kind="tiny_nn", size_budget_bytes=8192, deterministic=False, notes="experimental"
    )
    assert spec.deterministic is False
    assert spec.notes == "experimental"


def test_nano_artifact_spec_is_frozen() -> None:
    spec = NanoArtifactSpec(kind="rules", size_budget_bytes=512)
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        spec.kind = "formula"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# NanoDecisionSpec
# ---------------------------------------------------------------------------


def test_nano_decision_spec_fields() -> None:
    nano = NanoArtifactSpec(kind="rules", size_budget_bytes=512)
    fallback = NanoArtifactSpec(kind="formula", size_budget_bytes=256)
    spec = NanoDecisionSpec(capability="risk_score", nano_impl=nano, fallback_impl=fallback)
    assert spec.capability == "risk_score"
    assert spec.nano_impl is nano
    assert spec.fallback_impl is fallback
    assert spec.safety_critical is True


def test_nano_decision_spec_safety_critical_override() -> None:
    nano = NanoArtifactSpec(kind="tabular", size_budget_bytes=1024)
    fallback = NanoArtifactSpec(kind="rules", size_budget_bytes=256)
    spec = NanoDecisionSpec(
        capability="latency_predictor",
        nano_impl=nano,
        fallback_impl=fallback,
        safety_critical=False,
    )
    assert spec.safety_critical is False


def test_nano_decision_spec_is_frozen() -> None:
    nano = NanoArtifactSpec(kind="rules", size_budget_bytes=512)
    fallback = NanoArtifactSpec(kind="formula", size_budget_bytes=256)
    spec = NanoDecisionSpec(capability="x", nano_impl=nano, fallback_impl=fallback)
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        spec.capability = "y"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# KernelPolicyDecision
# ---------------------------------------------------------------------------


def test_kernel_policy_decision_allowed() -> None:
    d = KernelPolicyDecision(allowed=True, reason="allowed", metadata={"ts": 1.0})
    assert d.allowed is True
    assert d.reason == "allowed"
    assert d.metadata["ts"] == 1.0


def test_kernel_policy_decision_denied() -> None:
    d = KernelPolicyDecision(allowed=False, reason="subject_denylist", metadata={})
    assert d.allowed is False


def test_kernel_policy_decision_to_dict() -> None:
    d = KernelPolicyDecision(allowed=True, reason="allowed", metadata={"x": 1})
    result = d.to_dict()
    assert result == {"allowed": True, "reason": "allowed", "metadata": {"x": 1}}


def test_kernel_policy_decision_is_frozen() -> None:
    d = KernelPolicyDecision(allowed=True, reason="allowed", metadata={})
    with pytest.raises((dataclasses.FrozenInstanceError, AttributeError)):
        d.allowed = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# KernelDenyReason
# ---------------------------------------------------------------------------


def test_kernel_deny_reason_is_str_enum() -> None:
    assert isinstance(KernelDenyReason.ALLOWED, str)
    assert KernelDenyReason.ALLOWED == "allowed"


def test_kernel_deny_reason_key_values() -> None:
    assert KernelDenyReason.SUBJECT_DENYLIST == "subject_denylist"
    assert KernelDenyReason.ACTION_DENYLIST == "action_denylist"
    assert KernelDenyReason.CODE_MODIFICATION_IMMUTABLE_MODULE == (
        "code_modification_immutable_module"
    )
    assert KernelDenyReason.SELF_IMPROVEMENT_ALLOWED == "self_improvement_allowed"


def test_kernel_deny_reason_covers_policy_reasons() -> None:
    """Every reason string emitted by policy.py must appear in KernelDenyReason."""
    policy_reasons = {
        "prod_requires_allow_subjects",
        "prod_requires_allow_actions",
        "subject_denylist",
        "subject_not_in_allowlist",
        "action_denylist",
        "action_not_in_allowlist",
        "artifact_requires_privileged_caller",
        "missing_artifact_kind",
        "artifact_kind_not_promotable",
        "code_modification_requires_sio",
        "code_modification_immutable_module",
        "code_modification_immutable_function",
        "code_modification_missing_verification",
        "code_modification_verification_failed",
        "code_modification_requires_operator_attestation",
        "evolutionary_operation_requires_authorized_subject",
        "evolutionary_operation_missing_target_module",
        "evolutionary_target_outside_search_space",
        "evolutionary_code_matches_denied_pattern",
        "evolutionary_target_immutable_module",
        "evolutionary_target_immutable_function",
        "evolutionary_requires_operator_attestation",
        "evolutionary_invalid_verification_format",
        "evolutionary_verification_failed",
        "evolutionary_allowed",
        "self_improvement_requires_authorized_subject",
        "self_improvement_safety_critical_requires_attestation",
        "self_improvement_requires_operator_attestation",
        "self_improvement_invalid_safety_invariants",
        "self_improvement_safety_invariants_failed",
        "self_improvement_allowed",
        "allowed",
    }
    enum_values = {m.value for m in KernelDenyReason}
    missing = policy_reasons - enum_values
    assert not missing, f"KernelDenyReason missing reason codes: {missing}"


# ---------------------------------------------------------------------------
# __all__ completeness
# ---------------------------------------------------------------------------


def test_all_exports() -> None:
    import arya_contracts

    expected = {
        "NanoArtifactSpec",
        "NanoDecisionSpec",
        "NanoImplKind",
        "KernelPolicyDecision",
        "KernelDenyReason",
    }
    assert set(arya_contracts.__all__) == expected

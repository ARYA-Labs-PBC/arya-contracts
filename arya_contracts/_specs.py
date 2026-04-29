"""Nano decision architecture contracts — extracted from packages/core/nano.py (ARY-1882).

These types define the contract surface for nano decision mechanisms in ARYA Labs.
Zero non-stdlib dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NanoImplKind(str, Enum):
    """Implementation kind for a nano decision artifact."""

    RULES = "rules"
    FORMULA = "formula"
    LINEAR = "linear"
    TABULAR = "tabular"
    TINY_NN = "tiny_nn"


@dataclass(frozen=True, slots=True)
class NanoArtifactSpec:
    """Specification for a nano artifact (size, determinism, implementation kind)."""

    kind: str
    size_budget_bytes: int
    deterministic: bool = True
    notes: str | None = None


@dataclass(frozen=True, slots=True)
class NanoDecisionSpec:
    """Declare how a decision capability can be implemented as nano artifacts."""

    capability: str
    nano_impl: NanoArtifactSpec
    fallback_impl: NanoArtifactSpec
    safety_critical: bool = True

"""The package layout is part of the architecture, so it is asserted like any other rule."""

from __future__ import annotations

import importlib
from pathlib import Path

import pytest

import labpilot

CONTEXTS = (
    "experimentation",
    "governance",
    "codebase",
    "evidence",
    "orchestration",
    "evaluation",
)

LAYERS = ("domain", "application", "infrastructure", "interface")


@pytest.mark.unit
def test_version_is_exposed() -> None:
    assert labpilot.__version__ == "0.1.0"


@pytest.mark.unit
@pytest.mark.parametrize("context", CONTEXTS)
@pytest.mark.parametrize("layer", LAYERS)
def test_every_context_exposes_every_layer(context: str, layer: str) -> None:
    module = importlib.import_module(f"labpilot.contexts.{context}.{layer}")
    assert module.__file__ is not None


@pytest.mark.unit
@pytest.mark.parametrize("package", ["shared_kernel", "platform", "composition", "contexts"])
def test_supporting_packages_are_importable(package: str) -> None:
    module = importlib.import_module(f"labpilot.{package}")
    assert module.__doc__, f"labpilot.{package} should document its purpose"


@pytest.mark.unit
@pytest.mark.parametrize("context", CONTEXTS)
def test_every_context_documents_its_responsibility(context: str) -> None:
    module = importlib.import_module(f"labpilot.contexts.{context}")
    assert module.__doc__, f"context {context} should state what it owns"


@pytest.mark.unit
def test_architecture_contracts_are_configured(project_root: Path) -> None:
    config = (project_root / ".importlinter").read_text(encoding="utf-8")
    for contract in (
        "top-level-layers",
        "context-internal-layers",
        "supporting-contexts-independent",
        "orchestration-uses-published-interfaces",
        "domain-is-framework-free",
    ):
        assert f"importlinter:contract:{contract}" in config

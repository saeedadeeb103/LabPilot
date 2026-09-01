"""Composition roots: the only place where concrete adapters meet ports.

Each process (API, worker, MCP server, CLI) builds its object graph here and
passes dependencies inward. Nothing else in the package constructs an adapter,
which is what keeps the contexts testable without patching module globals.
"""

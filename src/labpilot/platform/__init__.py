"""Cross-cutting technical infrastructure shared by every process.

Configuration, database sessions, messaging, telemetry, and resilient HTTP live
here. This package holds no business rules and must never import from
``labpilot.contexts``; the dependency runs in the opposite direction.
"""

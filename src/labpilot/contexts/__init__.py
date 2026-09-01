"""The six bounded contexts that make up LabPilot.

Each context owns its own vocabulary, aggregates, and persistence, and is laid
out hexagonally as ``domain`` -> ``application`` -> ``infrastructure`` and
``interface``. Contexts reach each other only through published application
services and domain events, never by importing another context's ``domain`` or
``infrastructure``.
"""

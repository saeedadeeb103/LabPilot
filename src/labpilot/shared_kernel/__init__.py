"""Primitives that every bounded context is permitted to depend on.

The shared kernel is deliberately small. Adding anything here couples all six
contexts to it, so a concept belongs in this package only when it is genuinely
context-neutral and stable: typed identifiers, digests, the result and error
taxonomy, the domain event base, and the clock abstraction.
"""

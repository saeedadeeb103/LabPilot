"""Codebase: bounded, safe interaction with a local ML repository.

Supporting context. The ``SafePath`` value object canonicalises and contains
every path inside the configured repository root after symlink resolution, which
is what makes traversal attacks impossible rather than merely unlikely. Patch
applications record their pre-image revision so a revert is exact.
"""

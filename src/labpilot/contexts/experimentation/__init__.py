"""Experimentation: the lifecycle of a single ML experiment run.

Core domain. The ``ExperimentRun`` aggregate guards the transitions
``pending -> validated -> queued -> running -> terminal`` and enforces the two
invariants the whole security model rests on: a specification can never carry a
free-form command, and one idempotency key can never yield two runs.

Execution reaches the outside world through the ``ExecutionRunner`` port, so a
local subprocess adapter and a container adapter are interchangeable.
"""

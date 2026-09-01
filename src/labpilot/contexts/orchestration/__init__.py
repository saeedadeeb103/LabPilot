"""Orchestration: the process manager that drives a research session.

Holds the conversation, the plan, and the step budget in the
``ResearchOpsSession`` aggregate. This is the only context permitted to talk to
a language model, which keeps probabilistic behaviour confined to one place and
leaves every other context deterministic and unit-testable.
"""

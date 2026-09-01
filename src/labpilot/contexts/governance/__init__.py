"""Governance: authorization, human approval, and the audit trail.

Core domain, kept deliberately separate from the agent that requests its
decisions. The ``Approval`` aggregate binds a decision to one tool name and one
argument digest, so changing arguments after approval invalidates it. Policy
denials are terminal: no amount of model output can overturn one.
"""

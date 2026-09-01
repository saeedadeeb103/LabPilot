"""Evidence: the mapping from stated claims to verifiable facts.

Supporting context. Reports are only as trustworthy as their grounding, so the
``ClaimVerifier`` refuses to mark a report verified while any factual claim
lacks an evidence reference. The tracking system is reached through a gateway
port, keeping MLflow's vocabulary out of the domain.
"""

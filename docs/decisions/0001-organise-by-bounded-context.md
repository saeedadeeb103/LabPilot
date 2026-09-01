# 1. Organise the codebase by bounded context

- Status: accepted
- Date: 2026-09-02

## Context

The first draft of the plan proposed a technology-layered layout: `orchestrator/`,
`mcp_servers/`, `worker/`, `packages/contracts/`, and so on. That shape is easy to
start with and gets harder every week, because a single business concept ends up
smeared across four top-level directories.

Take "submit an experiment". Under a layered layout the specification lives in
`packages/contracts/experiment.py`, the tool that accepts it in
`mcp_servers/experiment/tools.py`, the command construction in
`worker/command_registry.py`, and the container call in `worker/docker_runner.py`.
Changing one invariant, such as forbidding a free-form command field, means
touching four packages and hoping no fifth place also constructs a command. The
compiler cannot help, because nothing declares that these files belong together.

The invariants this project exists to demonstrate are exactly the kind that must
not be bypassable:

- a specification can never carry a free-form command
- one idempotency key can never produce two runs
- an approval binds to one tool name and one argument digest
- every path resolves inside the repository root after symlink resolution

An invariant enforced in one of four places is not an invariant.

## Decision

Organise `src/labpilot` by bounded context, with each context internally
hexagonal.

```text
src/labpilot/contexts/<context>/
    domain/          entities, value objects, aggregates, events, ports
    application/     use cases, commands, queries, unit of work
    infrastructure/  adapters for databases and external systems
    interface/       inbound adapters: MCP tools, HTTP routers, CLI
```

Six contexts: Experimentation and Governance as core domains, Codebase, Evidence
and Evaluation as supporting, and Orchestration as a process manager over the
others. A deliberately small shared kernel holds context-neutral primitives, and
`platform/` holds cross-cutting technical concerns with no business rules.

Two rules make this real rather than aspirational:

1. Dependencies point inward: `domain` <- `application` <- `infrastructure` and
   `interface`, where `infrastructure` and `interface` are independent siblings.
2. Contexts reach each other only through published application services and
   domain events, never by importing another context's `domain` or
   `infrastructure`.

Both rules are encoded as [import-linter](../../.importlinter) contracts that run
in CI and in the pre-commit hook.

## Consequences

Good:

- Each invariant has exactly one home, and the aggregate that owns it is the only
  way to violate it.
- The domain layer imports no framework, so the interesting logic is testable
  without a database, a container runtime, or a language model.
- Adapters are swappable by construction. This is what lets a local subprocess
  runner and a container runner satisfy the same port, and what will later let a
  Slurm adapter join without a domain change.
- Every context is a candidate for extraction into its own service. Because
  inbound and outbound adapters already sit behind ports, extraction becomes a
  packaging change.
- Boundary erosion fails the build instead of surfacing in review.

Costs, accepted:

- More indirection than a flat layout, and more files for the same behaviour.
  Justified only because the security properties depend on single points of
  enforcement.
- Contributors must learn where a concept belongs. The context docstrings and
  this record exist to shorten that.
- Cross-context reads that would be a trivial join in a shared schema become an
  explicit application call or a projection.

## Alternatives considered

**Technology-layered packages.** Rejected for the reasons above: no single home
for an invariant, and no mechanical way to detect drift.

**A single flat package with modules.** Simplest for a project this size, and
tempting. Rejected because the evaluation story depends on comparing an
unrestricted variant against a hardened one, which requires the enforcement
points to be identifiable and swappable rather than diffuse.

**Separate services per context from day one.** Rejected as premature. The
context boundaries give most of the benefit at a fraction of the operational
cost, and the ports make later extraction cheap.

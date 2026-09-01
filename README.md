# LabPilot

**A policy-governed MCP agent for reproducible ML experimentation.**

LabPilot investigates how autonomous agents can safely operate ML experimentation
workflows. The system separates probabilistic planning from deterministic
authorization and execution using typed MCP tools, policy-as-code, human
approvals, isolated containers, experiment tracking, and trace-based evaluation.

> Status: early development. Phase 0 of 12. See
> [docs/implementation-plan.md](docs/implementation-plan.md) for the full plan and
> [docs/decisions](docs/decisions) for the architecture decision records.

---

## The problem

An agent that can run ML experiments is useful. An agent that can run ML
experiments *and* edit your repository is dangerous, because the same natural
language channel carries both the instruction and any untrusted content the agent
reads along the way. Prompt injection in a README, a path that escapes the
repository root, an approval reused after the arguments changed: each of these
turns a helpful assistant into an unreviewed committer.

LabPilot's answer is to give the model no authority at all. It proposes typed
objects; deterministic services decide whether those objects execute.

```text
The model proposes actions. Deterministic services decide whether and how
those actions execute.
```

There is no shell tool. An experiment is described by an `ExperimentSpec` with a
closed set of entrypoints, and a registry translates an approved entrypoint into
a known command. A patch is applied only when the presented approval token
matches the SHA-256 digest of the exact arguments being executed.

## Workflow

```text
request -> parse -> inspect repository -> plan -> validate -> policy gate
        -> human approval -> sandboxed execution -> verify against evidence
        -> evidence-linked report
```

## Architecture

The codebase is organised by bounded context, not by technical layer.

| Context | Role | Owns |
|---|---|---|
| Experimentation | Core | `ExperimentRun` lifecycle, specs, resource limits, execution port |
| Governance | Core | Policy decisions, argument-bound approvals, audit trail |
| Codebase | Supporting | Path containment, file reads, patch proposal and revert |
| Evidence | Supporting | Metrics, artifact digests, claim verification |
| Orchestration | Process | The session state machine and the only model provider |
| Evaluation | Supporting | The benchmark suite and its graders |

Each context is internally hexagonal:

```text
domain  <-  application  <-  infrastructure | interface
```

Those arrows are enforced by [import-linter](.importlinter) contracts that run in
CI, so the architecture cannot quietly erode. Contexts talk to each other through
published application services and domain events, never by importing another
context's internals.

## Layout

```text
src/labpilot/
  shared_kernel/   identifiers, digests, Result, events, clock
  platform/        config, db, messaging, telemetry, http (no business rules)
  contexts/        the six bounded contexts
  composition/     dependency wiring per process
apps/              thin process entrypoints
examples/          the ML repositories the agent operates on
policies/          Rego policies and their tests
tests/             unit, property, contract, integration, adversarial, e2e
```

## Getting started

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/). A container runtime is
not needed until the sandbox phase.

```bash
uv venv --python 3.12
uv sync --all-groups
make check
```

`make check` runs formatting, linting, type checking, the architecture contracts,
and the test suite. Run `make help` to see the individual targets.

## Security model

| Action | Policy |
|---|---|
| Search or read repository | Automatic |
| Read experiment metrics | Automatic |
| Create patch preview | Automatic |
| Apply or revert patch | Human approval |
| Start or cancel experiment | Human approval |
| Enable container networking | Always forbidden |
| Run arbitrary shell command | Always forbidden |
| Edit secrets or credentials | Always forbidden |

Approvals are bound to a tool name and an argument digest, expire, and are
single-use. Experiments run in ephemeral containers with no network, a read-only
root filesystem, dropped capabilities, and a hard resource ceiling.

## Evaluation

A 70-task benchmark covering repository understanding, experiment planning,
change and execute, results analysis, failure recovery, and adversarial security
scenarios, run against three variants: an unrestricted agent, a typed agent, and
hardened LabPilot. Results are published once measured; no numbers are claimed
before then.

## License

MIT. See [LICENSE](LICENSE).

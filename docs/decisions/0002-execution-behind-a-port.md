# 2. Put experiment execution behind a port with two adapters

- Status: accepted
- Date: 2026-09-02

## Context

Container isolation is the security boundary of this project. Experiments run
untrusted repository content, so the sandbox restrictions, no network, read-only
root filesystem, dropped capabilities, non-root user, and hard resource ceilings,
are the whole point rather than an operational detail.

That argues for building on the container runtime immediately. Two things argue
against it:

1. The development machine has no container runtime installed, and provisioning
   one pulls in a Linux virtual machine that needs tens of gigabytes.
2. Continuous integration and the fast unit and property test suites should not
   require a running virtual machine to execute a two-second training job.

Coupling the domain directly to the Docker SDK would make both problems
permanent, and would also make a future Slurm or remote-runner adapter a rewrite
rather than an addition.

## Decision

Define a single domain port and implement it twice.

```python
class ExecutionRunner(Protocol):
    async def start(self, spec: ExperimentSpec, output_dir: Path) -> ExecutionHandle: ...
    async def poll(self, handle: ExecutionHandle) -> ExecutionStatus: ...
    async def read_logs(self, handle: ExecutionHandle, offset: int, limit: int) -> LogChunk: ...
    async def cancel(self, handle: ExecutionHandle) -> None: ...
```

- `LocalSubprocessRunner`, built in Phase 4, runs a child process with
  `RLIMIT_AS`, `RLIMIT_CPU`, and `RLIMIT_NPROC`, a wall-clock timeout, a scrubbed
  environment, and a dedicated output directory.
- `DockerRunner`, built in Phase 6, provides the real isolation guarantee.

The same contract test suite runs against both adapters, so behavioural drift
between them is caught rather than assumed away.

The local adapter is explicitly **not** an isolation mechanism. It offers
resource bounds and reproducibility, nothing more, and it is never used to
execute untrusted content. Configuration selects the adapter, the default outside
development is the container runner, and the selected adapter is recorded on every
run so a result can never be misread as sandboxed when it was not.

## Consequences

Good:

- Phases 1 through 5 make progress with no virtualization installed, and the fast
  test suites stay fast.
- CI runs the full experiment lifecycle without a privileged runner.
- A Slurm or remote adapter later is an addition behind an existing port.
- Forcing the port to be expressible in domain terms keeps Docker's vocabulary
  out of the domain, which is the same discipline applied to MLflow and OPA.

Costs and risks, accepted:

- Two adapters mean two code paths. Mitigated by sharing one contract test suite.
- A local runner that resembles the real thing invites accidental use in the
  wrong place. Mitigated by recording the adapter on each run, defaulting to the
  container runner outside development, and refusing the local runner for any
  spec whose repository content is untrusted.
- The security properties are unproven until Phase 6. Accepted, because the
  adversarial benchmark in Phase 11 tests them against the container adapter,
  which is the configuration the results describe.

## Alternatives considered

**Depend on the Docker SDK directly in the application layer.** Simpler, and it
makes the sandbox real on day one. Rejected because it blocks all progress on a
runtime install, makes CI require privileged runners, and turns any future
execution backend into a rewrite.

**Local execution only for version 1.** Rejected outright. Without container
isolation the project's central claim is unsupported, and the adversarial
benchmark would measure nothing.

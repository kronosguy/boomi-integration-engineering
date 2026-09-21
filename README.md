# Boomi Integration Engineering

**A Boomi-built integration engineering and reliability lab focused on enterprise workforce, payroll, data, and operational integration.**

This repository is being built **entirely through Boomi** as a working engineering environment. Boomi processes, connectors, APIs, transformations, routing, error handling, orchestration, and integration patterns are used to build, execute, validate, and publish the artifacts contained in this repository.

The objective is not to demonstrate simple point-to-point connectivity. It is to engineer integrations that remain **correct, recoverable, observable, and restart-safe under failure**.

---

## What This Repository Demonstrates

The lab uses realistic workforce and payroll integration problems to examine what happens when integrations encounter conditions that are easy to overlook in a normal happy-path implementation:

* Large payloads exceeding runtime memory constraints
* Pagination against mutable source systems
* Duplicate and conflicting employee identities
* Token expiration and credential rotation
* Partial responses and ambiguous HTTP outcomes
* Schema and contract changes during execution
* Cross-midnight and daylight-saving time calculations
* Fixed-width payroll files with byte-level requirements
* Database deadlocks and concurrent updates
* CDC retention gaps
* Dead-letter recovery and poison records
* Distributed transaction limitations
* Duplicate delivery and idempotency
* Runtime failover and stale workers
* API quotas and competing workloads
* Encrypted and signed payroll files
* Historical corrections and bitemporal reporting
* Payroll publication gates and reconciliation

Each scenario is designed around a specific architectural trap, a controlled failure condition, and a measurable recovery requirement.

---

## Core Engineering Principle

**Technical success is not the same as business success.**

A process returning HTTP 200 does not necessarily mean the business transaction succeeded.

A completed database transaction does not necessarily mean a downstream processor committed the corresponding operation.

A successful Power BI refresh does not necessarily mean historical reporting is correct.

A balanced payroll total does not necessarily mean the correct employees received the correct amounts.

The lab therefore emphasizes:

```text
Source
  ↓
Ingestion
  ↓
Validation
  ↓
Canonicalization
  ↓
Transformation
  ↓
Persistence
  ↓
Business Processing
  ↓
Publication
  ↓
Reconciliation
  ↓
Evidence
```

Every stage must have an explicit understanding of **what was received, what was changed, what was committed, what failed, and what remains uncertain**.

---

# Engineering Scenarios

## 01. Payroll Close Under a Hard Memory Ceiling

Consolidate a 12 GB UKG-style workforce export through a Boomi Atom with a 2 GB JVM heap.

The lab examines:

* Streaming versus buffered processing
* Upstream partitioning
* Connector and parser memory behavior
* Disk spill
* Bounded concurrency
* Durable chunk manifests
* Oversized employee histories
* Mid-execution Atom termination
* Recovery without duplicate payroll output

**Goal:** Recover from failure without restarting the complete extract or losing durably processed records.

---

## 02. The Employee Cache That Lies

Integrate overlapping SuccessFactors, UKG, and payroll identities across 250,000 synthetic workers.

The lab addresses:

* Person versus employment identity
* Assignment identity
* Payroll identity
* Concurrent employment
* Rehires
* Conflicting duplicates
* Effective-dated resolution
* Durable identity state
* Cache visibility across execution boundaries

**Goal:** Produce deterministic identity results regardless of page order or parallel ingestion.

---

## 03. Authentication Expiry During an Eight-Hour Extract

Run a long workforce extraction across multiple authentication lifecycles.

Test:

* OAuth expiration
* SAML-bearer authentication
* Certificate rotation
* Clock skew
* Simultaneous 401 responses
* Permission failures
* Token-renewal coordination
* Pagination continuity
* Ambiguous authenticated writes

**Goal:** Renew credentials without skipping pages, creating renewal stampedes, or blindly replaying uncertain operations.

---

## 04. Pagination Across a Moving Workforce

Extract workforce records while administrators continue changing the source.

Compare:

* Snapshot-consistent pagination
* Mutable pagination
* Continuation links
* Query boundaries
* Tie-breaker keys
* Overlap strategies
* Deduplication
* Reconciliation

**Goal:** Explicitly identify when a source contract cannot provide a complete snapshot instead of falsely reporting success.

---

## 05. Hierarchy Reconstruction Without Payroll Explosion

Transform independently arriving employment, assignment, compensation, and organizational collections into a payroll hierarchy.

The lab examines:

* Relationship grains
* Canonical XML
* Boomi Maps
* XSLT
* Namespace preservation
* Deterministic ordering
* Null versus empty semantics
* Orphan relationships
* Effective dating
* Repeating compensation collections

**Goal:** Prove that every source earning appears exactly once without Cartesian multiplication.

---

## 06. Byte-Perfect Legacy Payroll

Generate a fixed-position payroll file with a strict 240-byte Windows-1252 record contract.

Validate:

* Byte versus character length
* Decimal precision
* Rounding
* Negative adjustments
* Negative zero
* Overflow
* Encoding
* Trailer totals
* CRLF handling
* Independent record reconstruction

**Goal:** Produce a financially and structurally correct payroll file that can survive strict downstream validation.

---

## 07. The Payroll Processor Committed, But Boomi Never Heard Back

Model a remote payroll processor that commits a batch before the connection fails.

Implement:

* Durable submission state
* Immutable batch identifiers
* Payload hashes
* Idempotency keys
* Submission ledgers
* Status reconciliation
* Ambiguous outcomes

**Goal:** Distinguish confirmed failure from an unknown commit outcome and prevent accidental duplicate payroll submission.

---

## 08. A Dead Letter Queue That Survives Its Own Recovery

Build a durable workforce and payroll failure-management pattern.

Classify:

* Transport failures
* HTTP failures
* Application failures
* Record-level failures
* Retryable outcomes
* Repairable outcomes
* Ambiguous outcomes
* Terminal outcomes

Implement:

* Retry budgets
* Exponential backoff
* Jitter
* Retry-After
* Circuit breakers
* Replay controls
* Attempt history
* Redacted diagnostics

**Goal:** Recover failed records without creating poison-message loops or repeating successful business effects.

---

## 09. Retroactive HR Truth Versus Previously Paid Truth

Model retroactive workforce changes after payroll and finance have already closed.

Implement:

* Business-effective timelines
* Observation timelines
* Bitemporal records
* Historical corrections
* Adjustment candidates
* Immutable paid results
* Reproducible reporting

**Goal:** Preserve both what was originally reported and what is currently understood.

---

## 10. DST, Cross-Midnight Work, and the Phantom Overtime Hour

Process workforce punches across time zones and daylight-saving transitions.

Test:

* Ambiguous local timestamps
* Nonexistent local timestamps
* Cross-midnight shifts
* Time-zone transfers
* Missing offsets
* Late punches
* Workday boundaries
* Overtime boundaries
* Rounding policies

**Goal:** Separate elapsed-time conservation from policy-based paid-time calculations.

---

## 11. CDC Recovery After the Retention Window Has Disappeared

Recover a SQL Server CDC process after its saved position is no longer available.

Implement:

* Durable checkpoints
* Update and delete handling
* Transaction awareness
* Retention-gap detection
* Consistent baseline recovery
* Source reconciliation

**Goal:** Prevent silent data loss when the previous CDC position can no longer be resumed.

---

## 12. Deadlocks, Hot Employees, and Partial Warehouse Commits

Load large workforce datasets concurrently into SQL Server while multiple executions compete for the same business keys.

Test:

* Skewed partitions
* Concurrent upserts
* Uniqueness constraints
* Lock ordering
* Deadlock retries
* Duplicate delivery
* Connection loss after commit
* Unknown commit outcomes

**Goal:** Achieve restart-safe database application without duplicate facts or broken dimension relationships.

---

## 13. Power BI Is Green While Historical Payroll Is Wrong

Detect reporting corrections that fall outside a normal rolling refresh window.

Implement:

* Warehouse invalidation tracking
* Historical refresh orchestration
* Correction intervals
* Delete handling
* Refresh failure recovery
* Publication versions
* Warehouse-to-model reconciliation

**Goal:** Treat successful refresh as an operational event, not proof of historical correctness.

---

## 14. Shared API Quotas During Payroll-Critical Traffic

Coordinate multiple workloads competing for the same constrained API capacity.

Test:

* Request-based limits
* Concurrency limits
* GraphQL query-cost limits
* HTTP 429 responses
* Changing rate-limit headers
* Backoff behavior
* Payroll priority
* Tenant fairness
* Deferred work

**Goal:** Control shared capacity without starving payroll traffic or creating synchronized retry storms.

---

## 15. Encrypted Payroll Files With Hostile Failure Modes

Process encrypted, signed, and compressed payroll results delivered through SFTP.

Validate:

* Signature verification
* Trusted sender identity
* Key rotation
* Wrong-recipient files
* Truncated ciphertext
* Archive expansion limits
* Temporary storage limits
* Restricted plaintext handling
* Cleanup after termination

**Goal:** Prevent unverified payroll plaintext from reaching downstream processing while maintaining recoverable operational evidence.

---

## 16. Rehire and Concurrent Employment Break the Identity Model

Model employees who leave, return, change identity attributes, or work concurrently for multiple subsidiaries.

Test:

* Recycled employee numbers
* Name changes
* Concurrent employment
* Legal-entity context
* Temporal identity relationships
* Crosswalk versioning
* Reviewed merges
* Unmerges
* Historical replay

**Goal:** Prevent uncertain identity matches from silently reaching payroll.

---

## 17. Schema Drift Halfway Through a Payroll Run

Introduce source and target contract changes while a payroll extraction is already executing.

Test:

* Additive fields
* Type changes
* New enum values
* Missing collections
* Semantic changes
* Versioned mappings
* Golden-corpus comparison
* Mapping compatibility
* Controlled replay

**Goal:** Detect semantic contract changes instead of treating every syntactically valid payload as compatible.

---

## 18. Split-Brain Execution After Runtime Failover

Simulate a worker continuing after another execution has taken ownership of its partition.

Implement:

* Durable work claims
* Lease management
* Fencing tokens
* Database enforcement
* Destination idempotency
* Network partition handling

**Goal:** Prevent stale workers from overwriting newer progress or producing duplicate payroll effects.

---

## 19. Employee Provisioning as a Recoverable Saga

Coordinate employee lifecycle changes across systems that cannot participate in one distributed transaction.

Orchestrate:

* Hiring
* Employment creation
* Payroll enrollment
* Reporting
* Transfers
* Corrections
* Terminations
* Compensation changes

Track:

* Desired state
* Observed state
* Dependencies
* Retries
* Compensating actions
* Manual changes
* Reconciliation

**Goal:** Drive systems toward a consistent state without deleting legitimate workforce activity or incorrectly reactivating terminated employment.

---

## 20. Payroll-Close Recovery With an Auditable Publication Gate

Combine the preceding failure patterns into an end-to-end payroll-close scenario.

During the final payroll window, introduce simultaneous failures involving:

* Retroactive HR changes
* Missing UKG pages
* Atom failure
* Partial payroll acknowledgement
* Identity reconciliation
* Reporting publication

Build:

* Immutable manifests
* Source completeness evidence
* Record-level lineage
* Destination acknowledgements
* Reconciliation controls
* Publication gates
* Machine-readable evidence

**Goal:** Do not publish payroll merely because individual systems report technical success.

Publication requires evidence that the declared close contract has been satisfied.

---

# Architecture Themes

The scenarios repeatedly test a core set of integration engineering disciplines.

### Reliability

* Restart-safe processing
* Checkpointing
* Durable state
* Idempotency
* Failure classification
* Controlled retries
* Recovery procedures

### Data Integrity

* Deterministic identity
* Effective dating
* Record lineage
* Reconciliation
* Versioned mappings
* Immutable transaction history

### Performance

* Bounded memory
* Streaming
* Partitioning
* Concurrency control
* Database locking behavior
* API admission control
* Disk utilization

### Security

* Credential lifecycle
* Secret protection
* Authorization
* Signature verification
* Restricted temporary storage
* Operational log hygiene

### Observability

Every significant process should be able to answer:

```text
What did we receive?
What did we process?
What did we reject?
What did we defer?
What did we commit?
What did the destination acknowledge?
What remains uncertain?
Can we prove it?
```

---

# Repository Structure

The repository is organized around deployable integration engineering artifacts rather than documentation alone.

```text
boomi-integration-engineering/
│
├── lab/
│   ├── health-check.txt
│   └── ...
│
├── scenarios/
│   ├── 01-payroll-memory/
│   ├── 02-employee-identity/
│   ├── 03-authentication-expiry/
│   └── ...
│
├── processes/
├── profiles/
├── maps/
├── scripts/
├── test-data/
├── evidence/
└── README.md
```

Artifacts are progressively generated and published through **Boomi integration processes**.

---

# What "Built by Boomi" Means

Boomi is not simply the subject of this repository.

**Boomi is the engineering platform used to build it.**

The repository is intended to demonstrate practical use of Boomi for:

* Process orchestration
* HTTP and REST integration
* API interaction
* File processing
* Data transformation
* JSON and XML handling
* Routing
* Error handling
* Retry patterns
* Database integration
* SFTP workflows
* Runtime execution
* Operational controls
* Integration testing
* Evidence generation
* Repository publication

The GitHub repository itself serves as an externally visible evidence layer for the integration work performed by Boomi.

---

# Current Proof of Integration

The initial integration path demonstrates Boomi writing an artifact directly into this repository through the GitHub REST API.

```text
Boomi Process
     │
     ▼
Message
     │
     ▼
HTTP Client
     │
     ▼
GitHub REST API
     │
     ▼
Repository Artifact
```

This establishes the foundation for progressively publishing lab artifacts, test evidence, configuration documentation, and engineering results through Boomi-managed processes.

---

# Engineering Standard

The objective of this repository is to move beyond:

> "The integration ran successfully."

The standard is:

> **The integration can explain what happened, recover from what failed, prove what was committed, and demonstrate why the resulting business state is correct.**

That standard applies across every scenario in the lab.

---

## Status

**Active Engineering Lab**

Platform: **Boomi**

Repository: **Boomi Integration Engineering**

Focus: **Integration Engineering, Reliability, Workforce Data, Payroll, APIs, Data Integrity, Recovery, and Observability**

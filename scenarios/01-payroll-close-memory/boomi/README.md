# Boomi Process XML

`processes/` contains the `<process>...</process>` XML bodies for the implemented Project 01 components used in the verified 12 GiB / 2 GiB heap execution path.

The XML is intentionally committed so the Boomi design can be reviewed outside the AtomSphere canvas: shape topology, connector actions, Flow Control settings, Dynamic Document Properties, process calls, custom Groovy, validation decisions, and recovery logic are all visible as source.

These files are process-body XML rather than complete portable Boomi deployment packages. Component IDs are intentionally retained where they are part of the implementation relationships and execution evidence. No API token, credential, password, or SQL connection secret is committed.

## Included process definitions

- `P01.C01 - Stream File Integrity.xml` — reusable fixed-buffer SHA-256 and byte-count integrity subprocess.
- `P01.15 - 12GB Source Proof.xml` — binds the real 12 GiB monolithic source and records source integrity plus JVM heap ceiling evidence.
- `P01.20 - Manifest Controller.xml` — converts the 374-entry manifest into durable READY work controls.
- `P01.30 - Chunk Processor.xml` — serial manifest-driven chunk processing, state transition, integrity, validation, and commit/quarantine routing.
- `P01.40 - Validation.xml` — verifies byte-count and SHA-256 expectations.
- `P01.50 - SQL Staging Contract.xml` — staging contract used by the current lab path; the physical SQL Server binding remains a separate implementation milestone.
- `P01.80 - Recovery.xml` — recovery sweep for stale PROCESSING state while preserving committed work.

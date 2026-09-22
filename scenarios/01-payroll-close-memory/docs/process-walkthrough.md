# Project 01 Process Walkthrough

This is a source-and-evidence view of the Boomi implementation used for the successful 12 GiB source / 2 GiB JVM heap proof.

## Executed path

```text
P01.15 - 12GB Source Proof
  -> P01.C01 - Stream File Integrity
  -> complete SHA-256 + byte count + JVM max heap proof

P01.20 - Manifest Controller
  -> read one manifest document
  -> split 374 manifest entries
  -> create READY work controls

P01.30 - Chunk Processor
  -> read one manifest document
  -> split internally
  -> Flow Control: one chunk at a time
  -> READY -> PROCESSING
  -> P01.C01 stream integrity check
  -> P01.40 validation
  -> P01.50 SQL staging contract
  -> PROCESSING -> COMMITTED or QUARANTINE
```

## Why the XML is committed

The XML files under `boomi/processes/` are the process-body definitions used for the implemented Boomi components. They make the process topology and configuration reviewable without requiring access to the original AtomSphere account.

A reviewer can follow the exact implementation details directly in source, including:

- the 64 KiB bounded stream buffer;
- SHA-256 and byte-count integrity checks;
- `allowSimultaneous="false"` and one-document Flow Control;
- manifest splitting and work-item mapping;
- READY -> PROCESSING -> COMMITTED / QUARANTINE state movement;
- validation subprocess calls;
- recovery logic for stale PROCESSING controls.

## Important boundary

`P01.50 - SQL Staging Contract.xml` is intentionally a contract, not a live SQL Server binding. No SQL endpoint, database, or credentials were supplied for this execution. The verified 12 GiB result therefore establishes bounded streaming, source integrity, manifest control, chunk state transitions, and terminal reconciliation of 374 work units. It does not claim that a production SQL Server stage or final payroll publication path was executed.

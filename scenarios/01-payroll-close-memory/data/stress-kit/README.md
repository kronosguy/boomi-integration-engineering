# UKG 12 GB Stress Dataset Kit

This package generates a deterministic UKG-shaped `ACTUAL_TOTALS` workload based on the source contract established from UKG Pro WFM API responses.

## Default workload

- Target size: 12 GiB
- Chunk target: ~32 MiB per valid JSON array
- Period: 2026-09-14 through 2026-09-20
- Normal payroll-detail rows use `combined=false`
- Calculated totals use `combined=true`
- Deterministic corrections, transfers, null hours, unknown cost centers, duplicate IDs, and one 250,000-row oversized employee are injected.

## Generate

```powershell
python .\generate_12gb.py
```

For a small smoke test first:

```powershell
python .\generate_12gb.py --target-gib 0.05 --chunk-mib 8 --output smoke-test
```

The generator writes:

```text
dataset/
├── manifest.json
└── timecard_metrics/
    ├── chunk-000001.json
    ├── chunk-000002.json
    └── ...
```

Each chunk is independently valid JSON so Boomi can process bounded files instead of loading a monolithic 12 GB document.

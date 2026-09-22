# Evidence Chain

## Verified result

| Control | Result |
|---|---:|
| Monolithic source bytes | 12,884,931,079 |
| Source SHA-256 | `d4f808f83cd00505cd180e6e6be78d923a1cd4056c419de097eb6e2125d2b7c8` |
| JVM max heap | 2,147,483,648 bytes / 2 GiB |
| Stream buffer | 65,536 bytes |
| Manifest chunks | 374 |
| Manifest employees | 418,418 |
| READY after | 0 |
| PROCESSING after | 0 |
| COMMITTED after | 374 |
| QUARANTINE after | 0 |
| Final status | PASSED |

## Boomi execution IDs

| Process | Execution |
|---|---|
| P01.15 - 12GB Source Proof | `execution-617b8faf-db35-4d2e-9cb7-c78f55834edb-2026.09.21` |
| P01.20 - Manifest Controller | `execution-d8f3c21e-a53c-42d6-96c4-7c8abfc812f0-2026.09.21` |
| P01.30 - Chunk Processor | `execution-6b58a013-38e3-4563-9c1f-b85b618ed787-2026.09.21` |

## Reproducibility

The 12 GiB file itself is intentionally not stored in GitHub. `data/stress-kit/generate_12gb.py`, `data/stress-kit/config.json`, the 374-entry `data/manifest.json`, and the published SHA-256 provide the reproducibility contract without committing a 12 GiB artifact.

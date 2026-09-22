#!/usr/bin/env python3
"""
Generate a deterministic UKG-shaped ACTUAL_TOTALS stress dataset.

Default:
  12 GiB total target
  ~32 MiB valid JSON array chunks

Usage:
  python generate_12gb.py
  python generate_12gb.py --target-gib 0.1 --chunk-mib 8
"""

import argparse
import hashlib
import json
from pathlib import Path
from datetime import date, timedelta

START = date(2026, 9, 14)

JOBS = [
    (70001, "COH/AIRPORTS/IAH/OPERATIONS/RAMP/Agent", "IAHOPS01", 81001),
    (70002, "COH/TRANSIT/METRO/BUS/Operator", "METROBUS", 81002),
    (70003, "COH/FIRE/EMS/Medic", "EMSOPS01", 81003),
    (70004, "COH/PUBLIC WORKS/FIELD/Technician", "PWFIELD1", 81004),
    (70005, "COH/HEALTH/CLINIC/Coordinator", "HLTHCLN1", 81005),
]

PAY = {
    "REG": (114, "REG"),
    "WORKED": (2000000008, "Worked Hours"),
    "COMBINED": (2000000010, "Actual combined hours"),
    "ANALYTICS": (1551, "Analytics - Paid Hours"),
}

def employee(seq):
    q = f"COH{seq:09d}"
    return {"id": 900000000 + seq, "qualifier": q, "name": q}

def lc(seq):
    pos = f"{100000000000 + seq:012d}"
    ref = 500000000 + seq
    return {
        "referenceId": ref,
        "laborString": f"{pos},Empty,Empty",
        "entries": [
            {
                "laborCategory": {"id": 9, "qualifier": "Position Number", "name": "Position Number"},
                "laborCategoryOrderNum": 1,
                "laborCategoryEntry": {"id": 600000000 + seq, "qualifier": pos, "name": pos},
                "laborCategoryEntryDescription": "Synthetic Position"
            },
            {
                "laborCategory": {"id": 59, "qualifier": "Career Ladder", "name": "Career Ladder"},
                "laborCategoryOrderNum": 2,
                "laborCategoryEntry": {"id": 22201, "qualifier": "Empty", "name": "Empty"},
                "laborCategoryEntryDescription": "Empty"
            },
            {
                "laborCategory": {"id": 109, "qualifier": "Cert", "name": "Cert"},
                "laborCategoryOrderNum": 3,
                "laborCategoryEntry": {"id": 31172, "qualifier": "Empty", "name": "Empty"},
                "laborCategoryEntryDescription": "Empty"
            }
        ]
    }

def row(emp, seq, day, pc_key, hours, combined, job_idx, suffix=""):
    pcid, pcname = PAY[pc_key]
    jid, jobpath, cc, ccid = JOBS[job_idx]
    ref = 500000000 + seq
    r = {
        "uniqueId": f"{emp['id']}:{day.isoformat()}:{pcid}{suffix}",
        "employee": emp,
        "payCode": {"id": pcid, "qualifier": pcname, "name": pcname},
        "hoursAmount": hours,
        "wages": 0.0,
        "wagesCurrency": {"amount": 0.0, "currencyCode": "USD"},
        "daysAmount": 0.0,
        "applyDate": day.isoformat(),
        "job": {"id": jid, "qualifier": jobpath, "name": jobpath},
        "jobTransfer": False,
        "laborTransfer": False,
        "amountType": "HOUR",
        "isFromCorrection": False,
        "combined": combined,
        "payPeriodWeek": 1,
        "payPeriodNumber": 20,
        "signedOff": False,
        "wageAddition": 0.0,
        "wageMultiplier": 0.0 if combined else 1.0,
        "laborCategories": lc(seq),
        "costCenter": {
            "referenceId": ref,
            "costCenter": {"id": ccid, "qualifier": cc, "name": cc}
        }
    }
    return r

def employee_payload(seq):
    emp = employee(seq)
    job_idx = seq % len(JOBS)
    totals = []
    for d in range(5):
        day = START + timedelta(days=d)
        totals.append(row(emp, seq, day, "WORKED", 8.0, True, job_idx))
        totals.append(row(emp, seq, day, "COMBINED", 8.0, True, job_idx))
        totals.append(row(emp, seq, day, "ANALYTICS", 8.0, True, job_idx))
        totals.append(row(emp, seq, day, "REG", 8.0, False, job_idx))

    if seq % 200 == 0:
        c = dict(totals[-1])
        c["uniqueId"] += ":CORR"
        c["hoursAmount"] = -8.0
        c["isFromCorrection"] = True
        totals.append(c)

    if seq % 333 == 0:
        totals[-1]["jobTransfer"] = True
        totals[-1]["laborTransfer"] = True

    if seq % 500 == 0:
        totals[-1]["hoursAmount"] = None

    if seq % 777 == 0:
        totals[-1]["costCenter"]["costCenter"] = {
            "id": 999999,
            "qualifier": "UNKNOWN_CC",
            "name": "UNKNOWN_CC"
        }

    if seq % 1000 == 0:
        totals.append(dict(totals[-1]))

    if seq == 2500:
        base = totals[-1]
        for n in range(250000):
            x = dict(base)
            x["uniqueId"] = f"{base['uniqueId']}:OVERSIZED:{n:06d}"
            x["hoursAmount"] = 0.01
            x["syntheticSequence"] = n
            totals.append(x)

    return {"employeeId": emp, "actualTotals": totals}

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target-gib", type=float, default=12.0)
    ap.add_argument("--chunk-mib", type=float, default=32.0)
    ap.add_argument("--output", default="dataset")
    args = ap.parse_args()

    target = int(args.target_gib * 1024**3)
    chunk_target = int(args.chunk_mib * 1024**2)
    root = Path(args.output)
    chunks_dir = root / "timecard_metrics"
    chunks_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "synthetic": True,
        "targetBytes": target,
        "chunkTargetBytes": chunk_target,
        "period": {"startDate": "2026-09-14", "endDate": "2026-09-20"},
        "chunks": []
    }

    total_bytes = 0
    employee_seq = 1
    chunk_no = 1

    while total_bytes < target:
        path = chunks_dir / f"chunk-{chunk_no:06d}.json"
        count = 0
        with open(path, "wb") as f:
            f.write(b"[")
            first = True
            while f.tell() < chunk_target and total_bytes + f.tell() < target:
                payload = employee_payload(employee_seq)
                blob = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
                if not first:
                    f.write(b",")
                f.write(blob)
                first = False
                count += 1
                employee_seq += 1
            f.write(b"]\n")

        size = path.stat().st_size
        digest = sha256(path)
        total_bytes += size
        manifest["chunks"].append({
            "chunk": chunk_no,
            "file": str(path.relative_to(root)),
            "bytes": size,
            "employees": count,
            "sha256": digest
        })
        print(f"{path.name}: {size / 1024**2:.2f} MiB, employees={count}, cumulative={total_bytes / 1024**3:.3f} GiB")
        chunk_no += 1

    manifest["generatedBytes"] = total_bytes
    manifest["generatedGiB"] = total_bytes / 1024**3
    manifest["employeesGenerated"] = employee_seq - 1

    with open(root / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    print(f"Done: {total_bytes / 1024**3:.3f} GiB across {len(manifest['chunks'])} chunks.")

if __name__ == "__main__":
    main()

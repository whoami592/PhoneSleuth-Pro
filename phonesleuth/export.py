"""Export records without writing raw full phone numbers."""
import csv, json
from pathlib import Path

def export_json(records, path):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(records, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    return p

def export_csv(records, path):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    keys = list(records[0].keys()) if records else []
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        if keys:
            writer.writeheader(); writer.writerows(records)
    return p

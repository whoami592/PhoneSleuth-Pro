"""Local SQLite storage with parameterized queries and audit events."""
import json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path

def utc_now():
    return datetime.now(timezone.utc).isoformat()

class Store:
    def __init__(self, path="data/phonesleuth.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def _init(self):
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS cases(
              case_id TEXT PRIMARY KEY, title TEXT NOT NULL, purpose TEXT NOT NULL,
              authorization_note TEXT NOT NULL, created_at TEXT NOT NULL, status TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS reports(
              report_id TEXT PRIMARY KEY, case_id TEXT, phone_hash TEXT,
              masked_number TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL,
              source_url TEXT, incident_date TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL,
              FOREIGN KEY(case_id) REFERENCES cases(case_id)
            );
            CREATE TABLE IF NOT EXISTS audit(
              event_id TEXT PRIMARY KEY, event TEXT NOT NULL, details_json TEXT NOT NULL,
              created_at TEXT NOT NULL
            );
            """)

    def audit(self, event, details):
        with self.connect() as db:
            db.execute("INSERT INTO audit VALUES(?,?,?,?)",
                (str(uuid.uuid4()), event, json.dumps(details, ensure_ascii=False), utc_now()))

    def create_case(self, title, purpose, authorization_note):
        if not all(x.strip() for x in (title, purpose, authorization_note)):
            raise ValueError("Title, purpose, and authorization note are required.")
        cid = "PS-" + uuid.uuid4().hex[:10].upper()
        with self.connect() as db:
            db.execute("INSERT INTO cases VALUES(?,?,?,?,?,?)",
                       (cid, title.strip(), purpose.strip(), authorization_note.strip(), utc_now(), "open"))
        self.audit("case_created", {"case_id": cid, "title": title.strip()})
        return cid

    def list_cases(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM cases ORDER BY created_at DESC")]

    def add_report(self, masked_number, category, description, source_url="", incident_date="", case_id=None, phone_hash=None):
        if not masked_number.strip() or not category.strip() or not description.strip():
            raise ValueError("Masked number, category, and description are required.")
        if source_url and not source_url.startswith(("https://", "http://")):
            raise ValueError("Source URL must start with http:// or https://.")
        rid = "R-" + uuid.uuid4().hex[:10].upper()
        with self.connect() as db:
            if case_id and not db.execute("SELECT 1 FROM cases WHERE case_id=?", (case_id,)).fetchone():
                raise ValueError("Unknown case ID.")
            db.execute("INSERT INTO reports VALUES(?,?,?,?,?,?,?,?,?,?)",
                (rid, case_id, phone_hash, masked_number.strip(), category.strip(),
                 description.strip(), source_url.strip(), incident_date.strip(), "unverified", utc_now()))
        self.audit("report_created", {"report_id": rid, "case_id": case_id, "category": category})
        return rid

    def list_reports(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM reports ORDER BY created_at DESC")]

    def update_status(self, report_id, status):
        if status not in {"unverified", "reviewing", "substantiated", "dismissed"}:
            raise ValueError("Unsupported status.")
        with self.connect() as db:
            cur = db.execute("UPDATE reports SET status=? WHERE report_id=?", (status, report_id))
            if not cur.rowcount:
                raise ValueError("Unknown report ID.")
        self.audit("report_status_updated", {"report_id": report_id, "status": status})

    def list_audit(self):
        with self.connect() as db:
            return [dict(r) for r in db.execute("SELECT * FROM audit ORDER BY created_at DESC")]

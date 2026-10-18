# PhoneSleuth Pro

**Privacy-conscious mobile-number OSINT and investigation toolkit**  
**Credit: coded by mr sabaz ali khan**

PhoneSleuth Pro provides phone-number formatting and numbering-plan metadata, links to public search engines, a local scam-report register, basic forensic case management, audit events, and JSON/CSV exports.

## Legal and ethical use

Use only for lawful purposes and information you are authorized to process. Follow applicable law and organizational policy. Do not use this project to stalk, harass, dox, impersonate, or access private accounts or leaked databases.

This project **does not**:
- reveal a subscriber's identity or CNIC;
- locate a phone in real time or track a person's movements;
- access WhatsApp, SMS, call records, telecom systems, or private databases;
- verify that a number is currently active or owned by a particular person.

Numbering-plan validity is not proof that a phone is active. Carrier/region labels are metadata and may be absent, outdated, or ambiguous. Scam reports are allegations until independently substantiated.

## Features

- Number parsing/formatting and numbering-plan metadata via `phonenumbers`.
- Public-search link builder (opens search engines; no automated scraping).
- Local SQLite case register with authorization note.
- Scam-report records with masked numbers and explicit evidence/source fields.
- Report status workflow: `unverified`, `reviewing`, `substantiated`, `dismissed`.
- Audit events for case/report changes.
- JSON and CSV export.
- Streamlit dashboard.
- Unit tests.

## Project layout

```text
PhoneSleuth-Pro/
├── app.py
├── phonesleuth/
│   ├── __init__.py
│   ├── phone.py
│   ├── osint.py
│   ├── storage.py
│   ├── privacy.py
│   └── export.py
├── tests/
├── data/
├── exports/
├── requirements.txt
├── .gitignore
└── README.md
```

## Windows 10/11 setup (PowerShell)

Install Python 3.10+ from python.org and enable **Add Python to PATH**.

```powershell
cd PhoneSleuth-Pro
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
streamlit run app.py
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Kali Linux setup

```bash
cd PhoneSleuth-Pro
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
streamlit run app.py
```

Open the local URL Streamlit prints (normally `http://localhost:8501`). By default, the app is intended for local use. Do not expose it to a public network without authentication, TLS, access controls, and a security review.

## Usage

1. Open **Number Analyzer** and enter an international number, such as `+923001234567`. This is a format example only; do not assume it belongs to a real person.
2. Use **Public OSINT** to build search links. Review results manually and record source URLs, dates, and context.
3. Create a case and document the authorization basis.
4. Add scam reports using a masked number. Keep descriptions factual; separate observed evidence from assumptions.
5. Update report status only when evidence supports the decision.
6. Export the required dataset to JSON/CSV.

## Privacy and evidence handling

- Store only information necessary for the case.
- Use masked numbers in reports. Do not commit `data/phonesleuth.db` or exports containing sensitive records.
- Keep the SQLite database on an encrypted device with restricted file permissions.
- Back up evidence securely; define retention/deletion rules.
- Preserve source URLs, UTC timestamps, and original files separately when chain of custody is required. This app is a basic register, not a certified forensic acquisition tool.
- A stable identifier hash is available in `phonesleuth.privacy.keyed_hash`; set `PHONESLEUTH_HASH_KEY` to a long random secret before use. Do not use a plain unkeyed hash for phone numbers because the input space is guessable.
- Treat all public-search findings as leads, not proof. Corroborate with independent sources.

## Configuration

- `PHONESLEUTH_DB`: optional path to SQLite database.
- `PHONESLEUTH_HASH_KEY`: optional secret for keyed identifier hashes. The app does not need it unless you use the helper.

## Tests

Run:

```bash
pytest -q
```

## Limitations

No automatic web crawling, people-search aggregation, geolocation, SIM-owner lookup, or telecom integration is included. Search-engine results vary by region and time. Check relevant laws and obtain appropriate authorization before processing personal data.

## License

MIT License. You may add the standard MIT license text in a `LICENSE` file before publishing.

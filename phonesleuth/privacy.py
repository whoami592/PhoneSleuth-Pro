"""Helpers for masking and hashing identifiers."""
import hashlib, os

def mask_number(number: str) -> str:
    digits = "".join(c for c in (number or "") if c.isdigit())
    if len(digits) <= 4:
        return "*" * len(digits)
    return "+" + ("*" * max(0, len(digits)-4)) + digits[-4:]

def keyed_hash(value: str, key: str | None = None) -> str:
    key = key if key is not None else os.environ.get("PHONESLEUTH_HASH_KEY", "")
    if not key:
        raise ValueError("Set PHONESLEUTH_HASH_KEY before creating a stable identifier hash.")
    return hashlib.sha256((key + value).encode("utf-8")).hexdigest()

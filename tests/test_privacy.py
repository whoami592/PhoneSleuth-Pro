import pytest
from phonesleuth.privacy import mask_number, keyed_hash

def test_mask_number():
    assert mask_number("+923001234567").endswith("4567")
    assert "*" in mask_number("+923001234567")

def test_hash_requires_key(monkeypatch):
    monkeypatch.delenv("PHONESLEUTH_HASH_KEY", raising=False)
    with pytest.raises(ValueError):
        keyed_hash("sample")
    assert len(keyed_hash("sample", "test-secret")) == 64

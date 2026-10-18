import pytest
from phonesleuth.storage import Store

def test_case_and_report_lifecycle(tmp_path):
    store = Store(tmp_path / "test.db")
    case_id = store.create_case("Test", "Training case", "Authorized local test")
    report_id = store.add_report("+********4567", "Spam", "Sample report", "https://example.org", case_id=case_id)
    assert store.list_reports()[0]["report_id"] == report_id
    store.update_status(report_id, "reviewing")
    assert store.list_reports()[0]["status"] == "reviewing"
    assert len(store.list_audit()) >= 3

def test_invalid_source_url_rejected(tmp_path):
    store = Store(tmp_path / "test.db")
    with pytest.raises(ValueError):
        store.add_report("+****1234", "Spam", "Test", "javascript:alert(1)")

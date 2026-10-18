import pytest
from phonesleuth.phone import analyze_number

def test_parse_valid_pk_number():
    result = analyze_number("+923001234567")
    assert result["country_code"] == 92
    assert result["international_format"].startswith("+92")
    assert "does not identify" in result["note"]

def test_blank_number_rejected():
    with pytest.raises(ValueError):
        analyze_number("")

def test_invalid_text_rejected():
    with pytest.raises(ValueError):
        analyze_number("not-a-number")

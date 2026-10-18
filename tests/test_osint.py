import pytest
from phonesleuth.osint import build_search_links

def test_builds_public_links():
    results = build_search_links("+923001234567")
    assert len(results) == 3
    assert all(x["url"].startswith("https://") for x in results)

def test_blank_query_rejected():
    with pytest.raises(ValueError):
        build_search_links("")

def test_long_query_rejected():
    with pytest.raises(ValueError):
        build_search_links("x" * 201)

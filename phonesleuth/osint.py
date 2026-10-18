"""Safe public-web search link builder. Does not scrape sites or access private data."""
from urllib.parse import quote_plus

ENGINES = {
    "Google": "https://www.google.com/search?q={q}",
    "Bing": "https://www.bing.com/search?q={q}",
    "DuckDuckGo": "https://duckduckgo.com/?q={q}",
}

def build_search_links(query: str) -> list[dict]:
    query = (query or "").strip()
    if not query:
        raise ValueError("Enter a public search query.")
    if len(query) > 200:
        raise ValueError("Query is too long (maximum 200 characters).")
    q = quote_plus(query)
    return [{"engine": name, "url": template.format(q=q),
             "note": "Opens a public search engine; results may be incomplete or inaccurate."}
            for name, template in ENGINES.items()]

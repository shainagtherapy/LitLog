import os
import requests

GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")



def googlebooks_search(q: str, max_results: int =10):
    if not q:
        return []
    
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": q,
        "printType": "books",
        "orderBy": "relevance",
        "maxResults": max_results,
        "fields": "items(volumeInfo/title,volumeInfo/authors,volumeInfo/imageLinks/thumnail)",
        "key": GOOGLE_BOOKS_API_KEY,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    items = (r.json().get("items") or [])
    results = []
    for it in items:
        vi = it.get("volumeInfo", {}) or {}
        title = vi.get("title")
        authors = ", ".join(vi.get("authors", []))
        thumb = (vi.get("imageLinks") or {}).get("thumbnail")

        if thumb and thumb.startswith("http:"):
            thumb = "http:" + thumb[5:]
        results.append({"title": title, "author": authors, "image_url": thumb})
    return results

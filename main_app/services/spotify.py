import os, time, base64, requests

_TOKEN_CACHE = {"access_token": None, "expires_at": 0}

def _get_spotify_token():
    # Client Credentials flow (no user scopes needed for catalog metadata).
    if _TOKEN_CACHE["access_token"] and _TOKEN_CACHE["expires_at"] > time.time() + 60:
        return _TOKEN_CACHE["access_token"]

    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise RuntimeError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your environment.")

    token_url = "https://accounts.spotify.com/api/token"
    creds_b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    headers = {"Authorization": f"Basic {creds_b64}"}
    data = {"grant_type": "client_credentials"}

    resp = requests.post(token_url, headers=headers, data=data, timeout=10)

    try:
        payload = resp.json()
    except ValueError:
        payload = {"error": f"Non-JSON token response (status {resp.status_code})"}

    if resp.status_code != 200:
        raise RuntimeError(f"Spotify token error {resp.status_code}: {payload}")

    token = payload.get("access_token")
    if not token:
        raise RuntimeError(f"Token response missing access_token: {payload}")

    _TOKEN_CACHE["access_token"] = token
    _TOKEN_CACHE["expires_at"] = time.time() + int(payload.get("expires_in", 3600))
    return token



def _spotify_search_audiobooks(q, market="US", limit=10):
    # Return list of dicts: title, author, image_url from Spotify Search (type=audiobook).
    token = _get_spotify_token()
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": q, "type": "audiobook", "market": market, "limit": limit}

    r = requests.get(url, headers=headers, params=params, timeout=10)       # *********** requests error on Heroku
    r.raise_for_status()
    data = r.json()
    items = (data.get("audiobooks") or {}).get("items", [])
    results = []
    for it in items:
        title = it.get("name")
        authors = ", ".join(a.get("name") for a in it.get("authors", []))
        images = it.get("images") or []
        image_url = images[-1]["url"] if images else None
        results.append({"title": title, "author": authors, "image_url": image_url})
    return results
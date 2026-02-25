# `spotify.py` – Spotify Data Retrieval & Processing

**File path**: `/app/cloned_repos/spotifydata/spotify.py`

The `spotify` module is the single point of interaction with the Spotify Web API.  
It authenticates a user, pulls data (liked songs, recent plays, albums, artists), and
converts that raw API payload into a set of dictionaries that can be stored in a
PostgreSQL database.

> **Used by**  
> * `pages.cred` – the login page that triggers data collection.  
> * `pages.cred.fetch_data` – the function that orchestrates the whole data‑fetching
>   pipeline.

---

## 1. Global configuration

```python
load_dotenv()                     # Load .env variables into os.environ

username = "Srivatsan Thiruvengadam"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played user-library-read'
```

* **Why these exist**  
  * `dotenv.load_dotenv()` pulls the Spotify client credentials from a `.env` file,
    keeping secrets out of source control.  
  * `client_id` / `client_secret` are required by the Spotify OAuth flow.  
  * `redirect_uri` is the callback URL that Spotify redirects to after authentication.  
  * `scope` declares the permissions the application needs (recently played tracks
    and the user’s library).

---

## 2. Public API

| Function | Purpose | Parameters | Returns | Notes |
|----------|---------|------------|---------|-------|
| `spotify_init(spotify_username)` | Authenticates a user and returns an OAuth token. | `spotify_username` – Spotify username (string) | `token` – OAuth token string | Uses `spotipy.util.prompt_for_user_token`. |
| `recent_songs(token)` | Retrieves the last 50 tracks the user played. | `token` – OAuth token | List of track items (raw Spotify dicts) | Adds an `added_at` field equal to `played_at`. |
| `get_liked_songs(token)` | Pulls all tracks the user has saved to their library. | `token` | List of track items (raw Spotify dicts) | Handles pagination (`limit=50`). |
| `get_albums(token, album_ids)` | Fetches album details for a list of album IDs. | `token`, `album_ids` (list of strings) | List of album dicts | Batches requests in groups of 20. |
| `get_artists(token, artist_ids)` | Fetches artist details for a list of artist IDs. | `token`, `artist_ids` (list of strings) | List of artist dicts | Batches requests in groups of 50. |
| `process_liked_songs(liked_songs)` | Normalises liked‑song data into a flat dictionary list. | `liked_songs` – list of raw track dicts | `songs_dict` – list of dicts | Each artist ID becomes a separate entry (one row per artist). |
| `process_albums(albums)` | Normalises album data into a flat dictionary list. | `albums` – list of raw album dicts | `album_dict` – list of dicts | Each genre and artist becomes a separate row. |
| `process_artists(artists)` | Normalises artist data into a flat dictionary list. | `artists` – list of raw artist dicts | `artist_dict` – list of dicts | Each genre becomes a separate row. |

> **All processing functions** return a *list of dictionaries* that can be fed directly
> into the PostgreSQL helper functions (`add_liked_songs_dict`, `add_albums_dict`,
> `add_artists_dict`).

---

## 3. How the module is used in the application

### 3.1. Authentication flow

```python
# pages/cred.py
token = spotify.spotify_init(username_input_value)
```

The `spotify_init` function is called with the username entered by the user.  
It opens a browser window for the user to grant permissions and returns an OAuth
token that is then reused for all subsequent API calls.

### 3.2. Fetching and storing liked songs

```python
songs = spotify.get_liked_songs(token)
songs_dict = spotify.process_liked_songs(songs)
postgres.add_liked_songs_dict(songs_dict, 'liked_songs')
```

* `get_liked_songs` pulls the entire library (paginated).  
* `process_liked_songs` flattens the nested structure into a list of rows.  
* The resulting list is inserted into the `liked_songs` table.

### 3.3. Fetching and storing recent plays

```python
recent = spotify.recent_songs(token)
recent_dict = spotify.process_liked_songs(recent)
postgres.add_liked_songs_dict(recent_dict, 'recents')
```

The same processing logic is reused for recent tracks, storing them in a separate
table.

### 3.4. Fetching and storing artists & albums

```python
# Collect unique artist and album IDs from the master song list
artist_ids = list(set([s['artists'] for s in master_songs_dict]))
album_ids  = list(set([s['album']   for s in master_songs_dict]))

artists = spotify.get_artists(token, artist_ids)
artists_dict = spotify.process_artists(artists)
postgres.add_artists_dict(artists_dict)

albums = spotify.get_albums(token, album_ids)
albums_dict = spotify.process_albums(albums)
postgres.add_albums_dict(albums_dict)
```

The module’s batch‑request helpers (`get_artists`, `get_albums`) reduce the number
of HTTP calls by grouping IDs into the maximum payload size allowed by the
Spotify API (50 artists / 20 albums per request).

---

## 4. Dependencies

| External | Reason | File path |
|----------|--------|-----------|
| `dotenv.load_dotenv` | Load environment variables (`CLIENT_ID`, `CLIENT_SECRET`). | `/app/cloned_repos/spotifydata/spotify.py` |
| `os` | Access `os.getenv` for credentials. | `/app/cloned_repos/spotifydata/spotify.py` |
| `pandas` | Imported but not used directly in this module; likely a leftover from earlier code. | `/app/cloned_repos/spotifydata/spotify.py` |
| `spotipy` | Official Spotify Web API client. Provides `Spotify` and `util.prompt_for_user_token`. | `/app/cloned_repos/spotifydata/spotify.py` |

> **Missing relationships** – None. All dependencies are explicitly listed in the
> `external_dependencies` field.

---

## 5. Design notes

* **Token handling** – The module does not cache the token; each call to
  `spotify_init` will prompt the user again. In a production system you might
  persist the token in a session or database.
* **Batching** – `get_albums` and `get_artists` manually split the ID lists into
  chunks to stay within Spotify’s request limits. This logic is reused by
  `pages.cred.fetch_data`.
* **Data flattening** – The processing functions intentionally duplicate rows
  for each artist/genre to simplify relational storage. For example, a single
  liked song with two artists results in two rows in the `liked_songs` table.
* **Error handling** – The module contains no explicit error handling; any
  exceptions from the Spotify API will propagate to the caller. The calling
  code (`pages.cred.fetch_data`) assumes successful execution.

---

## 6. Example usage

```python
from spotify import (
    spotify_init,
    get_liked_songs,
    process_liked_songs,
    get_artists,
    process_artists,
    get_albums,
    process_albums,
)

# 1. Authenticate
token = spotify_init("my_spotify_username")

# 2. Pull data
liked = get_liked_songs(token)
recent = recent_songs(token)

# 3. Normalise
liked_dict = process_liked_songs(liked)
recent_dict = process_liked_songs(recent)

# 4. Store (pseudo‑code)
postgres.add_liked_songs_dict(liked_dict, 'liked_songs')
postgres.add_liked_songs_dict(recent_dict, 'recents')

# 5. Fetch artists & albums
artist_ids = list(set([s['artists'] for s in liked_dict]))
album_ids  = list(set([s['album']   for s in liked_dict]))

artists = get_artists(token, artist_ids)
albums  = get_albums(token, album_ids)

postgres.add_artists_dict(process_artists(artists))
postgres.add_albums_dict(process_albums(albums))
```

---

## 7. Summary

`spotify.py` is the core data‑access layer for the Spotify Analyzer application.  
It abstracts away the Spotify OAuth flow, paginated API calls, and data
normalisation, providing a clean set of functions that the UI layer (`pages.cred`)
can call to populate the local PostgreSQL database. All interactions are
documented above, and the module’s dependencies are explicitly declared.
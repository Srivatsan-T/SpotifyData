# `spotify.py` – Spotify Data Retrieval & Processing

**File path:** `/app/cloned_repos/spotifydata/spotify.py`  
**Module name:** `spotify`  
**Purpose:**  
This module is the single point of interaction with the Spotify Web API.  
It authenticates a user, pulls raw data (liked songs, recent plays, albums, artists), and
converts that data into a flat list of dictionaries that can be inserted into a PostgreSQL
database by the `postgres` module.

---

## 1. External Dependencies

| Dependency | Why it exists | What functionality is used |
|------------|---------------|-----------------------------|
| `dotenv.load_dotenv` | Loads environment variables from a `.env` file. | `load_dotenv()` is called at import time to populate `os.getenv`. |
| `os` | Access to environment variables. | `os.getenv("CLIENT_ID")`, `os.getenv("CLIENT_SECRET")`. |
| `pandas` | Imported but not used directly in this module. | No direct usage; likely a leftover import. |
| `spotipy` | Official Spotify Web API client. | All API calls (`spotipy.util.prompt_for_user_token`, `spotipy.Spotify`). |

> **Note:** The module imports `pandas` but never references it. It can be removed without
> affecting functionality.

---

## 2. Module‑level Configuration

```python
load_dotenv()                     # Load .env file
username = "Srivatsan Thiruvengadam"   # Hard‑coded default (unused)
client_id = os.getenv("CLIENT_ID")      # Spotify client ID
client_secret = os.getenv("CLIENT_SECRET")  # Spotify client secret
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played user-library-read'
```

- **`client_id` / `client_secret`** are required for OAuth authentication.
- **`redirect_uri`** must match the URI registered in the Spotify developer dashboard.
- **`scope`** defines the permissions requested: reading recent plays and the user’s library.

---

## 3. Public API

| Function | Purpose | Key Steps | Return Value |
|----------|---------|-----------|--------------|
| `spotify_init(spotify_username)` | Authenticates a user and returns an OAuth token. | Calls `spotipy.util.prompt_for_user_token` with the configured scope and credentials. | `token` (string) |
| `recent_songs(token)` | Retrieves the user’s most recent 50 plays. | `sp.current_user_recently_played(limit=50)`. Adds an `added_at` field equal to `played_at`. | List of raw item dicts (`user_recent['items']`). |
| `get_liked_songs(token)` | Retrieves all songs the user has saved. | Paginated loop (`offset`, `limit=50`) until `next` is `None`. | List of raw item dicts. |
| `get_albums(token, album_ids)` | Fetches album details for a list of album IDs. | Batches requests in groups of 20 (Spotify API limit). | List of album dicts. |
| `get_artists(token, artist_ids)` | Fetches artist details for a list of artist IDs. | Batches requests in groups of 50. | List of artist dicts. |
| `process_liked_songs(liked_songs)` | Normalises liked‑song data into a flat dictionary per artist. | For each song, creates a dict with fields: `song_id`, `song_name`, `added_at`, `album`, `popularity`, `preview_url`, `duration_ms`. Then iterates over each artist in the song, adding an `artists` key and appending a copy of the dict. | List of dicts ready for DB insertion. |
| `process_albums(albums)` | Normalises album data into a flat dictionary per genre/artist. | For each album, creates a dict with `album_id`, `album_name`, `popularity`. Then for each genre and each artist, appends a copy of the dict with `genres` or `artists` set. | List of dicts ready for DB insertion. |
| `process_artists(artists)` | Normalises artist data into a flat dictionary per genre. | For each artist, creates a dict with `artist_id`, `artist_name`, `popularity`, `followers`. Then for each genre, appends a copy of the dict with `genres` set. | List of dicts ready for DB insertion. |

> **Important:**  
> - `process_liked_songs` creates a separate entry for each artist in a song; this is intentional to preserve the many‑to‑many relationship.  
> - `process_albums` and `process_artists` similarly duplicate rows for each genre or artist.

---

## 4. How the Module Is Used

The `spotify` module is imported by **`pages.cred`** (and its helper `fetch_data` function).  
The typical flow in `pages.cred.fetch_data` is:

```python
token = spotify.spotify_init(username)          # OAuth token
songs = spotify.get_liked_songs(token)          # Raw liked songs
songs_dict = spotify.process_liked_songs(songs) # Normalised dicts
# ... store in Postgres via postgres.add_liked_songs_dict

recent = spotify.recent_songs(token)            # Raw recent plays
recent_dict = spotify.process_liked_songs(recent)
# ... store in Postgres via postgres.add_liked_songs_dict

# Gather unique artist and album IDs from the combined song list
artist_ids = list(set([s['artists'] for s in master_songs_dict]))
artists = spotify.get_artists(token, artist_ids)
artists_dict = spotify.process_artists(artists)
postgres.add_artists_dict(artists_dict)

album_ids = list(set([s['album'] for s in master_songs_dict]))
albums = spotify.get_albums(token, album_ids)
albums_dict = spotify.process_albums(albums)
postgres.add_albums_dict(albums_dict)
```

Thus, `spotify.py` is the **data source** for the application.  
All downstream modules (`pages.liked_songs`, `pages.recents`, `pages.analytics`, etc.) rely on the
PostgreSQL tables populated by these functions.

---

## 5. Dependencies & Relationships

- **Depends on**: None (only external libraries).  
- **Used by**:  
  - `pages.cred` (module)  
  - `pages.cred.fetch_data` (function)  

No other modules in the codebase import or call functions from `spotify.py`.

---

## 6. Suggested Improvements

| Issue | Recommendation |
|-------|----------------|
| `pandas` is imported but unused | Remove the import to reduce noise. |
| Global variables (`username`, `client_id`, etc.) are defined but not used | Either remove them or document their intended purpose. |
| No docstrings for functions | Add concise docstrings explaining parameters, return values, and side‑effects. |
| Hard‑coded `username` | Remove or make it optional; the function already accepts a username argument. |
| Repeated code in `process_*` functions (copying dicts) | Consider refactoring to a helper that handles duplication. |

---

## 7. Quick Reference

```python
# Authenticate
token = spotify.spotify_init("my_spotify_username")

# Get data
liked = spotify.get_liked_songs(token)
recent = spotify.recent_songs(token)
albums = spotify.get_albums(token, album_ids)
artists = spotify.get_artists(token, artist_ids)

# Process for DB
liked_dict = spotify.process_liked_songs(liked)
recent_dict = spotify.process_liked_songs(recent)
albums_dict = spotify.process_albums(albums)
artists_dict = spotify.process_artists(artists)
```

These processed dictionaries are then passed to the `postgres` module for insertion into the
database.

---

**End of documentation for `spotify.py`.**
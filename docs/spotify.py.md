# `spotify.py` – Core Spotify Data Retrieval Module  
**File path:** `/app/cloned_repos/spotify_data/spotify.py`

The `spotify` module is the single point of contact between the application and the Spotify Web API.  
It handles authentication, data fetching, and data transformation so that the rest of the codebase can work with clean, database‑ready structures.

> **Used by**  
> - `pages.cred` (main login page)  
> - `pages.cred.fetch_data` (data ingestion routine)

---

## 1. Module‑level Imports & Configuration

| Import | Purpose | Notes |
|--------|---------|-------|
| `spotipy` | Official Spotify Web API client | Provides `Spotify` and `util.prompt_for_user_token` |
| `pandas as pd` | Data manipulation | Only used in `pages.cred.fetch_data` to build DataFrames |
| `os` | Environment variable access | Reads `CLIENT_ID` & `CLIENT_SECRET` |
| `dotenv.load_dotenv` | Loads `.env` file | Called immediately on import to populate `os.environ` |

```python
import spotipy
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
```

### Global constants

```python
username = "Srivatsan Thiruvengadam"   # Not used by the module itself
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played user-library-read'
```

- **Why these exist** – They provide the credentials and permissions required by the Spotify API.  
- **What they enable** – `spotipy.util.prompt_for_user_token` needs `client_id`, `client_secret`, `redirect_uri`, and `scope` to request an OAuth token.

---

## 2. Public API

| Function | Signature | Purpose | Key Steps |
|----------|-----------|---------|-----------|
| `spotify_init(spotify_username)` | `def spotify_init(spotify_username):` | Authenticates a user and returns an OAuth token. | Calls `spotipy.util.prompt_for_user_token` with the global credentials. |
| `recent_songs(token)` | `def recent_songs(token):` | Retrieves the last 50 songs the user played. | Uses `spotipy.Spotify(token).current_user_recently_played(limit=50)` and normalises the `added_at` field. |
| `get_liked_songs(token)` | `def get_liked_songs(token):` | Pulls all songs the user has saved to their library. | Loops over paginated results (`offset`, `limit=50`) until `next` is `None`. |
| `get_albums(token, album_ids)` | `def get_albums(token, album_ids):` | Batch‑fetches album objects for a list of IDs. | Requests up to 20 IDs per call (`sp.albums`). |
| `get_artists(token, artist_ids)` | `def get_artists(token, artist_ids):` | Batch‑fetches artist objects for a list of IDs. | Requests up to 50 IDs per call (`sp.artists`). |
| `process_liked_songs(liked_songs)` | `def process_liked_songs(liked_songs):` | Transforms raw liked‑song data into a flat list of dictionaries suitable for DB insertion. | Extracts song metadata, album ID, popularity, preview URL, duration, and each artist ID. |
| `process_albums(albums)` | `def process_albums(albums):` | Normalises album data into a list of dictionaries. | For each album, emits a row per genre and per artist. |
| `process_artists(artists)` | `def process_artists(artists):` | Normalises artist data into a list of dictionaries. | For each artist, emits a row per genre. |

> **Note** – All `process_*` functions return a *list of dictionaries*; each dictionary contains only scalar values (no nested lists).  
> This format matches the column layout expected by the PostgreSQL helper functions in `postgres.py`.

---

## 3. Detailed Function Explanations

### 3.1 `spotify_init`

```python
def spotify_init(spotify_username):
    token = spotipy.util.prompt_for_user_token(
        username=spotify_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )
    return token
```

- **Why** – The application needs an OAuth token to make authenticated API calls.  
- **What it relies on** – `spotipy.util.prompt_for_user_token` handles the OAuth flow (including opening a browser window).  
- **Usage** – Called once per user session (e.g., in `pages.cred.fetch_data`). The returned token is passed to all other functions.

### 3.2 `recent_songs`

```python
def recent_songs(token):
    sp = spotipy.Spotify(token)
    user_recent = sp.current_user_recently_played(limit=50)
    for i in user_recent['items']:
        i['added_at'] = i['played_at']
    return user_recent['items']
```

- **Why** – Provides a quick snapshot of what the user has listened to recently.  
- **What it relies on** – `sp.current_user_recently_played` from Spotipy.  
- **Usage** – In `pages.cred.fetch_data`, the returned list is processed by `process_liked_songs` and stored in the `recents` table.

### 3.3 `get_liked_songs`

```python
def get_liked_songs(token):
    sp = spotipy.Spotify(token)
    lim = 50
    off = 0
    songs = []
    next = 'not none'
    while next is not None:
        liked_songs = sp.current_user_saved_tracks(offset=off, limit=lim)
        for i in liked_songs['items']:
            songs.append(i)
        off += lim
        next = liked_songs['next']
    return songs
```

- **Why** – The user’s entire library may contain thousands of tracks; pagination is required.  
- **What it relies on** – `sp.current_user_saved_tracks` returns a paginated response with a `next` URL.  
- **Usage** – The raw list is passed to `process_liked_songs` and inserted into the `liked_songs` table.

### 3.4 `get_albums`

```python
def get_albums(token, album_ids):
    sp = spotipy.Spotify(token)
    albums = []
    number_of_ids = len(album_ids)
    if album_ids:
        for i in range(int(number_of_ids/20)):
            albums.extend(sp.albums(album_ids[20*i:20*i+20])['albums'])
        albums.extend(sp.albums(album_ids[int(number_of_ids/20)*20:])['albums'])
    return albums
```

- **Why** – Spotify limits batch requests to 20 IDs; this helper splits the list accordingly.  
- **What it relies on** – `sp.albums` returns a dictionary with an `albums` key.  
- **Usage** – After deduplicating album IDs, `pages.cred.fetch_data` calls this to fetch new album data, then processes it with `process_albums`.

### 3.5 `get_artists`

```python
def get_artists(token, artist_ids):
    sp = spotipy.Spotify(token)
    artists = []
    number_of_ids = len(artist_ids)
    if artist_ids:
        for i in range(int(number_of_ids/50)):
            artists.extend(sp.artists(artist_ids[50*i:50*i+50])['artists'])
        artists.extend(sp.artists(artist_ids[int(number_of_ids/50)*50:])['artists'])
    return artists
```

- **Why** – Spotify allows up to 50 IDs per batch.  
- **What it relies on** – `sp.artists` returns a dictionary with an `artists` key.  
- **Usage** – Called by `pages.cred.fetch_data` to pull new artist data, then processed with `process_artists`.

### 3.6 `process_liked_songs`

```python
def process_liked_songs(liked_songs):
    number_of_songs = len(liked_songs)
    songs_dict = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['song_id'] = liked_songs[i]['track']['id']
        temp_dict['song_name'] = liked_songs[i]['track']['name']
        temp_dict['added_at'] = liked_songs[i]['added_at']
        temp_dict['album'] = liked_songs[i]['track']['album']['id']
        temp_dict['popularity'] = liked_songs[i]['track']['popularity']
        temp_dict['preview_url'] = liked_songs[i]['track']['preview_url']
        temp_dict['duration_ms'] = liked_songs[i]['track']['duration_ms']

        for artist in liked_songs[i]['track']['artists']:
            temp_dict['artists'] = artist['id']
            songs_dict.append(temp_dict.copy())
    return songs_dict
```

- **Why** – The raw Spotify response nests many fields; the database expects a flat row per artist.  
- **What it relies on** – The structure of the `liked_songs` list returned by `get_liked_songs`.  
- **Usage** – The resulting list is fed to `postgres.add_liked_songs_dict`.

### 3.7 `process_albums`

```python
def process_albums(albums):
    number_of_songs = len(albums)
    album_dict = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['album_id'] = albums[i]['id']
        temp_dict['album_name'] = albums[i]['name']
        temp_dict['popularity'] = albums[i]['popularity']

        for genre in albums[i]['genres']:
            temp_dict['genres'] = genre
            album_dict.append(temp_dict.copy())
        if not albums[i]['genres']:
            temp_dict['genres'] = 'N.A'
        for artist in albums[i]['artists']:
            temp_dict['artists'] = artist['id']
            album_dict.append(temp_dict.copy())
    return album_dict
```

- **Why** – Albums can belong to multiple genres and have multiple artists; each combination becomes a separate row.  
- **What it relies on** – The `genres` and `artists` lists inside each album object.  
- **Usage** – The flattened list is inserted into the `album` table via `postgres.add_albums_dict`.

### 3.8 `process_artists`

```python
def process_artists(artists):
    number_of_songs = len(artists)
    artist_dict = []
    for i in range(number_of_songs):
        temp_dict = {}
        temp_dict['artist_id'] = artists[i]['id']
        temp_dict['artist_name'] = artists[i]['name']
        temp_dict['popularity'] = artists[i]['popularity']
        temp_dict['followers'] = artists[i]['popularity']   # likely a bug – should be artists[i]['followers']

        for genre in artists[i]['genres']:
            temp_dict['genres'] = genre
            artist_dict.append(temp_dict.copy())
        if not artists[i]['genres']:
            temp_dict['genres'] = 'N.A'
    return artist_dict
```

- **Why** – Normalises artist data for the `artist` table.  
- **What it relies on** – The `genres` list inside each artist object.  
- **Usage** – Inserted into the `artist` table via `postgres.add_artists_dict`.

---

## 4. Interaction with the Rest of the Codebase

### 4.1 `pages.cred.fetch_data`

```python
token = spotify.spotify_init(username)
songs = spotify.get_liked_songs(token)
songs_dict = spotify.process_liked_songs(songs)
...
artists = spotify.get_artists(token, artist_ids_spotify)
artists = spotify.process_artists(artists)
...
albums = spotify.get_albums(token, album_ids_spotify)
albums = spotify.process_albums(albums)
```

- **Role** – Orchestrates the entire ingestion pipeline: authentication → data retrieval → transformation → database insertion.  
- **Dependencies** – Relies on `spotify` for all API interactions and data shaping; relies on `postgres` for persistence; relies on `pandas` for DataFrame manipulation.

### 4.2 `pages.cred` (Login page)

- Imports `spotify` to expose the `spotify_init` function to the callback that triggers data fetching.  
- The callback `button_on_clicked` calls `fetch_data(value)` after a successful login.

---

## 5. Summary of Dependencies

| Dependency | Why it exists | What it provides |
|------------|---------------|-------------------|
| `dotenv.load_dotenv` | Loads environment variables from a `.env` file | Makes `CLIENT_ID` & `CLIENT_SECRET` available |
| `os` | Access to environment variables | `os.getenv` |
| `spotipy` | Official Spotify client | OAuth flow, API endpoints |
| `pandas` | DataFrame creation (used in `pages.cred.fetch_data`) | `pd.DataFrame.from_dict` |

> **No other external modules** are imported by `spotify.py`.  
> The module has no internal dependencies (`depends_on` is empty) and is only used by `pages.cred` and its `fetch_data` helper.

---

## 6. Things to Watch Out For

- **Hard‑coded username** – The global `username` variable is never used; authentication is performed per‑user via `spotify_init`.  
- **Potential bug** – In `process_artists`, `followers` is set to `artists[i]['popularity']` instead of the actual follower count.  
- **Batch limits** – `get_albums` and `get_artists` respect Spotify’s API limits (20 and 50 IDs per request).  
- **Data duplication** – `process_liked_songs` emits one row per artist; downstream code must deduplicate or handle duplicates appropriately.  

---

## 7. Quick Reference

```python
# Authenticate
token = spotify.spotify_init('my_spotify_username')

# Fetch data
liked = spotify.get_liked_songs(token)
recent = spotify.recent_songs(token)
albums = spotify.get_albums(token, album_ids)
artists = spotify.get_artists(token, artist_ids)

# Process for DB
liked_rows = spotify.process_liked_songs(liked)
recent_rows = spotify.process_liked_songs(recent)
album_rows = spotify.process_albums(albums)
artist_rows = spotify.process_artists(artists)
```

These processed rows can then be passed to the PostgreSQL helper functions (`add_liked_songs_dict`, `add_albums_dict`, `add_artists_dict`) for persistence.  

---
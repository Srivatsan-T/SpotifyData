# `spotify` Module  
**File:** `/app/cloned_repos/spotifydata/spotify.py`

The `spotify` module is the single point of interaction with the Spotify Web API.  
It authenticates a user, pulls data (liked songs, recent plays, albums, artists) and
provides helper functions that transform the raw API responses into dictionaries
ready for persistence in the PostgreSQL database.

> **Note** – The module contains no docstrings; all explanations are derived from the
> source code and the relationships listed in the evidence.

---

## 1. External Dependencies

| Dependency | Purpose |
|------------|---------|
| `dotenv.load_dotenv` | Loads environment variables from a `.env` file. |
| `os` | Reads the `CLIENT_ID` and `CLIENT_SECRET` environment variables. |
| `pandas` | Used only in `pages.cred.fetch_data` to convert lists of dicts into a DataFrame. |
| `spotipy` | Official Spotify Web API wrapper. Provides `Spotify` client and the
  `util.prompt_for_user_token` helper for OAuth. |

The module imports these at the top of the file:

```python
import spotipy
import pandas as pd
import os
from dotenv import load_dotenv
```

---

## 2. Global Configuration

```python
load_dotenv()                     # Load .env file
username = "Srivatsan Thiruvengadam"  # Hard‑coded default (unused)
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://localhost:7777/callback'
scope = 'user-read-recently-played user-library-read'
```

* **Why** – The OAuth flow requires a client ID, client secret, and a redirect URI.
  The `scope` defines the permissions the application requests from the user.

---

## 3. Core Functions

| Function | Signature | What it does | Dependencies |
|----------|-----------|--------------|--------------|
| `spotify_init` | `def spotify_init(spotify_username)` | Prompts the user for a Spotify OAuth token using the provided username. | `spotipy.util.prompt_for_user_token` |
| `recent_songs` | `def recent_songs(token)` | Retrieves the 50 most recent songs the user has played. | `spotipy.Spotify` |
| `get_liked_songs` | `def get_liked_songs(token)` | Retrieves all songs the user has added to their library (paginated). | `spotipy.Spotify` |
| `get_albums` | `def get_albums(token, album_ids)` | Batch‑fetches album details for a list of album IDs (max 20 per request). | `spotipy.Spotify` |
| `get_artists` | `def get_artists(token, artist_ids)` | Batch‑fetches artist details for a list of artist IDs (max 50 per request). | `spotipy.Spotify` |
| `process_liked_songs` | `def process_liked_songs(liked_songs)` | Transforms raw liked‑song objects into a list of flat dictionaries. Each artist in a song creates a separate dictionary entry. | None |
| `process_albums` | `def process_albums(albums)` | Transforms raw album objects into a list of dictionaries. Each genre and each artist in an album creates a separate entry. | None |
| `process_artists` | `def process_artists(artists)` | Transforms raw artist objects into a list of dictionaries. Each genre creates a separate entry. | None |

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

* **Why** – The rest of the module requires an OAuth token to make authenticated API calls.
* **What** – Returns a string token that can be passed to `spotipy.Spotify`.

### 3.2 `recent_songs`

```python
def recent_songs(token):
    sp = spotipy.Spotify(token)
    user_recent = sp.current_user_recently_played(limit=50)
    for i in user_recent['items']:
        i['added_at'] = i['played_at']
    return user_recent['items']
```

* **Why** – The application needs the most recent plays for analytics.
* **What** – Returns a list of item dictionaries; each item contains a `track` key.

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

* **Why** – Users may have hundreds of liked songs; pagination is required.
* **What** – Returns a list of liked‑song objects.

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

* **Why** – The Spotify API allows up to 20 IDs per request; this function batches accordingly.
* **What** – Returns a list of album objects.

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

* **Why** – The API allows up to 50 IDs per request; batching is performed.
* **What** – Returns a list of artist objects.

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

* **Why** – The database schema expects a flat record per song‑artist pair.
* **What** – Produces a list of dictionaries ready for insertion into the `liked_songs`
  table.

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

* **Why** – Albums can belong to multiple genres and have multiple artists; each
  combination is stored as a separate row.
* **What** – Returns a list of dictionaries for the `album` table.

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
        temp_dict['followers'] = artists[i]['popularity']   # likely a bug – should be followers

        for genre in artists[i]['genres']:
            temp_dict['genres'] = genre
            artist_dict.append(temp_dict.copy())
        if not artists[i]['genres']:
            temp_dict['genres'] = 'N.A'
    return artist_dict
```

* **Why** – Normalises artist data for the `artist` table.
* **What** – Produces a list of dictionaries; each genre becomes a separate row.

---

## 4. Integration with the Rest of the Codebase

### 4.1 `pages.cred` (Login & Data Fetch)

* **Imports**  
  ```python
  import spotify
  import postgres
  ```
* **Workflow**  
  1. `spotify.spotify_init(username)` → OAuth token.  
  2. `spotify.get_liked_songs(token)` → raw liked songs.  
  3. `spotify.process_liked_songs(...)` → flat dicts.  
  4. Convert to `pandas.DataFrame`, filter by `added_at`, and insert into PostgreSQL.  
  5. Repeat similar steps for recent songs, artists, and albums.  
  6. Use `postgres` helper functions to create tables, check for existing data, and insert new rows.

* **Why** – The `spotify` module abstracts all API interactions; `pages.cred` focuses on
  orchestration and persistence.

### 4.2 `pages.cred.fetch_data`

* This is a duplicate of the logic in `pages.cred` but defined as a separate function
  for potential reuse. It calls the same `spotify` functions and performs identical
  database operations.

### 4.3 No Other Modules Depend on `spotify`

The evidence shows that only `pages.cred` (and its nested `fetch_data`) use the
`spotify` module. No other modules import or reference it.

---

## 5. Usage Example

```python
# In a Dash callback or a script
import spotify
import postgres

# 1. Authenticate
token = spotify.spotify_init("my_spotify_username")

# 2. Pull data
liked = spotify.get_liked_songs(token)
recent = spotify.recent_songs(token)

# 3. Process
liked_dicts = spotify.process_liked_songs(liked)
recent_dicts = spotify.process_liked_songs(recent)

# 4. Persist
postgres.create_liked_songs_table()
postgres.add_liked_songs_dict(liked_dicts, 'liked_songs')
```

---

## 6. Summary of Relationships

| Module | Depends on | Used by |
|--------|------------|---------|
| `spotify` | `dotenv`, `os`, `pandas`, `spotipy` | `pages.cred`, `pages.cred.fetch_data` |
| `pages.cred` | `spotify`, `postgres` | – |
| `pages.cred.fetch_data` | `spotify`, `postgres` | – |

*No missing relationships are indicated in the evidence.*

---

## 7. Caveats & Observations

* The module contains no docstrings; developers should refer to the code comments
  and the documentation above.
* The `process_artists` function mistakenly copies `popularity` into the
  `followers` field – likely a bug that should be corrected.
* The hard‑coded `username` variable at the top is unused; it can be removed.
* The module does not expose any classes; all functionality is provided via
  standalone functions.

---

### End of Documentation for `spotify.py`
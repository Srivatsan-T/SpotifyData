# `pages.cred` – Spotify Login & Data Ingestion Page

**File path:** `/app/cloned_repos/spotifydata/pages/cred.py`

`pages.cred` is a Dash page that serves as the entry point of the Spotify Analyzer web‑app.  
It presents a login form, fetches the user’s Spotify data, stores it in a PostgreSQL database, and then redirects the user to the tools page.

---

## 1. Module Overview

| Symbol | Type | Description |
|--------|------|-------------|
| `layout` | function | Returns the Dash layout for the login page. |
| `check_date` | function | Parses Spotify timestamps into `datetime` objects. |
| `fetch_data` | function | Orchestrates the whole data‑fetching pipeline: authenticates with Spotify, pulls liked songs, recent plays, artists, and albums, and writes the results to PostgreSQL. |
| `button_on_clicked` | callback | Triggered when the user clicks the **Login** button. Calls `fetch_data` and redirects to `/tools/<username>`. |
| `time_based_calc` | **commented out** callback | Intended for periodic refreshes (currently inactive). |

The module is registered as a Dash page at the root path (`/`) via `dash.register_page`.

---

## 2. Imports & Dependencies

```python
from dash import dcc, callback
from dash.dependencies import Input, Output, State
from dash import html
import dash
import spotify
import postgres
import pandas as pd
from datetime import datetime
```

| Import | Why it exists | Functionality used |
|--------|---------------|--------------------|
| `dash`, `dash.html`, `dash.dcc`, `dash.callback`, `dash.dependencies` | Build the UI and define callbacks. | `html.Div`, `dcc.Input`, `dcc.Button`, `dcc.Location`, `callback`, `Input`, `Output`, `State` |
| `spotify` | Access Spotify API helpers. | `spotify_init`, `get_liked_songs`, `recent_songs`, `get_artists`, `get_albums`, `process_liked_songs`, `process_artists`, `process_albums` |
| `postgres` | Persist data locally. | `create_liked_songs_table`, `create_recent_songs_table`, `create_artist_table`, `create_album_table`, `check_liked_songs`, `add_liked_songs_dict`, `add_artists_dict`, `add_albums_dict`, `select_unique_artists`, `select_unique_albums` |
| `pandas` | Manipulate tabular data before DB insertion. | `pd.DataFrame` |
| `datetime` | Convert ISO timestamps from Spotify. | `datetime.fromisoformat` |

> **Note:** The module has no incoming dependencies (`used_by` is empty). It is only referenced by the Dash app itself.

---

## 3. Page Layout (`layout`)

```python
def layout():
    return html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div([
            html.Div([...], className='left'),
            html.Div([...], className='right')
        ], className='box-form')
    ])
```

* **`dcc.Location`** – Enables programmatic navigation via the callback that updates the `pathname`.
* **Left column** – Displays the app title and description.
* **Right column** – Contains the login form:
  * `dcc.Input` for the Spotify username (`id='username_input'`).
  * `html.Button` to submit (`id='username_submit_button'`).

The layout is rendered automatically by Dash when the user visits `/`.

---

## 4. Helper: `check_date`

```python
def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])
```

* Strips the trailing `Z` from the ISO timestamp returned by Spotify.
* Converts the string to a `datetime` object for comparison with the latest stored `added_at` value.

---

## 5. Core Function: `fetch_data`

```python
def fetch_data(username):
    token = spotify.spotify_init(username)
    ...
```

### 5.1. Authentication
* Calls `spotify.spotify_init(username)` to obtain an OAuth token.

### 5.2. Liked Songs
1. `spotify.get_liked_songs(token)` → raw list of tracks.
2. `spotify.process_liked_songs(songs)` → list of dicts with fields:
   * `song_id`, `song_name`, `added_at`, `album`, `popularity`, `preview_url`, `duration_ms`, `artists`.
3. Convert to a `pandas.DataFrame`.
4. `postgres.create_liked_songs_table()` – ensures the table exists.
5. `postgres.check_liked_songs('liked_songs')` – fetches the most recent `added_at` in the table.
6. If new songs exist (`flag` is `True`), filter the DataFrame to only those added after the stored timestamp.
7. Convert the filtered DataFrame back to a list of dicts and insert via `postgres.add_liked_songs_dict`.

### 5.3. Recent Plays
* Same pipeline as liked songs, but uses `spotify.recent_songs(token)` and stores in the `recents` table.

### 5.4. Artists
1. Extract all artist IDs from the combined liked + recent song list.
2. `spotify.get_artists(token, artist_ids)` fetches artist objects.
3. `postgres.create_artist_table()` – ensures the artist table exists.
4. `postgres.select_unique_artists()` retrieves already stored artist IDs.
5. Filter out duplicates, process with `spotify.process_artists`, and insert via `postgres.add_artists_dict`.

### 5.5. Albums
1. Extract all album IDs from the combined song list.
2. `spotify.get_albums(token, album_ids)` fetches album objects.
3. `postgres.create_album_table()` – ensures the album table exists.
4. `postgres.select_unique_albums()` retrieves already stored album IDs.
5. Filter out duplicates, process with `spotify.process_albums`, and insert via `postgres.add_albums_dict`.

### 5.6. Summary
`fetch_data` is a **side‑effect‑only** function: it does not return a value but writes all new data to the database. It is invoked by the login button callback.

---

## 6. Callback: `button_on_clicked`

```python
@callback(
    Output('url', 'pathname'),
    [Input('username_submit_button', 'n_clicks')],
    [State('username_input', 'value')]
)
def button_on_clicked(n_clicks, value):
    if value == None:
        return '/'
    else:
        fetch_data(value)
        return f'/tools/{value}'
```

* **Trigger:** User clicks the **Login** button.
* **Behavior:**
  * If no username is entered, stay on the login page (`'/'`).
  * Otherwise, call `fetch_data(value)` to populate the database and redirect to `/tools/<username>`.
* **Why the dependency exists:**  
  * The callback needs to read the username (`State`) and update the URL (`Output`).  
  * It relies on `fetch_data` to perform the heavy lifting of data ingestion.

---

## 7. Commented‑Out Callback (`time_based_calc`)

```python
'''
@callback(
    Output('placeholder','children'),
    [Input('interval-component','n_intervals')],
    [State('username_input', 'value')]
)
def time_based_calc(n_intevrals,username):
    fetch_data(username)
'''
```

* Intended for periodic refreshes (e.g., every few minutes) using a Dash `Interval` component.
* Currently inactive; no effect on the running application.

---

## 8. Interaction Flow

1. **User visits `/`** → `layout()` renders the login form.
2. **User enters username** → value stored in `dcc.Input`.
3. **User clicks "Login"** → `button_on_clicked` fires:
   * Calls `fetch_data(username)` → pulls data from Spotify, processes it, and writes to PostgreSQL.
   * Redirects to `/tools/<username>`.
4. **Tools page** (handled by `pages.tools`) greets the user and offers navigation to other pages (`liked`, `recents`, `analytics`).

---

## 9. Summary of Key Points

| Feature | What it does | Where it lives |
|---------|--------------|----------------|
| **Login UI** | Simple form with username input and button | `layout()` |
| **Data ingestion** | Pulls liked songs, recent plays, artists, albums; stores in PostgreSQL | `fetch_data()` |
| **Timestamp handling** | Converts ISO strings to `datetime` for filtering | `check_date()` |
| **Navigation** | Redirects to tools page after successful fetch | `button_on_clicked()` |
| **Dependencies** | `dash`, `spotify`, `postgres`, `pandas`, `datetime` | Imports at top of file |
| **Page registration** | Root path (`/`) | `dash.register_page(__name__, path='/')` |

This module is the gateway that connects the user to the rest of the Spotify Analyzer application by authenticating, fetching, and persisting data. All subsequent pages (`liked_songs`, `recents`, `analytics`, `tools`) rely on the data stored by `fetch_data`.
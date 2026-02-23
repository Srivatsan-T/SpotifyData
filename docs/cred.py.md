# `pages.cred` – User‑Login & Data‑Ingestion Page

**File path**  
`/app/cloned_repos/spotify_data/pages/cred.py`

The `cred` module is the entry point of the Spotify Analyzer web app.  
It registers the root page (`/`) and provides a login form that triggers
the ingestion of a user’s Spotify data into a local PostgreSQL database.

---

## 1. Module Registration

```python
dash.register_page(__name__, path='/')
```

* Registers this module as the root page of the Dash application.
* When the user navigates to `/`, the `layout()` function is rendered.

---

## 2. Layout

```python
def layout():
    return html.Div([
        dcc.Location(id='url', refresh=True),
        html.Div([...], className='box-form')
    ])
```

* **`dcc.Location`** – Forces a page refresh when the URL changes.
* The page is split into two halves:
  * **Left** – A static header with the app title and description.
  * **Right** – A login form:
    * `dcc.Input` for the Spotify username.
    * `html.Button` labeled **Login**.

The layout is purely presentational; all logic is handled by the
callback defined below.

---

## 3. Helper Function – `check_date`

```python
def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])
```

* Converts a Spotify ISO‑8601 timestamp (e.g. `"2023-07-01T12:34:56Z"`)
  into a Python `datetime` object.
* The trailing `"Z"` is stripped before parsing.
* Used to filter songs that were added after the most recent entry in the
  database.

---

## 4. Core Data‑Ingestion – `fetch_data`

```python
def fetch_data(username):
    token = spotify.spotify_init(username)
    ...
```

### 4.1. Flow Overview

| Step | Action | Dependencies |
|------|--------|--------------|
| 1 | **Authenticate** | `spotify.spotify_init` |
| 2 | **Fetch liked songs** | `spotify.get_liked_songs` |
| 3 | **Process liked songs** | `spotify.process_liked_songs` |
| 4 | **Store in DB** | `postgres.create_liked_songs_table`, `postgres.check_liked_songs`, `postgres.add_liked_songs_dict` |
| 5 | **Fetch recent songs** | `spotify.recent_songs` |
| 6 | **Process recent songs** | `spotify.process_liked_songs` |
| 7 | **Store in DB** | `postgres.create_recent_songs_table`, `postgres.check_liked_songs`, `postgres.add_liked_songs_dict` |
| 8 | **Merge song lists** | Python `set` |
| 9 | **Fetch & store artists** | `spotify.get_artists`, `postgres.create_artist_table`, `postgres.select_unique_artists`, `spotify.process_artists`, `postgres.add_artists_dict` |
| 10 | **Fetch & store albums** | `spotify.get_albums`, `postgres.create_album_table`, `postgres.select_unique_albums`, `spotify.process_albums`, `postgres.add_albums_dict` |

#### Detailed Steps

1. **Authentication**  
   `spotify.spotify_init(username)` returns an OAuth token for the user.

2. **Liked Songs**  
   * `spotify.get_liked_songs(token)` pulls all saved tracks.  
   * `spotify.process_liked_songs` normalises the data into a list of
     dictionaries (one per artist per track).  
   * A Pandas `DataFrame` is created only to filter by `added_at`.  
   * `postgres.check_liked_songs('liked_songs')` returns the most recent
     `added_at` timestamp in the table.  
   * New entries (after that timestamp) are inserted via
     `postgres.add_liked_songs_dict`.

3. **Recent Songs** – analogous to liked songs but uses the
   `recent_songs` table.

4. **Artists**  
   * Extract unique artist IDs from the merged song list.  
   * `spotify.get_artists` fetches artist details in batches of 50.  
   * Existing artist IDs are filtered out using
     `postgres.select_unique_artists`.  
   * New artists are processed (`spotify.process_artists`) and stored
     (`postgres.add_artists_dict`).

5. **Albums** – similar to artists but uses `spotify.get_albums` and
   `postgres.add_albums_dict`.

### 4.2. Why Each Dependency Exists

| Dependency | Reason |
|------------|--------|
| `spotify` | Provides OAuth, API calls, and data normalisation. |
| `postgres` | Handles table creation, querying, and bulk inserts. |
| `pandas` | Used temporarily to filter rows by `added_at`. |
| `datetime` | Parses ISO timestamps for comparison. |

---

## 5. Callback – `button_on_clicked`

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

* Triggered when the **Login** button is clicked.
* **Input**: button click count.  
* **State**: current value of the username input field.
* **Output**: updates the browser’s pathname, causing a redirect.
* If no username is supplied, the user stays on the login page.
* Otherwise, `fetch_data` is called to ingest data, then the user is
  redirected to `/tools/<username>`.

---

## 6. Commented‑Out Callback

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

* Appears to be an alternative, time‑based ingestion trigger.
* Currently inactive (enclosed in triple quotes).
* If enabled, it would periodically call `fetch_data` for the current
  username.

---

## 7. External Dependencies

| Library | Purpose |
|---------|---------|
| `dash` | Core Dash framework. |
| `dash.callback` | Decorator for callbacks. |
| `dash.dcc` | Dash Core Components (`Location`, `Input`, `Button`). |
| `dash.dependencies` | `Input`, `Output`, `State` objects. |
| `dash.html` | HTML component wrappers. |
| `datetime.datetime` | ISO timestamp parsing. |
| `pandas` | Temporary DataFrame for filtering. |

---

## 8. Interaction with Other Modules

* **`pages.tools`** – After successful login, the user is redirected
  to `/tools/<username>`, which displays a welcome message.
* **`pages.liked_songs`**, **`pages.recents`**, **`pages.analytics`** –  
  These pages query the tables populated by `fetch_data` to display
  the user’s liked songs, recent plays, and analytics.  
  They import `postgres` directly; `cred` does not import them.

---

## 9. Summary

`pages.cred` is the gateway to the Spotify Analyzer:

1. **User enters Spotify username** → **Login button** →  
2. **`button_on_clicked`** triggers **`fetch_data`** →  
3. **Data is fetched, processed, and stored** in PostgreSQL →  
4. **User is redirected** to the tools page.

The module relies on the `spotify` API wrapper for data retrieval and
normalisation, and on the `postgres` helper for database interactions.
All UI components are built with Dash, and the module is registered as
the root page of the application.
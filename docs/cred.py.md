# `pages.cred` – Login & Data‑Fetching Page

**File path:** `/app/cloned_repos/spotifydata/pages/cred.py`

The `cred` module implements the root page of the Dash application.  
It presents a login form, obtains a Spotify access token, pulls the user’s
liked and recently played tracks, and stores them in a PostgreSQL database.
After a successful login the user is redirected to the *Tools* page.

---

## 1.  Module Registration

```python
dash.register_page(__name__, path='/')
```

*Why it exists* – Registers this module as the root page (`/`) of the Dash
application.  
*What it does* – Makes the `layout()` function available as the page
content and the callbacks defined in this file active.

---

## 2.  Imports & Dependencies

| Import | Purpose | File Path Reference |
|--------|---------|---------------------|
| `dash` | Core Dash functionality (e.g., `register_page`) | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `dash.html` | HTML components (`Div`, `H1`, `Input`, etc.) | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `dash.dcc` | Dash Core Components (`Location`, `Input`) | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `dash.callback` | Decorator for callbacks | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `dash.dependencies` (`Input`, `Output`, `State`) | Callback wiring | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `datetime.datetime` | Convert timestamp strings to `datetime` objects | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `pandas` | Build DataFrames for intermediate processing | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `spotify` | Wrapper around the Spotipy API | `/app/cloned_repos/spotifydata/pages/cred.py` |
| `postgres` | Database helper functions | `/app/cloned_repos/spotifydata/pages/cred.py` |

> **Note:** All dependencies are explicitly listed in the `external_dependencies`
> field of the evidence JSON.

---

## 3.  Public API

| Symbol | Type | Description |
|--------|------|-------------|
| `layout()` | function | Returns the Dash layout for the login page. |
| `check_date(timestamp)` | function | Parses a Spotify timestamp string into a `datetime` object. |
| `fetch_data(username)` | function | Orchestrates data retrieval from Spotify and persistence in PostgreSQL. |
| `button_on_clicked(n_clicks, value)` | callback | Handles the login button click, triggers data fetch, and redirects. |

> The module itself has no `used_by` entries, but its functions are used
> internally by the callbacks defined in the same file.

---

## 4.  Detailed Function Documentation

### 4.1 `layout()`

```python
def layout():
    return html.Div([...])
```

* **Purpose** – Builds the UI for the login page.
* **Key Elements**  
  * `dcc.Location(id='url', refresh=True)` – Enables programmatic
    navigation via the `url` component.
  * `dcc.Input(id='username_input')` – Text input for the Spotify username.
  * `html.Button(id='username_submit_button')` – Triggers the login flow.
* **Return Value** – A Dash `Div` containing the form and branding.

> The layout is referenced by the Dash app when rendering the root
> (`/`) route.

---

### 4.2 `check_date(timestamp)`

```python
def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])
```

* **Purpose** – Convert Spotify’s ISO‑8601 timestamp (ending with `Z`)
  into a Python `datetime` object.
* **Why needed** – The database stores `added_at` as a `datetime`; we need
  to compare new records against the most recent stored timestamp.
* **Return Value** – `datetime` instance.

---

### 4.3 `fetch_data(username)`

```python
def fetch_data(username):
    token = spotify.spotify_init(username)
    ...
```

* **Purpose** – Pulls liked and recent tracks, processes them, and
  persists the results in PostgreSQL.
* **Workflow**  
  1. **Token acquisition** – `spotify.spotify_init(username)` returns an
     OAuth token.
  2. **Liked songs**  
     * `spotify.get_liked_songs(token)` → raw list of tracks.  
     * `spotify.process_liked_songs(...)` → list of dicts with selected
       fields.  
     * Convert to `pandas.DataFrame`, create the `liked_songs` table,
       check the most recent `added_at`, filter new records, and insert
       them via `postgres.add_liked_songs_dict`.
  3. **Recent songs** – Same pipeline as liked songs, but stored in the
     `recents` table.
  4. **Master song list** – Union of liked and recent songs; used to
     discover new artists and albums.
  5. **Artists** –  
     * Extract unique artist IDs.  
     * `spotify.get_artists(token, artist_ids)` fetches artist data.  
     * Compare against existing artist IDs in the DB (`select_unique_artists`).  
     * Process new artists (`spotify.process_artists`) and insert via
       `postgres.add_artists_dict`.
  6. **Albums** – Similar to artists: fetch, deduplicate, process, and
     insert with `postgres.add_albums_dict`.

* **Dependencies** – Uses `spotify` for API calls, `postgres` for DB
  operations, `pandas` for DataFrame manipulation, and `datetime` for
  timestamp conversion.

* **Return Value** – None. Side‑effects are database writes.

---

### 4.4 `button_on_clicked(n_clicks, value)`

```python
@callback(
    Output('url', 'pathname'),
    [Input('username_submit_button', 'n_clicks')],
    [State('username_input', 'value')]
)
def button_on_clicked(n_clicks, value):
    if value is None:
        return '/'
    else:
        fetch_data(value)
        return f'/tools/{value}'
```

* **Purpose** – Handles the login button click.
* **Behavior**  
  * If the username field is empty, stay on the root page.  
  * Otherwise, call `fetch_data(value)` to populate the database and
    redirect the browser to `/tools/<username>`.
* **Why it exists** – Provides a seamless user experience: after
  logging in, the user is taken directly to the tools page where they can
  explore their data.
* **Return Value** – New pathname for the `dcc.Location` component,
  causing a client‑side navigation.

---

## 5.  Commented‑Out Callback

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

* **What it would do** – Periodically refresh data while the user is
  on the page (e.g., every few seconds).  
* **Why it is commented** – The current design performs a one‑time
  fetch on login; continuous polling is unnecessary and was disabled.

---

## 6.  Interaction with the Rest of the Codebase

| Downstream Module | Interaction |
|-------------------|-------------|
| `pages.tools` | Receives the user after successful login via the redirect in `button_on_clicked`. |
| `pages.liked_songs`, `pages.recents`, `pages.analytics` | All read from the same PostgreSQL tables populated by `fetch_data`. |
| `postgres` | Provides table creation, data insertion, and querying functions used by `fetch_data`. |
| `spotify` | Supplies OAuth token and raw Spotify data used by `fetch_data`. |

> No other module imports `pages.cred` directly; it is only registered
> as a Dash page.

---

## 7.  Summary

* `pages.cred` is the entry point of the application, presenting a
  login form and orchestrating the initial data ingestion from Spotify.
* It relies on **Dash** for UI and navigation, **Spotipy** (via the
  `spotify` wrapper) for API access, **PostgreSQL** (via the `postgres`
  helper) for persistence, and **pandas** for intermediate data
  manipulation.
* The module’s callbacks ensure that once a user logs in, their data is
  fetched and stored, and the UI redirects them to the tools page where
  they can explore their liked songs, recents, and analytics.

This documentation should give developers a clear understanding of the
module’s responsibilities, its dependencies, and how it fits into the
overall application flow.
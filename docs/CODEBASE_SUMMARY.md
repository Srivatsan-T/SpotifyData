# SpotifyData Codebase Overview

# Codebase Overview

**Total Modules:** 8

This document provides a comprehensive overview of all modules in the codebase.

---

## Module Summaries

### `index`

**File:** `/app/cloned_repos/spotifydata/index.py`  
**UID:** `index`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Error generating summary

**Role in System:** Unknown

---



---

## Module Documentation

### liked_songs.py.md

# `pages.liked_songs` – Liked Songs Page

**File path**  
`/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer Dash application.  
It is responsible for:

* Registering the page with a dynamic URL (`/liked/<username>`).  
* Rendering a navigation bar, a pagination slider, and a placeholder for the songs table.  
* Providing a Dash callback that populates the table with the current page of liked songs.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `postgres` | The page pulls data from the PostgreSQL database. | `postgres.select_liked_songs()` |
| `dash` | Core Dash functionality (page registration). | `dash.register_page` |
| `dash.callback` | Decorator for the callback. | `@callback` |
| `dash.dcc` | Dash Core Components – used for the pagination slider. | `dcc.Slider` |
| `dash.dependencies` | Input/Output/State objects for callbacks. | `Input`, `Output`, `State` |
| `dash.html` | HTML components for layout. | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap‑styled components. | `dbc.NavbarSimple`, `dbc.Table` |
| `math` | Pagination calculations. | `math.ceil` |
| `pandas` | DataFrame creation and manipulation. | `pd.DataFrame` |

> **Note:** The module has no downstream consumers (`used_by` is empty).

---

## Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* Registers this module as a Dash page.  
* The URL contains a `<username>` placeholder that is passed to the `layout` function.

---

## `layout(username=None)`

```python
def layout(username=None):
    liked_songs = postgres.select_liked_songs(0)
    number_of_liked_songs = len(liked_songs)
    page_size = 50
    number_of_pages = math.ceil(number_of_liked_songs / page_size)

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Liked Songs", href=f'http://localhost:8050/liked/{username}', id='LikedSongs')),
            dbc.NavItem(dbc.NavLink("Recents", href=f'http://localhost:8050/recents/{username}', id="Recents")),
            dbc.NavItem(dbc.NavLink("Analytics", href=f'http://localhost:8050/analytics/{username}', id="Analytics")),
            dbc.NavItem(dbc.NavLink("Back", href=f'http://localhost:8050/tools/{username}', id="Back"))
        ],
        brand="Spotify Analyzer",
        brand_href="http://localhost:8050/",
        className='box-form left'
    )

    return html.Div([
        navbar,
        html.Div([dcc.Slider(id='Pagination', min=1, max=number_of_pages, step=1, value=1,
                             marks={i: str(i) for i in range(1, number_of_pages + 1)})],
                 style={'margin': '0 40px'}),
        html.Div(children=[], id='liked_table', style={'margin': '0 40px'})
    ], style={})
```

### What it does

1. **Data fetch** – Calls `postgres.select_liked_songs(0)` to get the full list of liked songs.  
2. **Pagination** – Calculates the number of pages (`page_size = 50`) and creates a `dcc.Slider` that lets the user choose a page.  
3. **Navigation bar** – Uses `dbc.NavbarSimple` to provide links to other pages (`Recents`, `Analytics`, `Back`).  
4. **Table placeholder** – An empty `html.Div` with `id='liked_table'` that will be populated by the callback.

### Interaction with the rest of the system

* The `layout` function is called by Dash when the user navigates to `/liked/<username>`.  
* The `username` parameter is used only for constructing navigation links; the actual data is independent of the username (the database stores all users’ data).

---

## Callback – `pages(active_page, max)`

```python
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']

    if active_page == max:
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50)
    else:
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50, active_page * 50)

    df = pd.DataFrame(liked_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

### Why the dependency exists

* **`postgres`** – Provides `select_liked_songs(beg, end)` to fetch a slice of the liked songs table.  
* **`pandas`** – Converts the raw tuples into a DataFrame for easy manipulation.  
* **`dash_bootstrap_components`** – Renders the DataFrame as a Bootstrap‑styled table.  
* **`dash.dependencies`** – Supplies `Input`, `Output`, and `State` objects for the callback.

### Functionality

1. **Pagination logic** – Determines the slice of data to fetch based on the current slider value (`active_page`).  
2. **Data retrieval** – Calls `postgres.select_liked_songs` with appropriate `beg` and `end` indices.  
3. **DataFrame creation** – Builds a DataFrame with the specified columns.  
4. **Column pruning** – Drops `song_id` and `preview_url` before rendering.  
5. **Table rendering** – Uses `dbc.Table.from_dataframe` to create a styled table that replaces the contents of `liked_table`.

### Interaction with the rest of the system

* The callback is triggered whenever the user moves the pagination slider.  
* It updates the `liked_table` component in the layout, providing a dynamic, paginated view of liked songs.

---

## Summary

* **Purpose** – Display a paginated table of a user’s liked songs.  
* **Key components** – Navigation bar, pagination slider, and a table placeholder.  
* **Data source** – PostgreSQL via `postgres.select_liked_songs`.  
* **Rendering** – Uses `pandas` for data manipulation and `dash_bootstrap_components` for UI.  
* **Integration** – Registered as a Dash page (`/liked/<username>`) and interacts with the rest of the app through navigation links and the pagination slider.

This module is self‑contained: it has no downstream consumers, but it is a core part of the user interface for exploring liked songs.

---

### analytics.py.md

# `pages.analytics` – Analytics Dashboard

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`

The `analytics` module implements the *Analytics* page of the Spotify Analyzer web‑app.  
It is a **Dash page** that shows:

* A navigation bar with links to the other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).
* A year selector (`dcc.Dropdown`) that pulls the list of years from the database.
* A dynamic content area (`target_div`) that displays:
  * A table of the top 3 albums for the selected year.
  * Two bar charts – *Most Popular Songs* and *Least Popular Songs* – for that year.

The page is registered with the URL pattern `/analytics/<username>`.

---

## 1. Imports & Dependencies

| Import | Purpose | File Path |
|--------|---------|-----------|
| `dash`, `dash.callback`, `dash.dcc`, `dash.html` | Core Dash components and callback decorators. | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (navbar, tables). | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `pandas as pd` | Data manipulation and DataFrame creation. | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `postgres` | Database helper functions for retrieving analytics data. | `/app/cloned_repos/spotifydata/pages/analytics.py` |

> **Note:** The `postgres` module is the only *external* dependency that provides data for this page.  
> All other imports are standard Dash or Python libraries.

---

## 2. Page Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* Registers the module as a Dash page.
* The `<username>` part of the URL is passed to the `layout` and callback functions.

---

## 3. `layout(username=None)`

### Purpose
Creates the static layout of the Analytics page.

### Key Elements

| Element | Description | Notes |
|---------|-------------|-------|
| `navbar` | `dbc.NavbarSimple` with four navigation links. | Uses `username` to build URLs. |
| `dcc.Dropdown` | Dropdown for selecting a year. | Options are the first element of each tuple returned by `postgres.get_years()`. |
| `target_div` | Empty container that will be populated by the callback. | Styled with margins for visual spacing. |

### Flow

1. Calls `postgres.get_years()` to obtain a list of available years.
2. Builds the navigation bar with links that include the current `username`.
3. Returns a `html.Div` containing the navbar, the year selector, and the empty `target_div`.

---

## 4. `analytics_display(value)`

### Purpose
Callback that updates `target_div` when a year is selected.

### Trigger
```python
@callback(
    Output('target_div', 'children'),
    [Input('year_drop', 'value')]
)
```

### Logic

| Step | Description | Data Source |
|------|-------------|-------------|
| 1 | **Check** if a year (`value`) is selected. | `value` from the dropdown. |
| 2 | **Retrieve albums** for the year. | `postgres.get_albums_for_year(value)` |
| 3 | **Compute most popular songs** (descending). | `postgres.get_popular_for_year(value, 'desc')` |
| 4 | **Compute least popular songs** (ascending). | `postgres.get_popular_for_year(value, 'asc')` |
| 5 | **Build bar charts** (`dcc.Graph`) for both popularity lists. | Uses the lists `most_pop_list`, `most_names_list`, `least_pop_list`, `least_names_list`. |
| 6 | **Create a DataFrame** of albums and convert it to a Bootstrap table. | `pd.DataFrame(albums, columns=['ALBUM', 'SONGS COUNT'])` |
| 7 | **Return** a list of components: heading, table, and two graphs. | These are rendered inside `target_div`. |
| 8 | **If no year selected**, return a placeholder message. | Simple `html.H1` with styling. |

#### Data Transformation Details

* `most_populars` and `least_populars` are lists of tuples where the 5th element (`j[4]`) represents the month (1‑12).  
* For each month, the popularity score is transformed to `j[2]*10 + 100` (arbitrary scaling) and the song name is stored.  
* The resulting lists are used as the `y` and `text` data for the bar charts.

---

## 5. Interaction with Other Modules

| Module | Interaction | Purpose |
|--------|-------------|---------|
| `pages.cred` | Calls `fetch_data(username)` to populate the database tables before the analytics page is accessed. | Ensures that `liked_songs`, `recents`, `artists`, and `albums` tables are up‑to‑date. |
| `pages.liked_songs` & `pages.recents` | Provide navigation links to the analytics page. | User can move between pages. |
| `postgres` | Supplies all data needed for analytics. | `get_years`, `get_albums_for_year`, `get_popular_for_year`. |

> **Dependency Rationale**  
> The analytics page relies on the `postgres` module because all analytics data (years, albums, popularity metrics) are stored in PostgreSQL.  
> The page does not directly interact with the Spotify API; that work is performed in `pages.cred.fetch_data`.

---

## 6. Usage Summary

1. **User logs in** via the root page (`pages.cred`).  
2. **Data is fetched** from Spotify and stored in PostgreSQL tables.  
3. **User navigates** to `/analytics/<username>`.  
4. The **dropdown** is populated with years from the database.  
5. When a year is selected, the **callback** queries the database, builds charts and a table, and displays them in `target_div`.

---

## 7. File‑Level Summary

```text
File: /app/cloned_repos/spotifydata/pages/analytics.py
- Registers a Dash page at /analytics/<username>
- Provides a layout with a navbar, year selector, and placeholder div
- Implements a callback that renders album table and popularity charts
- Depends on postgres module for data retrieval
- Uses Dash, Dash Bootstrap Components, and pandas for UI and data handling
```

---

### Missing Relationship Data

The evidence shows no `used_by` entries for `pages.analytics`.  
Therefore, no other modules explicitly import or call functions from this module beyond the Dash framework’s internal routing.  
If additional relationships exist, they are not captured in the provided evidence.

---

### spotify.py.md

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

---

### cred.py.md

# Module `pages.cred`

**File path**  
`/app/cloned_repos/spotifydata/pages/cred.py`

The `cred` module implements the *login* page of the Spotify Analyzer Dash application.  
It is registered as the root page (`path='/'`) and is responsible for:

1. Rendering the login form.  
2. Fetching the user’s Spotify data (liked songs, recent plays, artists, albums).  
3. Persisting that data in a PostgreSQL database.  
4. Redirecting the user to the tools page after a successful login.

Below is a developer‑focused breakdown of the module’s public API, its dependencies, and how it interacts with the rest of the codebase.

---

## Public API

| Symbol | Type | Description |
|--------|------|-------------|
| `layout()` | function | Returns a Dash `html.Div` that contains the login form and a hidden `dcc.Location` used for redirection. |
| `check_date(timestamp)` | function | Converts a Spotify timestamp string (ISO‑8601 with a trailing `Z`) into a `datetime` object. |
| `fetch_data(username)` | function | Orchestrates the entire data‑fetching pipeline: authenticates with Spotify, pulls liked songs and recent plays, processes the raw data, and writes it to PostgreSQL. |
| `button_on_clicked(n_clicks, value)` | callback | Triggered when the **Login** button is pressed. Calls `fetch_data` and returns a new pathname (`/tools/<username>`). |

> **Note**: The module also contains a commented‑out callback (`time_based_calc`) that would refresh data on a timer, but it is not active.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `dash`, `dash.html`, `dash.dcc`, `dash.callback`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State` | The module is a Dash page; it renders UI components and defines callbacks. | UI rendering (`html.Div`, `dcc.Input`, `dcc.Button`, `dcc.Location`), callback registration (`@callback`), and input/output wiring. |
| `spotify` | Provides all Spotify API interactions. | `spotify_init`, `get_liked_songs`, `recent_songs`, `get_artists`, `get_albums`, `process_liked_songs`, `process_artists`, `process_albums`. |
| `postgres` | Handles persistence of fetched data. | `create_liked_songs_table`, `create_recent_songs_table`, `create_artist_table`, `create_album_table`, `check_liked_songs`, `add_liked_songs_dict`, `add_artists_dict`, `add_albums_dict`, `select_unique_artists`, `select_unique_albums`. |
| `pandas` | Data manipulation for filtering new records. | `pd.DataFrame`, `df.apply`, `df[df['added_at'] > res]`. |
| `datetime` | Parsing ISO timestamps from Spotify. | `datetime.fromisoformat`. |

> All dependencies are explicitly listed in the `depends_on` and `external_dependencies` sections of the JSON evidence.

---

## How the Module Works

### 1. Page Registration

```python
dash.register_page(__name__, path='/')
```

Registers the module as the root page of the Dash app. When the user visits `/`, Dash will call `layout()` to render the page.

### 2. Rendering the Login Form

`layout()` returns a nested `html.Div` structure:

- `dcc.Location(id='url', refresh=True)` – a hidden component that can be updated to change the browser’s pathname.
- Two columns (`left` and `right`) styled with CSS classes.
- The right column contains:
  - A heading (`Login`) and a prompt.
  - A `dcc.Input` for the Spotify username (`id='username_input'`).
  - A `html.Button` (`id='username_submit_button'`) that triggers the login callback.

### 3. Timestamp Conversion

```python
def check_date(timestamp):
    return datetime.fromisoformat(timestamp[:-1])
```

Spotify returns timestamps like `"2023-07-01T12:34:56Z"`.  
`check_date` strips the trailing `Z` and converts the string to a `datetime` object for comparison.

### 4. Data Fetching Pipeline (`fetch_data`)

1. **Authenticate**  
   ```python
   token = spotify.spotify_init(username)
   ```

2. **Liked Songs**  
   - Pull raw data: `songs = spotify.get_liked_songs(token)`
   - Process into a list of dictionaries: `songs_dict = spotify.process_liked_songs(songs)`
   - Convert to a `DataFrame` to filter new entries:
     ```python
     df = pd.DataFrame.from_dict(songs_dict)
     res, flag = postgres.check_liked_songs('liked_songs')
     if flag:
         df['added_at'] = df['added_at'].apply(check_date)
         df = df[df['added_at'] > res]
     ```
   - Store the filtered list in the database:
     ```python
     songs_dict = list(df.T.to_dict().values())
     postgres.add_liked_songs_dict(songs_dict, 'liked_songs')
     ```

3. **Recent Plays** – identical to liked songs but uses the `recents` table.

4. **Master Song List** – combines liked and recent songs, deduplicated with `set`.

5. **Artists**  
   - Extract unique artist IDs from the master list.  
   - Fetch artist details: `artists = spotify.get_artists(token, artist_ids_spotify)`  
   - Remove already‑stored artists by comparing with `postgres.select_unique_artists()`.  
   - Process and insert new artists.

6. **Albums** – analogous to artists: fetch, dedupe, process, insert.

The function is intentionally side‑effect‑heavy: it writes to the database but returns nothing.

### 5. Login Callback

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

- When the **Login** button is clicked, the callback receives the username.
- If the username is empty, the user stays on the login page.
- Otherwise, `fetch_data` is called to populate the database, and the browser is redirected to `/tools/<username>`.

### 6. (Commented) Periodic Refresh

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

This code is currently commented out. If enabled, it would periodically call `fetch_data` to keep the database up‑to‑date.

---

## Interaction with Other Modules

| Module | Interaction |
|--------|-------------|
| `pages.tools` | After login, the user is redirected to `/tools/<username>`. |
| `pages.liked_songs`, `pages.recents`, `pages.analytics` | These pages read from the tables created/updated by `cred.fetch_data`. |
| `postgres` | All database operations are performed through this module. |
| `spotify` | All API calls to Spotify are routed through this module. |

> The `cred` module itself is not imported elsewhere; it is discovered by Dash via `dash.register_page`. Its functions (`layout`, `fetch_data`, `button_on_clicked`) are used internally by the Dash framework.

---

## Summary

- **Purpose**: Provide a login interface, authenticate with Spotify, fetch and store user data, and redirect to the tools page.  
- **Key Functions**: `layout`, `check_date`, `fetch_data`, `button_on_clicked`.  
- **Dependencies**: Dash UI components, Spotify API wrapper, PostgreSQL helper, Pandas, and datetime.  
- **Data Flow**: Username → Spotify API → Processed dicts → Pandas DataFrames → PostgreSQL tables.  
- **Redirection**: `dcc.Location` + callback updates the pathname to `/tools/<username>` after successful data import.

This documentation should give developers a clear understanding of how the `cred` module fits into the overall application, what external services it relies on, and how its internal logic orchestrates data fetching and persistence.

---

### recents.py.md

# `recents.py`

**File path**  
`/app/cloned_repos/spotifydata/pages/recents.py`

---

## Overview

`recents.py` defines a **Dash page** that displays a paginated table of the user’s most recently played songs.  
The page is registered with the Dash app under the URL pattern `/recents/<username>`.  
It pulls data from the PostgreSQL database via the `postgres` module, formats it with `pandas`, and renders it with `dash_bootstrap_components`.

---

## Dependencies

| Dependency | Why it exists | What functionality is imported / relied upon |
|------------|---------------|----------------------------------------------|
| `postgres` | The page needs to read the list of recent songs that have already been stored in the database. | `postgres.select_recent_songs(beg, end)` – returns a list of song tuples. |
| `dash` | Core Dash framework for building the app. | `dash.register_page` – registers the page with the app. |
| `dash.callback` | Declares the callback that updates the table when the pagination slider changes. | `@callback` decorator. |
| `dash.dcc` | Provides the `Slider` component used for pagination. | `dcc.Slider`. |
| `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State` | Connects UI components to the callback. | `Input`, `Output`, `State`. |
| `dash.html` | Basic HTML components for layout. | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap‑styled components for a nicer UI. | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink`, `dbc.Table`. |
| `math` | Calculates the number of pages needed for pagination. | `math.ceil`. |
| `pandas` | Converts raw tuples into a DataFrame for easy table rendering. | `pd.DataFrame`. |

> **Note:** All imports are explicitly listed in the module’s `external_dependencies` section of the evidence.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

* Registers this module as a page in the Dash app.  
* The `<username>` part of the URL is passed to the `layout` and `pages` functions as the `username` argument.

---

## Functions

### `layout(username=None)`

* **Purpose** – Builds the static part of the page (navbar, slider, empty table placeholder).  
* **Key Steps**  
  1. **Fetch data** – Calls `postgres.select_recent_songs(0)` to get all recent songs.  
  2. **Pagination** – Calculates `number_of_pages` using `math.ceil(number_of_recent_songs / 50)`.  
  3. **Navbar** – Uses `dbc.NavbarSimple` with links to *Liked Songs*, *Recents*, *Analytics*, and *Back*.  
  4. **Slider** – `dcc.Slider` with `min=1`, `max=number_of_pages`, `step=1`, and `marks` for each page number.  
  5. **Table placeholder** – An empty `html.Div` with `id='recents_table'` that will be populated by the callback.  
* **Return Value** – A `html.Div` containing the navbar, slider, and table placeholder.

### `pages(active_page, max)`

* **Purpose** – Callback that updates the table when the slider value changes.  
* **Inputs** – `active_page` (current slider value) and `max` (maximum slider value).  
* **Logic**  
  1. **Determine slice** – If the active page is the last page, call `postgres.select_recent_songs(active_page*50-50)`; otherwise call `postgres.select_recent_songs(active_page*50-50, active_page*50)`.  
  2. **Create DataFrame** – `pd.DataFrame(recent_songs, columns=column_names)`.  
  3. **Drop unnecessary columns** – `song_id` and `preview_url`.  
  4. **Render table** – `dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)`.  
* **Output** – The rendered table is returned to the `recents_table` component.

---

## Interaction with Other Modules

| Module | Relationship | Explanation |
|--------|--------------|-------------|
| `postgres` | **Used by** | `recents` calls `postgres.select_recent_songs` to fetch data. |
| `pages.liked_songs`, `pages.analytics`, `pages.tools` | **Not used by** | These pages are separate routes; they do not import or depend on `recents`. |
| `pages.cred` | **Not used by** | The login page does not import `recents`. |

> **Evidence**: The `used_by` list for `recents` is empty, indicating no downstream modules depend on it.

---

## Role in the System

* **User Interface** – Provides a visual, paginated view of the user’s recent listening history.  
* **Data Access** – Delegates data retrieval to the `postgres` module, keeping database logic separate.  
* **Reusability** – The layout and callback are self‑contained; they can be imported or modified without affecting other pages.  
* **Navigation** – The navbar links integrate the page into the overall application flow.

---

## Summary

`recents.py` is a self‑contained Dash page that:

1. Registers itself under `/recents/<username>`.  
2. Builds a navbar, pagination slider, and empty table placeholder.  
3. Uses a callback to fetch a slice of recent songs from PostgreSQL, format them with `pandas`, and render a Bootstrap table.  

All dependencies are explicitly imported, and the module does not influence or rely on any other page modules.

---

### postgres.py.md

# PostgreSQL Data Access Layer – `postgres.py`

**File path**: `/app/cloned_repos/spotifydata/postgres.py`

The `postgres` module is the single source of truth for all interactions with the local PostgreSQL database that backs the Spotify Analyzer web‑app.  
It exposes a small, well‑defined API for creating tables, inserting data, and querying the data that is later consumed by the Dash pages (`pages.cred`, `pages.liked_songs`, `pages.recents`, `pages.analytics`).

> **NOTE** – All relationships are taken directly from the supplied JSON evidence.  
> If a dependency or usage relationship is missing from the evidence, it is explicitly noted below.

---

## 1. Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `psycopg2` | Provides the PostgreSQL driver used to open a connection. | `psycopg2.connect()` |
| `psycopg2.extras.execute_values` | Enables efficient bulk inserts of many rows. | `execute_values(cursor, query, values)` |

> The module itself has **no other internal dependencies**.

---

## 2. Public API

| Function | Signature | Purpose | Key Implementation Details |
|----------|-----------|---------|-----------------------------|
| `postgres_init` | `postgres_init(db='postgres', user='postgres', pw='admin', host='localhost', port='5432')` | Opens a new database connection. | Uses `psycopg2.connect()` with the supplied parameters. |
| `create_liked_songs_table` | `create_liked_songs_table()` | Creates the `liked_songs` table. | Reads `sql/create_liked_songs.sql` and executes it. |
| `create_recent_songs_table` | `create_recent_songs_table()` | Creates the `recents` table. | Reads `sql/create_recent_songs.sql`. |
| `create_album_table` | `create_album_table()` | Creates the `album` table and returns all rows. | Executes `sql/create_album_table.sql` then `sql/select_all_albums.sql`. |
| `create_artist_table` | `create_artist_table()` | Creates the `artist` table. | Executes `sql/create_artist_table.sql`. |
| `select_unique_artists` | `select_unique_artists()` | Returns a list of unique artist IDs already stored. | Executes `sql/select_unique_artist_ids.sql`. |
| `check_liked_songs` | `check_liked_songs(table)` | Returns the most recent `added_at` timestamp for a table and a flag indicating if the table contains data. | Executes `SELECT MAX(added_at) FROM {table}`. |
| `add_liked_songs_dict` | `add_liked_songs_dict(songs, table)` | Bulk‑inserts a list of song dictionaries into the specified table. | Escapes single quotes in `song_name`, builds a column list, and uses `execute_values`. |
| `add_albums_dict` | `add_albums_dict(albums)` | Bulk‑inserts a list of album dictionaries into the `album` table. | Escapes single quotes in `album_name` and uses `execute_values`. |
| `add_artists_dict` | `add_artists_dict(artists)` | Bulk‑inserts a list of artist dictionaries into the `artist` table. | Escapes single quotes in `artist_name` and uses `execute_values`. |
| `select_unique_albums` | `select_unique_albums()` | Returns a list of unique album IDs already stored. | Executes `sql/select_unique_album_ids.sql`. |
| `select_liked_songs` | `select_liked_songs(beg, end='all')` | Returns a slice of all liked songs (supports pagination). | Executes `sql/view_liked_songs.sql` and returns `res[beg:]` or `res[beg:end]`. |
| `select_recent_songs` | `select_recent_songs(beg, end='all')` | Returns a slice of all recent songs. | Executes `sql/view_recents.sql`. |
| `get_years` | `get_years()` | Returns a list of years for which data exists. | Executes `sql/get_years.sql`. |
| `get_albums_for_year` | `get_albums_for_year(year)` | Returns albums for a specific year. | Executes `sql/get_albums.sql` with the year interpolated. |
| `get_popular_for_year` | `get_popular_for_year(year, flag)` | Returns the most/least popular songs for each month of a year. | Loops over months 1‑12, reads `sql/get_popular.sql`, executes with `(year, month, flag)`, aggregates results. |

> All functions open a new connection, perform the operation, commit (if needed), close the cursor, and close the connection.  
> No connection pooling is used; each call is independent.

---

## 3. How Other Modules Use `postgres`

| Module | Usage | What it relies on |
|--------|-------|-------------------|
| `pages.cred` | *`fetch_data`* creates tables, checks for existing data, inserts new songs/artists/albums. | `create_*_table`, `check_liked_songs`, `add_*_dict`, `select_unique_*` |
| `pages.liked_songs` | `layout` and `pages` functions query liked songs for display. | `select_liked_songs` |
| `pages.recents` | `layout` and `pages` functions query recent songs for display. | `select_recent_songs` |
| `pages.analytics` | `layout` queries available years; `analytics_display` queries albums and popularity data. | `get_years`, `get_albums_for_year`, `get_popular_for_year` |
| `pages.cred.fetch_data` (duplicate) | Same as `pages.cred.fetch_data` above. | Same set of functions |

> **Dependency graph** (simplified):  
> `pages.*` → `postgres` → PostgreSQL database.

---

## 4. External Dependencies

- **`psycopg2`** – PostgreSQL driver.
- **`psycopg2.extras.execute_values`** – Bulk insert helper.

These are imported at the top of the file:

```python
import psycopg2
from psycopg2.extras import execute_values
```

---

## 5. SQL Files

The module relies on a set of SQL scripts stored in the `sql/` directory:

| SQL file | Purpose |
|----------|---------|
| `create_liked_songs.sql` | Table definition for liked songs. |
| `create_recent_songs.sql` | Table definition for recent songs. |
| `create_album_table.sql` | Table definition for albums. |
| `create_artist_table.sql` | Table definition for artists. |
| `select_all_albums.sql` | Retrieve all albums (used after creation). |
| `select_unique_artist_ids.sql` | Retrieve distinct artist IDs. |
| `select_unique_album_ids.sql` | Retrieve distinct album IDs. |
| `view_liked_songs.sql` | View or query liked songs. |
| `view_recents.sql` | View or query recent songs. |
| `get_years.sql` | Retrieve distinct years from data. |
| `get_albums.sql` | Retrieve albums for a given year. |
| `get_popular.sql` | Retrieve popular songs for a given month/year. |

> The module opens these files relative to the current working directory (`open('sql/...').read()`).

---

## 6. Error Handling & Edge Cases

- **Empty data**: `add_*_dict` functions silently return if the list is empty.
- **No rows**: `check_liked_songs` returns `(None, False)` if the table is empty.
- **Pagination**: `select_*_songs` accepts `beg` and `end` indices; if `end` is `'all'`, it returns all rows from `beg` onward.
- **SQL injection**: Single quotes in names are escaped (`replace("'", "''")`) before bulk insert.

---

## 7. Summary

`postgres.py` is the backbone of the data layer for the Spotify Analyzer.  
It abstracts all database operations behind a clean API, allowing the Dash pages to focus on presentation and user interaction.  
By centralizing SQL execution and connection handling, the module ensures consistency, reduces duplication, and makes future database migrations straightforward.

---

---

### tools.py.md

# `pages.tools` – Tool Page for the Spotify Analyzer

**File path**  
`/app/cloned_repos/spotifydata/pages/tools.py`

---

## Overview

`pages.tools` is a Dash page that provides a simple navigation bar and a greeting for the user.  
It is registered as a dynamic route (`/tools/<username>`) and is intended to be the landing page after a user logs in.

The module has no internal dependencies on other parts of the codebase – it only relies on external libraries for UI rendering.

---

## Imports & External Dependencies

| Import | Purpose |
|--------|---------|
| `dash` | Core Dash framework for page registration and callbacks. |
| `dash.html` | HTML component helpers (`html.Div`, `html.H1`, etc.). |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (`NavbarSimple`, `NavItem`, `NavLink`). |

These dependencies are required to build the page layout and navigation bar.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/tools/<username>')
```

* **Why** – Registers this module as a Dash page that accepts a dynamic `username` segment.  
* **What** – Makes the page discoverable by Dash’s page routing system.  
* **File reference** – `pages/tools.py`

---

## `layout` Function

```python
def layout(username=None):
```

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `username` | `str` | `None` | The Spotify username extracted from the URL. It is used to build navigation links and to display a personalized greeting. |

### Functionality

1. **Navbar Construction**  
   * Uses `dbc.NavbarSimple` with three navigation links:  
     * **Liked Songs** → `/liked/<username>`  
     * **Recents** → `/recents/<username>`  
     * **Analytics** → `/analytics/<username>`  
   * The navbar is styled with the class `box-form left`.

2. **Greeting**  
   * Splits the `username` on `%20` (URL‑encoded space) and takes the first part as `first_name`.  
   * Displays a large, white‑text greeting:  
     * `"Hello"`  
     * `<first_name>`  
     * A subtitle prompting the user to use the navigation links.

3. **Return Value**  
   * An `html.Div` containing the navbar and the greeting section.  
   * The outer `Div` is styled with `{'width': '100vw'}` to span the viewport width.

### Example Return Structure

```html
<div style="width:100vw;">
  <div class="box-form left">  <!-- Navbar -->
    ...
  </div>
  <div style="padding-left:25px; padding-top:10px;">
    <h1 style="font-size:10vmax;color:white;">Hello</h1>
    <h1 style="font-size:10vmax;color:white;"><first_name></h1>
    <h5 style="color:white;">use the navigation links to access various features of the tool</h5>
  </div>
</div>
```

### Usage

* The Dash application automatically calls `layout` when the user navigates to `/tools/<username>`.  
* The returned layout is rendered as the page content.  
* The navigation links rely on the same `username` to keep the session context.

---

## Dependencies Summary

| Dependency | Reason | Functionality Used |
|------------|--------|--------------------|
| `dash` | Page registration and callback infrastructure | `dash.register_page` |
| `dash.html` | Building HTML components | `html.Div`, `html.H1`, `html.H5` |
| `dash_bootstrap_components` | Bootstrap‑styled navigation bar | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink` |

No internal modules are imported; therefore, there are no downstream dependencies (`used_by` is empty).

---

## Documentation Summary

- **Module**: `pages.tools` – provides a simple, user‑friendly landing page after login.  
- **Key Function**: `layout(username)` – builds the page layout with a navbar and greeting.  
- **External Libraries**: Dash core, Dash HTML, Dash Bootstrap Components.  
- **Routing**: Registered as `/tools/<username>`.  
- **No downstream usage** – the module is self‑contained and only renders UI.

Feel free to extend the page with additional components or callbacks as needed, but keep in mind that the current implementation is intentionally lightweight.

---

### index.py.md

# `index.py` – Application Bootstrap

**File path**: `/app/cloned_repos/spotifydata/index.py`

`index.py` is the single entry point for the Spotify Analyzer Dash application.  
It creates the `Dash` app instance, configures the Bootstrap theme, and sets up the page container that will render the individual pages registered elsewhere in the codebase.

---

## 1. Overview

```python
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([dash.page_container])

if __name__ == '__main__':
    app.run_server(debug=True)
```

- **Dash app creation** – `Dash(__name__, ...)` creates the main application object.
- **Bootstrap theme** – `external_stylesheets=[dbc.themes.BOOTSTRAP]` loads the Bootstrap CSS so that all components are styled consistently.
- **Page routing** – `use_pages=True` tells Dash to automatically discover modules that call `dash.register_page`.  
  The `dash.page_container` placeholder will render the currently selected page.
- **Server launch** – `app.run_server(debug=True)` starts the development server on `http://127.0.0.1:8050/`.

---

## 2. Dependencies

| Dependency | Why it exists | Functionality imported / relied upon |
|------------|---------------|--------------------------------------|
| `dash` | Provides the core Dash framework. | `Dash` constructor, `dash.page_container` placeholder. |
| `dash.html` | Gives access to HTML components. | `html.Div` used for the app layout. |
| `dash_bootstrap_components` | Supplies Bootstrap themes and components. | `dbc.themes.BOOTSTRAP` used as an external stylesheet. |

> **Note**: `index.py` has no internal dependencies (i.e., it does not import any other modules from the project). All other modules register pages via `dash.register_page`, but they are not directly imported here.

---

## 3. Usage

### 3.1 Running the Application

```bash
python app.py
```

- The script checks `if __name__ == '__main__'` to ensure it is executed as the main program.
- `app.run_server(debug=True)` starts the Dash development server with live‑reload enabled.

### 3.2 Page Rendering

- **Page registration**: Other modules (e.g., `pages.tools`, `pages.analytics`, etc.) call `dash.register_page`.  
  When a user navigates to a URL that matches a registered page, Dash automatically renders that page inside the `dash.page_container` placeholder defined in `index.py`.

- **Layout**: The layout is a single `html.Div` containing the `dash.page_container`.  
  This minimal layout allows all registered pages to be displayed without additional scaffolding.

---

## 4. Role in the System

- **Bootstrap**: `index.py` is the sole module that creates the `Dash` application instance.  
  All other modules rely on this instance indirectly by registering pages and defining callbacks that the app will manage.

- **Routing**: By enabling `use_pages=True`, the module delegates routing responsibilities to Dash’s page system.  
  The `dash.page_container` acts as a dynamic placeholder that swaps in the appropriate page component based on the current URL.

- **Styling**: The inclusion of the Bootstrap theme ensures a consistent UI across all pages without requiring each page to import the stylesheet separately.

---

## 5. Summary

- **Primary purpose**: Initialize the Dash app, apply Bootstrap styling, and provide a container for page content.
- **Key imports**: `Dash`, `html.Div`, `dash_bootstrap_components.themes.BOOTSTRAP`, `dash.page_container`.
- **Execution**: Run via `python app.py`; the server listens on `http://127.0.0.1:8050/`.
- **Dependencies**: Only external Dash and Bootstrap components; no internal project modules are imported.
- **Interaction**: Other modules register pages; `index.py` renders them through `dash.page_container`.

This module is the foundation upon which the entire Spotify Analyzer web application is built.

---

### codebase_overview.md

# Codebase Overview

**Total Modules:** 8

This document provides a comprehensive overview of all modules in the codebase.

---

## Module Summaries

### `index`

**File:** `/app/cloned_repos/spotifydata/index.py`  
**UID:** `index`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Error generating summary

**Role in System:** Unknown

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Error generating summary

**Role in System:** Unknown

---



---


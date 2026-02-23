# SpotifyData Codebase Overview

# Codebase Overview

**Total Modules:** 8

This document provides a comprehensive overview of all modules in the codebase.

---

## Module Summaries

### `index`

**File:** `/app/cloned_repos/spotifydata/index.py`  
**UID:** `index`

**Purpose:** Initializes and runs a Dash web application using Bootstrap styling and page routing.

**Responsibilities:**
- Creates a Dash app instance with Bootstrap theme and page support.
- Defines the main layout to include the page container.
- Starts the development server when executed as the main module.

**Key Components:**
- `app (Dash instance)`
- `app.layout (html.Div containing dash.page_container)`

**Dependencies:** `dash`, `dash.Dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Entry point that launches the web interface for the Spotify data application, coordinating page rendering and styling.

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Error parsing summary response

**Role in System:** Unknown

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** This module implements the landing page of a Dash web application that authenticates a Spotify user, retrieves their music data, and stores it in a PostgreSQL database.

**Responsibilities:**
- Creates the login page layout with input fields and a submit button.
- Converts Spotify timestamp strings to Python datetime objects via `check_date`.
- Fetches liked songs, recent songs, artists, and albums from Spotify, processes them, and inserts new records into PostgreSQL tables.
- Defines a Dash callback that triggers data fetching on button click and redirects to the tools page.
- Handles incremental updates by comparing timestamps with existing database entries.
- 

**Key Components:**
- `layout()`
- `check_date(timestamp)`
- `fetch_data(username)`
- `button_on_clicked(n_clicks,value)`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State`, `dash.html`, `datetime.datetime`, `pandas`, `postgres`, `spotify`

**Role in System:** Serves as the entry point for user authentication and data ingestion, bridging the front‑end Dash interface with the back‑end Spotify API and PostgreSQL storage. It initiates the data pipeline that feeds subsequent analytical pages.

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's liked Spotify songs.

**Responsibilities:**
- Registers the '/liked/<username>' route and constructs the page layout with navigation and pagination controls.
- Retrieves liked songs from the PostgreSQL database via the postgres module.
- Transforms the retrieved data into a pandas DataFrame and renders it as a Bootstrap table.
- Handles pagination logic to fetch appropriate slices of data based on user interaction.
- Integrates navigation links to other pages (Recents, Analytics, Back).

**Key Components:**
- `layout(username=None)`
- `pages(active_page,max)`
- `postgres.select_liked_songs`
- `dbc.NavbarSimple`
- `dcc.Slider`
- `dbc.Table.from_dataframe`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the user-facing component of the Spotify Analyzer application, enabling users to view and navigate through their liked songs within the web interface.

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's most recent Spotify songs, including navigation links to other pages.

**Responsibilities:**
- Fetch recent song data from the PostgreSQL database
- Calculate pagination parameters and render a slider for page selection
- Generate a navigation bar linking to Liked Songs, Recents, Analytics, and Back pages
- Render the song table using Dash Bootstrap components
- Update the table contents dynamically based on slider input via a callback

**Key Components:**
- `layout(username=None)`
- `pages(active_page,max)`
- `navbar (dbc.NavbarSimple)`
- `dcc.Slider (Pagination)`
- `dbc.Table.from_dataframe`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the Recents view in the Spotify Analyzer web application, enabling users to browse their recent listening history with pagination and navigation to related analytics pages.

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Provides a user‑specific tools page for the Spotify Analyzer web app, featuring navigation links to liked songs, recents, and analytics.

**Responsibilities:**
- Registers the page with Dash using a dynamic URL template.
- Defines a layout function that builds a navbar and greeting header based on the supplied username.
- Generates navigation links pointing to other app sections for the current user.

**Key Components:**
- `layout(username=None) function`
- `NavbarSimple component with NavLinks`

**Dependencies:** `dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Serves as one of the main pages in the Dash application, enabling users to access different Spotify data features via a personalized interface.

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Provides a PostgreSQL data access layer for storing and retrieving Spotify data such as liked songs, recent songs, albums, and artists, and offers analytics queries.

**Responsibilities:**
- Establishes database connections via psycopg2
- Creates and manages tables for liked songs, recent songs, albums, and artists
- Inserts bulk data into tables using execute_values
- Retrieves data for display and analytics (e.g., unique artists/albums, song lists, yearly statistics)

**Key Components:**
- `postgres_init`
- `create_liked_songs_table`
- `create_recent_songs_table`
- `create_album_table`
- `create_artist_table`
- `select_unique_artists`
- `check_liked_songs`
- `add_liked_songs_dict`
- `add_albums_dict`
- `add_artists_dict`
- `select_unique_albums`
- `select_liked_songs`
- `select_recent_songs`
- `get_years`
- `get_albums_for_year`
- `get_popular_for_year`

**Dependencies:** `psycopg2`, `psycopg2.extras.execute_values`

**Used By:** `pages.analytics`, `pages.analytics.analytics_display`, `pages.analytics.layout`, `pages.cred`, `pages.cred.fetch_data`, `pages.liked_songs`, `pages.liked_songs.layout`, `pages.liked_songs.pages`, `pages.recents`, `pages.recents.layout`, `pages.recents.pages`

**Role in System:** Acts as the core data persistence layer, exposing CRUD and analytics functions to the UI and analytics pages, enabling data-driven features across the application.

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Provides a data access layer for Spotify, handling authentication and retrieval of recent plays, liked tracks, albums, and artists, then normalizing the data into dictionary structures.

**Responsibilities:**
- Authenticate a user via Spotify OAuth and return an access token.
- Fetch the user's most recent played tracks and return them as a list of items.
- Retrieve all tracks the user has saved (liked) in batches.
- Batch-fetch album details given a list of album IDs.
- Batch-fetch artist details given a list of artist IDs.
- Transform raw liked track data into a flat list of dictionaries with key metadata.
- Transform raw album data into a flat list of dictionaries with key metadata.
- Transform raw artist data into a flat list of dictionaries with key metadata.

**Key Components:**
- `spotify_init()`
- `recent_songs()`
- `get_liked_songs()`
- `get_albums()`
- `get_artists()`
- `process_liked_songs()`
- `process_albums()`
- `process_artists()`
- `username`
- `client_id`
- `client_secret`
- `redirect_uri`
- `scope`

**Dependencies:** `dotenv.load_dotenv`, `os`, `pandas`, `spotipy`

**Used By:** `pages.cred`, `pages.cred.fetch_data`

**Role in System:** Serves as the Spotify API client and data normalizer, supplying other application components (e.g., UI pages) with structured music data for display or further analysis.

---



---

## Module Documentation

### spotify.py.md

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

---

### recents.py.md

# `recents.py` – Recents Page

**File path**  
`/app/cloned_repos/spotifydata/pages/recents.py`

---

## Overview

`recents.py` implements the **Recents** page of the Spotify Analyzer web application.  
It is a Dash page that displays a paginated table of the most recently played songs for a
given user. The page is registered with the URL pattern `/recents/<username>`.

The module relies on:

| Dependency | Purpose |
|------------|---------|
| `postgres` | Fetches recent‑song data from the PostgreSQL database. |
| `dash` & `dash_bootstrap_components` | Build the page layout and UI components. |
| `pandas` | Convert raw database rows into a DataFrame for easy rendering. |
| `math` | Compute the number of pagination pages. |

---

## Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

* Registers this module as a Dash page.  
* The `<username>` placeholder is passed to the `layout` function.

---

## `layout(username=None)`

### Purpose
Creates the static part of the page: a navigation bar, a pagination slider, and an empty
container that will be filled with the recent‑songs table.

### Key Steps

1. **Data Retrieval**  
   ```python
   recents = postgres.select_recent_songs(0)
   ```
   * Calls `postgres.select_recent_songs` to fetch all recent songs (starting at offset 0).  
   * The `postgres` module is responsible for executing the SQL query that returns the
     recent‑songs view.

2. **Pagination Calculation**  
   ```python
   number_of_recent_songs = len(recents)
   page_size = 50
   number_of_pages = math.ceil(number_of_recent_songs / page_size)
   ```
   * Uses `math.ceil` to determine how many pages are needed when showing 50 songs per page.

3. **Navigation Bar**  
   ```python
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
   ```
   * Provides quick navigation to other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).

4. **Return Structure**  
   ```python
   return html.Div([
       navbar,
       html.Div([dcc.Slider(id='Pagination', min=1, max=number_of_pages,
                            step=1, value=1,
                            marks={i: str(i) for i in range(1, number_of_pages+1)})],
                style={'margin':'0 40px'}),
       html.Div(children=[], id='recents_table', style={'margin':'0 40px'})
   ], style={})
   ```
   * The slider (`Pagination`) controls the current page.  
   * The `recents_table` div will be populated by the callback below.

---

## Callback `pages(active_page, max)`

```python
@callback(
    Output('recents_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    ...
```

### Purpose
Dynamically updates the table of recent songs whenever the user changes the pagination slider.

### Logic

1. **Column Definition**  
   ```python
   column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
   ```

2. **Data Retrieval with Pagination**  
   ```python
   if active_page == max:
       recent_songs = postgres.select_recent_songs(active_page*50-50)
   else:
       recent_songs = postgres.select_recent_songs(active_page*50-50, active_page*50)
   ```
   * Calls `postgres.select_recent_songs` with `beg` and optional `end` parameters to fetch
     only the rows for the current page.

3. **DataFrame Construction**  
   ```python
   df = pd.DataFrame(recent_songs, columns=column_names)
   df = df.drop(['song_id', 'preview_url'], axis=1)
   ```

4. **Render Table**  
   ```python
   return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
   ```
   * Uses `dash_bootstrap_components` to create a styled table from the DataFrame.

---

## Dependencies Explained

| Module | Why it is imported | What functionality is used |
|--------|--------------------|----------------------------|
| `postgres` | Provides database access functions (`select_recent_songs`). | `select_recent_songs` is called to fetch recent‑song records. |
| `dash` | Core Dash framework. | `dash.register_page` registers the page. |
| `dash_bootstrap_components` | Bootstrap‑styled components. | `NavbarSimple`, `NavItem`, `NavLink`, `Table`. |
| `dash.dependencies` (`Input`, `Output`, `State`) | Defines callback inputs/outputs. | `@callback` decorator and its arguments. |
| `dash` (`dcc`, `html`) | UI components. | `dcc.Slider`, `html.Div`, `html.H1`, etc. |
| `pandas` | Data manipulation. | `pd.DataFrame` and `drop`. |
| `math` | Mathematical utilities. | `math.ceil` for pagination calculation. |

---

## Interaction Flow

1. **User navigates** to `/recents/<username>`.  
2. Dash calls `layout(username)` to render the page skeleton.  
3. The slider (`Pagination`) is displayed with marks for each page.  
4. When the slider value changes, the `pages` callback is triggered.  
5. The callback fetches the appropriate slice of recent songs from the database, builds a
   DataFrame, removes unnecessary columns, and renders a Bootstrap table inside
   `recents_table`.  
6. The user can navigate between pages using the slider; the table updates accordingly.

---

## Notes

* The module does **not** directly handle authentication or data fetching from Spotify;
  that logic resides in `pages.cred` and the `spotify` module.
* The `recents` page relies on the database schema defined in the SQL files referenced by
  `postgres.select_recent_songs`.  
* No other modules list `recents` as a dependency in the provided evidence, but the
  `postgres` module lists `recents` as a consumer.

---

### Summary

`recents.py` is a self‑contained Dash page that:

1. **Registers** itself under `/recents/<username>`.  
2. **Builds** a navigation bar, pagination slider, and placeholder for a table.  
3. **Fetches** recent‑song data from PostgreSQL via the `postgres` module.  
4. **Displays** the data in a paginated, Bootstrap‑styled table using `pandas` and
   `dash_bootstrap_components`.  

This module is the primary entry point for viewing a user’s recently played songs within
the Spotify Analyzer application.

---

### analytics.py.md

# `pages.analytics` – Analytics Page

**File path**  
`/app/cloned_repos/spotifydata/pages/analytics.py`

The `analytics` module implements the *Analytics* page of the Spotify Analyzer web‑app.  
It is a Dash page that displays:

* A navigation bar with links to the other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).
* A dropdown to select a year.
* A dynamic container (`target_div`) that shows:
  * A table of the top 3 albums for the selected year.
  * Two bar charts – most popular and least popular songs for each month of that year.

---

## Imports & Dependencies

| Import | Purpose | Source |
|--------|---------|--------|
| `dash`, `dash.html`, `dash.dcc`, `dash.callback`, `dash.dependencies.Input`, `dash.dependencies.Output` | Core Dash components and callback decorators. | `dash` package |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (Navbar, Table). | `dash_bootstrap_components` package |
| `pandas as pd` | Data manipulation and DataFrame creation. | `pandas` package |
| `postgres` | Database helper functions (`get_years`, `get_albums_for_year`, `get_popular_for_year`). | Local module `postgres.py` |

> **Why these dependencies exist**  
> *Dash* provides the web UI framework.  
> *Bootstrap* gives a ready‑made navigation bar and table styling.  
> *Pandas* is used to convert raw tuples from PostgreSQL into a DataFrame for easy rendering.  
> The `postgres` module contains all SQL helpers that fetch the data needed for the analytics.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* Registers this module as a Dash page.  
* The URL pattern includes a `<username>` placeholder that is passed to `layout` and the callback.

---

## `layout(username=None)`

```python
def layout(username = None):
    years  = list(postgres.get_years())
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
        html.Div([dcc.Dropdown([year[0] for year in years], placeholder='Select year', id='year_drop')],
                 style={'margin':'0 500px',"padding-top":'20px'}),
        html.Div(children=[], id='target_div', style={'margin':'30px 200px'})
    ])
```

### What it does

1. **Fetch available years** – `postgres.get_years()` returns a list of tuples like `[(2020,), (2021,), …]`.  
2. **Build navigation bar** – `dbc.NavbarSimple` contains links that keep the current `username` in the URL.  
3. **Year selector** – a `dcc.Dropdown` with the list of years.  
4. **Result container** – an empty `Div` (`id='target_div'`) that will be populated by the callback.

### Interaction with the rest of the system

* The `layout` function is called by Dash when the user navigates to `/analytics/<username>`.  
* The `username` is used only for constructing navigation links; the analytics data is independent of the user (the database is shared).

---

## `analytics_display(value)`

```python
@callback(
    Output('target_div','children'),
    [Input('year_drop','value')]
)
def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)
        ...
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results", ...)]
```

### Callback flow

| Step | Action | Data Source | Notes |
|------|--------|-------------|-------|
| 1 | User selects a year in the dropdown (`year_drop`). | UI | Triggers callback. |
| 2 | `postgres.get_albums_for_year(value)` | PostgreSQL | Returns tuples `(album_name, song_count)` for the selected year. |
| 3 | `postgres.get_popular_for_year(value, 'desc')` | PostgreSQL | Returns tuples `(song_name, popularity, month)` sorted descending. |
| 4 | Build `most_pop_list` & `most_names_list` | Loop over months 1‑12 | For each month, find the song with the highest popularity. |
| 5 | Build `most_popular` graph | `dcc.Graph` | Bar chart with months on x‑axis and popularity on y‑axis. |
| 6 | `postgres.get_popular_for_year(value, 'asc')` | PostgreSQL | Same as step 3 but ascending. |
| 7 | Build `least_pop_list` & `least_names_list` | Loop over months 1‑12 | For each month, find the song with the lowest popularity. |
| 8 | Build `least_popular` graph | `dcc.Graph` | Bar chart similar to step 5. |
| 9 | Convert `albums` to a `pandas.DataFrame` | `pd.DataFrame` | Columns: `ALBUM`, `SONGS COUNT`. |
|10 | Assemble final children list | `html.H2`, `dbc.Table`, `most_popular`, `least_popular` | Returned to `target_div`. |
|11 | If no year selected | Return a prompt message | `html.H1` with instructions. |

### Data processing details

* **Popularity calculation** – The code multiplies the raw popularity (`j[2]`) by 10 and adds 100.  
  This scaling is arbitrary but keeps the bar heights in a readable range.  
* **Month mapping** – `j[4]` holds the month number (1‑12).  
  The lists `most_pop_list` and `least_pop_list` are indexed by month‑1.  
* **Graph construction** – Each graph uses a single bar trace with `x=[1..12]`.  
  The `text` property holds the song name for tooltip display.

### Interaction with other modules

* **`postgres`** – All database queries are performed through this module.  
  The callback relies on `get_years`, `get_albums_for_year`, and `get_popular_for_year`.  
* **`pages.cred`** – After a user logs in, `cred.fetch_data` populates the database tables that `analytics_display` reads.  
* **`pages.liked_songs` & `pages.recents`** – These pages use the same navigation bar and share the same database schema.

---

## Usage Summary

1. **User logs in** → `pages.cred` fetches data and stores it in PostgreSQL.  
2. **User navigates** to `/analytics/<username>` → Dash calls `layout` to render the page.  
3. **User selects a year** → `analytics_display` callback runs, queries the database, and renders the table + graphs.  
4. **Navigation links** keep the user on the same `username` context across pages.

---

## Key Code Snippets

```python
# Register the page
dash.register_page(__name__, path_template='/analytics/<username>')

# Build the year dropdown
dcc.Dropdown([year[0] for year in years], placeholder='Select year', id='year_drop')

# Callback signature
@callback(
    Output('target_div','children'),
    [Input('year_drop','value')]
)
def analytics_display(value):
    ...
```

---

## Dependencies Recap

- **Dash** – UI framework and callback system.  
- **dash_bootstrap_components** – Styled navigation bar and tables.  
- **pandas** – DataFrame conversion for table rendering.  
- **postgres** – SQL helper functions that provide the data for analytics.

All dependencies are explicitly listed in the `external_dependencies` field of the JSON evidence. No other modules are required for `analytics.py` to function.

---

### index.py.md

# `index.py` – Application Bootstrap

**File path**: `/app/cloned_repos/spotifydata/index.py`

---

## Overview

`index.py` is the entry point for the Spotify Analyzer Dash application.  
It creates the Dash app instance, configures the external stylesheet, and
defines the top‑level layout that will host all page components.

```python
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html
import dash_bootstrap_components as dbc
import dash

app = Dash(__name__, external_stylesheets=[
           dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = html.Div([dash.page_container])

if __name__ == '__main__':
    app.run_server(debug=True)
```

---

## Dependencies

| Import | Why it exists | Functionality used |
|--------|---------------|--------------------|
| `from dash import Dash, html` | Provides the core Dash application class and HTML component factory. | `Dash` creates the app instance; `html` is used to build the root `Div`. |
| `import dash_bootstrap_components as dbc` | Supplies Bootstrap themes and components for styling. | `dbc.themes.BOOTSTRAP` is passed as an external stylesheet. |
| `import dash` | Needed for the `dash.page_container` placeholder. | `dash.page_container` is a special component that renders the current page registered via `dash.register_page`. |

> **Note**: The evidence shows no explicit `depends_on` or `used_by` relationships for `index.py`.  
> Therefore, any downstream modules that rely on the `app` instance are not captured in this data set.

---

## Usage

### 1. Application Creation

```python
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True
)
```

- **`__name__`**: Identifies the module name for Dash.
- **`external_stylesheets`**: Loads the Bootstrap theme for consistent styling across all pages.
- **`use_pages=True`**: Enables Dash’s multi‑page feature, allowing the app to automatically discover pages registered with `dash.register_page`.

### 2. Root Layout

```python
app.layout = html.Div([dash.page_container])
```

- The root layout is a single `Div` that contains `dash.page_container`.  
- `dash.page_container` is a placeholder that Dash replaces with the layout of the currently active page (e.g., `/tools/<username>`, `/liked/<username>`, etc.).

### 3. Running the Server

```python
if __name__ == '__main__':
    app.run_server(debug=True)
```

- When executed directly (`python index.py`), the Dash development server starts on `http://127.0.0.1:8050/`.  
- `debug=True` enables hot‑reloading and detailed error messages during development.

---

## Interaction with Other Modules

- **Page Modules** (`pages.*`): Each page module registers itself with `dash.register_page`.  
  When a user navigates to a URL that matches a registered page, Dash automatically renders that page’s layout inside `dash.page_container`.  
  The `index.py` file does not directly import or call these modules; it relies on Dash’s page discovery mechanism.

- **Shared `app` Instance**:  
  If any other module imports `index` and accesses `index.app`, it can add callbacks, modify the layout, or register additional components.  
  However, the current evidence does not show any such imports.

---

## Summary

- `index.py` bootstraps the Dash application with Bootstrap styling and multi‑page support.  
- It defines a minimal root layout that delegates rendering to the page system.  
- No explicit dependencies or downstream usage are recorded in the provided evidence, but the file serves as the central hub that ties together all page modules via Dash’s page container.

---

### tools.py.md

# `pages.tools` – Tool Page for the Spotify Analyzer

**File path**  
`/app/cloned_repos/spotifydata/pages/tools.py`

---

## Overview

`pages.tools` is a Dash page that provides a simple navigation bar and a greeting for a logged‑in user.  
It is registered with Dash using a dynamic URL template (`/tools/<username>`), so the page can be accessed as:

```
http://localhost:8050/tools/<username>
```

The page is the landing spot after a user logs in and fetches their Spotify data.

---

## Imports & External Dependencies

| Import | Purpose | Why it exists |
|--------|---------|---------------|
| `dash` | Core Dash framework | Provides `dash.register_page` and the `callback` decorator. |
| `dash.html` | HTML component factory | Used to create `<div>`, `<h1>`, `<h5>` elements. |
| `dash_bootstrap_components` (aliased as `dbc`) | Bootstrap‑styled components | Supplies `NavbarSimple`, `NavItem`, and `NavLink` for a responsive navigation bar. |

> **Note:** No other modules import `pages.tools`, and it is not referenced by any other part of the codebase (`used_by` is empty).

---

## Page Registration

```python
dash.register_page(__name__, path_template='/tools/<username>')
```

- **`__name__`** – Registers this module as a Dash page.
- **`path_template`** – Enables a dynamic segment (`<username>`) in the URL, which is passed to the `layout` function.

---

## `layout` Function

```python
def layout(username=None):
    ...
```

### Parameters

- `username` (str, optional) – The Spotify username extracted from the URL.  
  It defaults to `None` when the page is accessed without a username, but in practice the app always supplies it.

### Workflow

1. **Navigation Bar (`navbar`)**  
   - Built with `dbc.NavbarSimple`.  
   - Contains three navigation links:
     - **Liked Songs** → `/liked/<username>`
     - **Recents** → `/recents/<username>`
     - **Analytics** → `/analytics/<username>`
   - Uses `brand="Spotify Analyzer"` and a custom CSS class `box-form left`.

2. **User Greeting**  
   - `first_name` is extracted by splitting the `username` on `%20` (URL‑encoded space) and taking the first part.  
   - Two large white headings display `"Hello"` and the extracted first name.  
   - A smaller instruction heading tells the user to use the navigation links.

3. **Return Value**  
   - A top‑level `html.Div` containing the navbar and greeting.  
   - The outer div is styled with `{'width': '100vw'}` to span the full viewport width.

### Example Output

```html
<div style="width:100vw;">
  <div class="navbar-simple box-form left">
    <!-- Navigation links -->
  </div>
  <div style="padding-left:25px; padding-top:10px;">
    <h1 style="font-size:10vmax;color:white;">Hello</h1>
    <h1 style="font-size:10vmax;color:white;"><first_name></h1>
    <h5 style="color:white;">use the navigation links to access various features of the tool</h5>
  </div>
</div>
```

---

## Usage in the Application

- **Entry Point** – After a user logs in via `pages.cred`, the callback `button_on_clicked` redirects to `/tools/<username>`.  
- **Navigation** – The navbar links allow the user to jump to the Liked Songs, Recents, or Analytics pages, each of which also accepts the same `<username>` parameter.  
- **No Further Dependencies** – The module does not import or call any functions from other modules; it only builds UI components.

---

## Summary

- **Purpose** – Provide a welcoming, navigable landing page for a logged‑in Spotify user.  
- **Key Components** – Dash page registration, Bootstrap navbar, dynamic greeting.  
- **Dependencies** – `dash`, `dash.html`, `dash_bootstrap_components`.  
- **Integration** – Registered as `/tools/<username>` and used as the default landing page after login.  
- **No downstream consumers** – The module is self‑contained and not referenced by any other part of the codebase.

---

### cred.py.md

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

---

### postgres.py.md

# `postgres.py`

**File path:** `/app/cloned_repos/spotifydata/postgres.py`

The `postgres` module is the single source of truth for all interactions with the PostgreSQL database that backs the Spotify Analyzer web‑app.  
It abstracts away connection handling, SQL file loading, and bulk inserts so that the rest of the codebase can focus on business logic.

---

## External Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `psycopg2` | Provides the PostgreSQL driver. | `psycopg2.connect()` to open a connection. |
| `psycopg2.extras.execute_values` | Enables efficient bulk inserts. | `execute_values(cursor, query, values)` for `add_*_dict` functions. |

---

## Core Functions

| Function | Purpose | Parameters | Return Value | Side‑Effects |
|----------|---------|------------|--------------|--------------|
| `postgres_init(db='postgres', user='postgres', pw='admin', host='localhost', port='5432')` | Opens a new database connection. | Connection parameters (all optional). | `psycopg2.connection` | None |
| `create_liked_songs_table()` | Creates the `liked_songs` table. | None | None | Executes SQL from `sql/create_liked_songs.sql`. |
| `create_recent_songs_table()` | Creates the `recents` table. | None | None | Executes SQL from `sql/create_recent_songs.sql`. |
| `create_album_table()` | Creates the `album` table and returns all rows. | None | `list[tuple]` | Executes SQL from `sql/create_album_table.sql` and `sql/select_all_albums.sql`. |
| `create_artist_table()` | Creates the `artist` table. | None | None | Executes SQL from `sql/create_artist_table.sql`. |
| `select_unique_artists()` | Returns all distinct artist IDs. | None | `list[tuple]` | Executes SQL from `sql/select_unique_artist_ids.sql`. |
| `check_liked_songs(table)` | Checks the most recent `added_at` timestamp in a table. | `table` – name of the table (`'liked_songs'` or `'recents'`). | `(timestamp, bool)` – timestamp and a flag indicating if a row exists. | Executes `SELECT MAX(added_at)` on the given table. |
| `add_liked_songs_dict(songs, table)` | Bulk‑inserts a list of song dictionaries into the specified table. | `songs` – list of dicts; `table` – target table name. | None | Uses `execute_values` to insert rows; commits transaction. |
| `add_albums_dict(albums)` | Bulk‑inserts a list of album dictionaries into the `album` table. | `albums` – list of dicts. | None | Uses `execute_values`; commits. |
| `add_artists_dict(artists)` | Bulk‑inserts a list of artist dictionaries into the `artist` table. | `artists` – list of dicts. | None | Uses `execute_values`; commits. |
| `select_unique_albums()` | Returns all distinct album IDs. | None | `list[tuple]` | Executes SQL from `sql/select_unique_album_ids.sql`. |
| `select_liked_songs(beg, end='all')` | Retrieves a slice of the `liked_songs` table. | `beg` – start index; `end` – end index or `'all'`. | `list[tuple]` | Executes SQL from `sql/view_liked_songs.sql`. |
| `select_recent_songs(beg, end='all')` | Retrieves a slice of the `recents` table. | `beg` – start index; `end` – end index or `'all'`. | `list[tuple]` | Executes SQL from `sql/view_recents.sql`. |
| `get_years()` | Returns all years present in the data. | None | `list[tuple]` | Executes SQL from `sql/get_years.sql`. |
| `get_albums_for_year(year)` | Returns albums for a specific year. | `year` – integer year. | `list[tuple]` | Executes SQL from `sql/get_albums.sql` with `year` interpolated. |
| `get_popular_for_year(year, flag)` | Returns popular songs for each month of a year. | `year` – integer; `flag` – `'asc'` or `'desc'` for ordering. | `list[tuple]` | Loops over months, executing SQL from `sql/get_popular.sql` with parameters. |

> **Note**  
> All SQL files are read with `open('sql/...').read()` relative to the project root.  
> Every function commits the transaction and closes the cursor and connection to avoid leaks.

---

## How the Module Is Used

| Module | How it uses `postgres` | What it achieves |
|--------|-----------------------|------------------|
| `pages.cred` | *Creates tables*, *checks for new data*, *inserts* liked songs, recents, artists, and albums. | Persists fresh Spotify data and avoids duplicates. |
| `pages.cred.fetch_data` | Same as above, but extracted into a helper function. | Allows the callback to trigger data fetching without duplicating logic. |
| `pages.liked_songs` | Calls `select_liked_songs` to paginate and display liked songs. | Provides the UI for browsing liked songs. |
| `pages.recents` | Calls `select_recent_songs` to paginate and display recent plays. | Provides the UI for browsing recent songs. |
| `pages.analytics` | Calls `get_years`, `get_albums_for_year`, and `get_popular_for_year` to build charts. | Supplies data for analytics dashboards. |
| `pages.analytics.analytics_display` | Same as above, but inside a callback. | Dynamically updates the analytics view when a year is selected. |

---

## Typical Workflow

1. **User logs in** → `pages.cred.fetch_data` is invoked.  
2. **Tables are created** (if they don't exist) via `create_*_table` functions.  
3. **Existing data is checked** with `check_liked_songs` to avoid re‑inserting older entries.  
4. **New data is inserted** using `add_*_dict` functions.  
5. **UI pages** (`liked_songs`, `recents`, `analytics`) query the database through `select_*` or `get_*` functions to render tables and charts.

---

## Design Rationale

- **Separation of concerns** – All database logic lives in one module, keeping the UI code clean.  
- **Bulk inserts** – `execute_values` dramatically speeds up data ingestion compared to row‑by‑row inserts.  
- **SQL file separation** – Keeps complex queries in dedicated `.sql` files, making them easier to maintain and test.  
- **Pagination support** – `select_*_songs` accept slice parameters, enabling efficient paging in the UI.  
- **Duplication guard** – `check_liked_songs` and `select_unique_*` functions prevent re‑processing the same data.

---

## Things to Watch

- **File paths** – The module assumes the `sql/` directory is located relative to the project root. If the working directory changes, SQL file loading will fail.  
- **Connection parameters** – Default credentials (`postgres`/`admin`) are hard‑coded; adjust `postgres_init` if you use a different database setup.  
- **Error handling** – The current implementation does not catch database errors; consider adding try/except blocks for production use.  
- **SQL injection** – The module escapes single quotes manually in `add_*_dict`; using parameterized queries would be safer.  

---

## Summary

`postgres.py` is the backbone of the Spotify Analyzer’s data persistence layer.  
It provides a clean API for creating tables, inserting bulk data, and querying for analytics, all while keeping the rest of the application focused on presentation and user interaction.

---

### liked_songs.py.md

# `pages.liked_songs` – Liked Songs Page

**File path:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer web‑app.  
It is a Dash page that displays a paginated table of the user’s liked songs
stored in a PostgreSQL database.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Page registration** | `dash.register_page(__name__, path_template='/liked/<username>')` registers the page with a dynamic `<username>` segment. |
| **Layout** | `layout(username=None)` builds the page layout: a navigation bar, a pagination slider, and a container for the song table. |
| **Callback** | `pages(active_page, max)` updates the table whenever the pagination slider changes. |
| **Dependencies** | Relies on the local `postgres` module to fetch data, and on Dash, Dash‑Bootstrap‑Components, Pandas, and the standard `math` library. |

---

## Imports & External Dependencies

```python
from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html
import dash
import pandas as pd
import postgres
import math
```

* **Dash** – Core framework for building the web UI.
* **Dash‑Bootstrap‑Components** – Provides Bootstrap‑styled components (e.g., `NavbarSimple`, `Table`).
* **Dash dependencies** – `Input`, `Output`, `State` are used to wire the callback.
* **Pandas** – Converts query results into a DataFrame for easy table rendering.
* **Postgres** – Custom module that exposes `select_liked_songs` for database access.
* **Math** – `ceil` is used to calculate the number of pagination pages.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* Registers this module as a Dash page.
* The URL pattern `/liked/<username>` allows the page to be accessed for any Spotify username.

---

## Layout Function

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

### Why the dependencies exist

| Dependency | Reason |
|------------|--------|
| `postgres` | Provides `select_liked_songs` to fetch liked songs from the database. |
| `math` | `ceil` calculates the number of pages needed for pagination. |
| `dash_bootstrap_components` | Builds a Bootstrap‑styled navigation bar. |
| `dash` / `dash.dependencies` | Creates the slider and defines the callback wiring. |
| `pandas` | Not used directly in `layout`, but imported for consistency with the rest of the module. |

### How the layout works

1. **Data fetch** – Calls `postgres.select_liked_songs(0)` to get all liked songs.  
   *The function returns a list of tuples; the length determines pagination.*

2. **Pagination** – With a fixed `page_size` of 50, the number of pages is computed.

3. **Navigation bar** – Provides links to other pages (`Recents`, `Analytics`, `Back`) with URLs that include the current `username`.

4. **Slider** – A `dcc.Slider` with id `Pagination` lets the user choose a page number.  
   *`marks` are generated for each page.*

5. **Table container** – An empty `html.Div` with id `liked_table` will be populated by the callback.

---

## Callback – `pages`

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

### Why the dependencies exist

| Dependency | Reason |
|------------|--------|
| `postgres` | `select_liked_songs(beg, end)` retrieves the appropriate slice of liked songs for the requested page. |
| `pandas` | Converts the list of tuples into a DataFrame for easy manipulation and rendering. |
| `dash_bootstrap_components` | `dbc.Table.from_dataframe` creates a Bootstrap‑styled table from the DataFrame. |
| `dash.dependencies` | `Input` and `State` wire the slider value to the callback. |

### How the callback works

1. **Input** – The slider’s current value (`active_page`) triggers the callback.  
   The `max` state provides the total number of pages.

2. **Query** –  
   * If the user is on the last page (`active_page == max`), the query fetches all remaining songs starting from `(active_page * 50 - 50)` to the end.  
   * Otherwise, it fetches a fixed slice of 50 songs: from `(active_page * 50 - 50)` to `active_page * 50`.

3. **DataFrame** – The raw tuples are turned into a DataFrame with the specified column names.

4. **Column pruning** – `song_id` and `preview_url` are dropped because they are not needed for display.

5. **Table rendering** – `dbc.Table.from_dataframe` creates a styled table that is returned as the children of the `liked_table` div.

---

## Interaction with the Rest of the System

* **User Flow** – After logging in via `pages.cred`, the user is redirected to `/tools/<username>`.  
  From there, clicking “Liked Songs” navigates to `/liked/<username>`, which loads this page.

* **Data Source** – The liked songs are stored in the PostgreSQL table `liked_songs`.  
  The `postgres.select_liked_songs` function (defined in `postgres.py`) reads from this table.

* **Pagination** – The slider allows the user to navigate through the liked songs in chunks of 50.  
  The callback ensures that only the relevant slice is fetched and displayed.

---

## Summary

`pages.liked_songs` is a self‑contained Dash page that:

1. **Registers** itself with a dynamic URL.
2. **Builds** a navigation bar and pagination slider.
3. **Fetches** liked songs from a PostgreSQL database via the `postgres` module.
4. **Displays** the songs in a Bootstrap‑styled table, updating on slider changes.

All interactions are driven by Dash callbacks, and the module relies on the `postgres` helper for database access, `pandas` for data manipulation, and `dash_bootstrap_components` for UI styling.

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

**Purpose:** Initializes and runs a Dash web application using Bootstrap styling and page routing.

**Responsibilities:**
- Creates a Dash app instance with Bootstrap theme and page support.
- Defines the main layout to include the page container.
- Starts the development server when executed as the main module.

**Key Components:**
- `app (Dash instance)`
- `app.layout (html.Div containing dash.page_container)`

**Dependencies:** `dash`, `dash.Dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Entry point that launches the web interface for the Spotify data application, coordinating page rendering and styling.

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Error parsing summary response

**Role in System:** Unknown

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** This module implements the landing page of a Dash web application that authenticates a Spotify user, retrieves their music data, and stores it in a PostgreSQL database.

**Responsibilities:**
- Creates the login page layout with input fields and a submit button.
- Converts Spotify timestamp strings to Python datetime objects via `check_date`.
- Fetches liked songs, recent songs, artists, and albums from Spotify, processes them, and inserts new records into PostgreSQL tables.
- Defines a Dash callback that triggers data fetching on button click and redirects to the tools page.
- Handles incremental updates by comparing timestamps with existing database entries.
- 

**Key Components:**
- `layout()`
- `check_date(timestamp)`
- `fetch_data(username)`
- `button_on_clicked(n_clicks,value)`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State`, `dash.html`, `datetime.datetime`, `pandas`, `postgres`, `spotify`

**Role in System:** Serves as the entry point for user authentication and data ingestion, bridging the front‑end Dash interface with the back‑end Spotify API and PostgreSQL storage. It initiates the data pipeline that feeds subsequent analytical pages.

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's liked Spotify songs.

**Responsibilities:**
- Registers the '/liked/<username>' route and constructs the page layout with navigation and pagination controls.
- Retrieves liked songs from the PostgreSQL database via the postgres module.
- Transforms the retrieved data into a pandas DataFrame and renders it as a Bootstrap table.
- Handles pagination logic to fetch appropriate slices of data based on user interaction.
- Integrates navigation links to other pages (Recents, Analytics, Back).

**Key Components:**
- `layout(username=None)`
- `pages(active_page,max)`
- `postgres.select_liked_songs`
- `dbc.NavbarSimple`
- `dcc.Slider`
- `dbc.Table.from_dataframe`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the user-facing component of the Spotify Analyzer application, enabling users to view and navigate through their liked songs within the web interface.

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's most recent Spotify songs, including navigation links to other pages.

**Responsibilities:**
- Fetch recent song data from the PostgreSQL database
- Calculate pagination parameters and render a slider for page selection
- Generate a navigation bar linking to Liked Songs, Recents, Analytics, and Back pages
- Render the song table using Dash Bootstrap components
- Update the table contents dynamically based on slider input via a callback

**Key Components:**
- `layout(username=None)`
- `pages(active_page,max)`
- `navbar (dbc.NavbarSimple)`
- `dcc.Slider (Pagination)`
- `dbc.Table.from_dataframe`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the Recents view in the Spotify Analyzer web application, enabling users to browse their recent listening history with pagination and navigation to related analytics pages.

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Provides a user‑specific tools page for the Spotify Analyzer web app, featuring navigation links to liked songs, recents, and analytics.

**Responsibilities:**
- Registers the page with Dash using a dynamic URL template.
- Defines a layout function that builds a navbar and greeting header based on the supplied username.
- Generates navigation links pointing to other app sections for the current user.

**Key Components:**
- `layout(username=None) function`
- `NavbarSimple component with NavLinks`

**Dependencies:** `dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Serves as one of the main pages in the Dash application, enabling users to access different Spotify data features via a personalized interface.

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Provides a PostgreSQL data access layer for storing and retrieving Spotify data such as liked songs, recent songs, albums, and artists, and offers analytics queries.

**Responsibilities:**
- Establishes database connections via psycopg2
- Creates and manages tables for liked songs, recent songs, albums, and artists
- Inserts bulk data into tables using execute_values
- Retrieves data for display and analytics (e.g., unique artists/albums, song lists, yearly statistics)

**Key Components:**
- `postgres_init`
- `create_liked_songs_table`
- `create_recent_songs_table`
- `create_album_table`
- `create_artist_table`
- `select_unique_artists`
- `check_liked_songs`
- `add_liked_songs_dict`
- `add_albums_dict`
- `add_artists_dict`
- `select_unique_albums`
- `select_liked_songs`
- `select_recent_songs`
- `get_years`
- `get_albums_for_year`
- `get_popular_for_year`

**Dependencies:** `psycopg2`, `psycopg2.extras.execute_values`

**Used By:** `pages.analytics`, `pages.analytics.analytics_display`, `pages.analytics.layout`, `pages.cred`, `pages.cred.fetch_data`, `pages.liked_songs`, `pages.liked_songs.layout`, `pages.liked_songs.pages`, `pages.recents`, `pages.recents.layout`, `pages.recents.pages`

**Role in System:** Acts as the core data persistence layer, exposing CRUD and analytics functions to the UI and analytics pages, enabling data-driven features across the application.

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Provides a data access layer for Spotify, handling authentication and retrieval of recent plays, liked tracks, albums, and artists, then normalizing the data into dictionary structures.

**Responsibilities:**
- Authenticate a user via Spotify OAuth and return an access token.
- Fetch the user's most recent played tracks and return them as a list of items.
- Retrieve all tracks the user has saved (liked) in batches.
- Batch-fetch album details given a list of album IDs.
- Batch-fetch artist details given a list of artist IDs.
- Transform raw liked track data into a flat list of dictionaries with key metadata.
- Transform raw album data into a flat list of dictionaries with key metadata.
- Transform raw artist data into a flat list of dictionaries with key metadata.

**Key Components:**
- `spotify_init()`
- `recent_songs()`
- `get_liked_songs()`
- `get_albums()`
- `get_artists()`
- `process_liked_songs()`
- `process_albums()`
- `process_artists()`
- `username`
- `client_id`
- `client_secret`
- `redirect_uri`
- `scope`

**Dependencies:** `dotenv.load_dotenv`, `os`, `pandas`, `spotipy`

**Used By:** `pages.cred`, `pages.cred.fetch_data`

**Role in System:** Serves as the Spotify API client and data normalizer, supplying other application components (e.g., UI pages) with structured music data for display or further analysis.

---



---


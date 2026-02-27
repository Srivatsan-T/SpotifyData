# SpotifyData Codebase Overview

# Codebase Overview

**Total Modules:** 8

This document provides a comprehensive overview of all modules in the codebase.

---

## Module Summaries

### `index`

**File:** `/app/cloned_repos/spotifydata/index.py`  
**UID:** `index`

**Purpose:** Initializes and runs a Dash web application with Bootstrap styling and page routing.

**Responsibilities:**
- Creates a Dash app instance with Bootstrap theme and page support.
- Defines the app layout to include the page container.
- Starts the development server when executed as the main module.

**Key Components:**
- `app (Dash instance)`
- `app.layout (html.Div containing dash.page_container)`

**Dependencies:** `dash`, `dash_bootstrap_components`

**Role in System:** Entry point that launches the web interface for the Spotify data application, coordinating page rendering and styling.

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Provides a dynamic analytics page for a Spotify data web app, displaying yearly statistics such as most and least popular songs per month and top albums.

**Responsibilities:**
- Creates the page layout with navigation and a year selection dropdown.
- Registers the page with Dash routing.
- Handles user input via a callback to fetch data from the PostgreSQL backend.
- Generates bar graphs for monthly popularity and a table of top albums.
- Returns appropriate UI components based on user interaction.

**Key Components:**
- `layout(username=None) – constructs the page layout and navigation.`
- `analytics_display(value) – Dash callback that builds graphs and tables when a year is selected.`
- `Uses postgres.get_years(), postgres.get_albums_for_year(), postgres.get_popular_for_year() for data retrieval.`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`

**Role in System:** Serves as the analytics view within the Dash application, enabling users to explore yearly Spotify listening trends and album popularity.

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** Provides the landing page for a Dash application that authenticates a Spotify user, fetches their music data, and stores it in a PostgreSQL database.

**Responsibilities:**
- Creates the login UI layout and handles navigation via URL changes.
- Converts Spotify timestamps to Python datetime objects.
- Fetches liked songs, recent songs, artists, and albums from the Spotify API, processes them, and persists them in Postgres tables.
- Defines a callback that triggers data fetching on login and redirects to a user‑specific tools page.

**Key Components:**
- `layout()`
- `check_date(timestamp)`
- `fetch_data(username)`
- `button_on_clicked(n_clicks,value)`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State`, `dash.html`, `datetime.datetime`, `pandas`, `postgres`, `spotify`

**Role in System:** Serves as the entry point for user authentication and data ingestion, bridging the Dash UI with Spotify API calls and PostgreSQL persistence.

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Provides the "Liked Songs" page for the Spotify Analyzer web application, displaying a paginated table of a user’s liked tracks.

**Responsibilities:**
- Registers the page route '/liked/<username>' with Dash.
- Generates the page layout including navigation bar, pagination slider, and table placeholder.
- Handles pagination callbacks to fetch the appropriate slice of liked songs from the database.
- Transforms database rows into a pandas DataFrame and renders them as a Bootstrap table.
- Drops non‑display columns (song_id, preview_url) before rendering.

**Key Components:**
- `layout(username=None) – constructs the page layout.`
- `pages(active_page,max) – Dash callback that updates the table based on pagination.`
- `navbar – navigation bar with links to other pages.`
- `Pagination slider – controls page selection.`

**Dependencies:** `dash`, `dash_bootstrap_components`, `dash.dependencies`, `dash.html`, `pandas`, `postgres`, `math`

**Role in System:** Serves as a user‑facing page within the Dash application, interfacing with the PostgreSQL backend to present liked songs and enabling navigation to other analytical views.

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's most recent songs from a PostgreSQL database.

**Responsibilities:**
- Registers the '/recents/<username>' route with Dash.
- Generates the page layout including navigation bar and pagination slider.
- Handles pagination callbacks to query recent songs and render them in a Bootstrap table.
- Formats and cleans the data before display.
- Links to other user-specific pages such as Liked Songs, Analytics, and Tools.

**Key Components:**
- `layout(username=None) – constructs the page layout.`
- `pages(active_page,max) – callback that fetches and renders recent songs.`
- `navbar – navigation bar with links to other pages.`
- `Pagination slider – controls page selection.`
- `dbc.Table.from_dataframe – renders song data as a table.`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the user-facing interface for viewing recent listening history within the Spotify Analyzer web application, integrating data retrieval from PostgreSQL with Dash UI components.

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Provides a user‑specific tools page for the Spotify Analyzer web application, displaying navigation links and a personalized greeting.

**Responsibilities:**
- Registers the page with Dash using a dynamic URL template
- Creates a Bootstrap navbar with links to Liked Songs, Recents, and Analytics pages
- Generates a layout that greets the user by first name and offers navigation guidance

**Key Components:**
- `layout(username=None) function`
- `NavbarSimple component with NavLinks`

**Dependencies:** `dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Serves as a client‑side view in the Dash app, enabling users to access various analytical tools related to their Spotify data.

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Provides a lightweight data access layer for a Spotify analytics application, handling PostgreSQL connection setup and CRUD operations for liked songs, recent songs, albums, artists, and analytical queries.

**Responsibilities:**
- Establishes and returns PostgreSQL connections via psycopg2.
- Creates database tables by executing SQL scripts located in the sql/ directory.
- Inserts bulk data into tables using execute_values for efficiency.
- Retrieves and filters data for display and analytics, including time‑based queries.
- Offers helper functions for analytics such as year extraction and popularity metrics.
- Closes connections cleanly after each operation.

**Key Components:**
- `postgres_init()`
- `create_liked_songs_table()`
- `create_recent_songs_table()`
- `create_album_table()`
- `create_artist_table()`
- `select_unique_artists()`
- `check_liked_songs()`
- `add_liked_songs_dict()`
- `add_albums_dict()`
- `add_artists_dict()`
- `select_unique_albums()`
- `select_liked_songs()`
- `select_recent_songs()`
- `get_years()`
- `get_albums_for_year()`
- `get_popular_for_year()`
- `execute_values from psycopg2.extras`

**Dependencies:** `psycopg2`, `psycopg2.extras.execute_values`

**Used By:** `pages.analytics`, `pages.analytics.analytics_display`, `pages.analytics.layout`, `pages.cred`, `pages.cred.fetch_data`, `pages.liked_songs`, `pages.liked_songs.layout`, `pages.liked_songs.pages`, `pages.recents`, `pages.recents.layout`, `pages.recents.pages`

**Role in System:** Acts as the central database interface for the Spotify data analytics web application, enabling page modules to create tables, insert data, and query analytics without handling raw SQL or connection logic.

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Provides functions to authenticate with Spotify and retrieve recent plays, liked tracks, albums, and artists, then process the data into structured dictionaries for downstream use.

**Responsibilities:**
- Authenticate a user via Spotipy and return an access token.
- Fetch a user's most recent played tracks.
- Retrieve all tracks the user has saved (liked).
- Batch fetch album and artist details by IDs.
- Transform raw Spotify responses into flat dictionaries suitable for analysis or storage.

**Key Components:**
- `spotify_init()`
- `recent_songs()`
- `get_liked_songs()`
- `get_albums()`
- `get_artists()`
- `process_liked_songs()`
- `process_albums()`
- `process_artists()`
- `username, client_id, client_secret, redirect_uri, scope constants`

**Dependencies:** `dotenv.load_dotenv`, `os`, `pandas`, `spotipy`

**Used By:** `pages.cred`, `pages.cred.fetch_data`

**Role in System:** Acts as the data acquisition layer for Spotify data, exposing a clean API that other modules (e.g., pages.cred) can call to obtain and preprocess user listening information.

---



---

## Module Documentation

### analytics.py.md

# `pages.analytics` – Analytics Page

**File path**  
`/app/cloned_repos/spotifydata/pages/analytics.py`

The *Analytics* page is a Dash page that displays a year‑based analytics view for a Spotify user.  
It is registered with Dash’s page system and contains two main components:

| Component | Purpose |
|-----------|---------|
| `layout` | Builds the page layout (navbar, year selector, placeholder for results). |
| `analytics_display` | Callback that populates the placeholder with charts and tables when a year is chosen. |

Below is a developer‑friendly breakdown of the module, its dependencies, and how it is used in the application.

---

## 1. Module Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* **Why** – Registers the module as a Dash page that can be accessed via `/analytics/<username>`.  
* **What** – The `dash` package provides the `register_page` function that hooks the module into Dash’s routing system.

---

## 2. Imports & External Dependencies

| Import | Source | Reason |
|--------|--------|--------|
| `from dash import dcc, callback` | `dash` | `dcc` provides Dash core components (e.g., `Dropdown`, `Graph`). `callback` is a decorator for defining callbacks. |
| `import dash_bootstrap_components as dbc` | `dash_bootstrap_components` | Provides Bootstrap‑styled components (`NavbarSimple`, `Table`). |
| `from dash.dependencies import Input, Output` | `dash.dependencies` | Used to declare callback inputs/outputs. |
| `from dash import html` | `dash` | Provides HTML components (`Div`, `H1`, etc.). |
| `import pandas as pd` | `pandas` | Used to create DataFrames for tables. |
| `import postgres` | `postgres` | Custom module that exposes database helper functions (`get_years`, `get_albums_for_year`, `get_popular_for_year`). |

> **Note** – All external dependencies are listed in the `external_dependencies` field of the evidence.

---

## 3. `layout(username=None)`

```python
def layout(username=None):
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

1. **Fetches available years** – Calls `postgres.get_years()` to populate the year dropdown.  
2. **Builds a navigation bar** – Links to other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).  
3. **Creates the main layout** –  
   * A `Dropdown` (`id='year_drop'`) for selecting a year.  
   * An empty `Div` (`id='target_div'`) that will be filled by the callback.

### Why the dependency on `postgres` exists

`postgres.get_years()` queries the database for distinct years present in the user’s data.  
Without this call the dropdown would have no options, so the analytics page would be unusable.

### Interaction with downstream modules

* The page itself is not directly used by other modules in the evidence (`used_by` is empty).  
* However, the callback inside this module will be triggered by user interaction on the page, and the resulting UI elements will be rendered by Dash.

---

## 4. `analytics_display(value)`

```python
@callback(
    Output('target_div', 'children'),
    [Input('year_drop', 'value')]
)
def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)

        # Build most popular songs bar
        most_pop_list = [0]*12
        most_names_list = ['NONE']*12
        most_populars = postgres.get_popular_for_year(value, 'desc')
        for i in range(1,13):
            for j in most_populars:
                if j[4] == i:
                    most_pop_list[i-1] = j[2]*10 + 100
                    most_names_list[i-1] = j[0]
        most_popular = dcc.Graph(
            figure={'data': [{'x': list(range(1,13)), 'type':'bar', 'y':most_pop_list, 'text':most_names_list}],
                     'layout':{'title':'Most Popular Songs Graph'}}
        )

        # Build least popular songs bar
        least_pop_list = [0]*12
        least_names_list = ['NONE']*12
        least_populars = postgres.get_popular_for_year(value, 'asc')
        for i in range(1,13):
            for j in least_populars:
                if j[4] == i:
                    least_pop_list[i-1] = j[2]*10 + 100
                    least_names_list[i-1] = j[0]
        least_popular = dcc.Graph(
            figure={'data': [{'x': list(range(1,13)), 'type':'bar', 'y':least_pop_list, 'text':least_names_list}],
                     'layout':{'title':'Least Popular Songs Graph'}}
        )

        df = pd.DataFrame(albums, columns=['ALBUM', 'SONGS COUNT'])

        result = [
            html.H2("Your top 3 albums from that year are",
                    style={'color':'white','border-style':'solid','text-align':'center'}),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,
                                     index=False, style={'padding-top':'45px','text-align':'center'}),
            most_popular,
            least_popular
        ]
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results",
                        style={'border-style':'solid','font-size':'7vmax','color':'white','text-align':'center'})]
```

### What it does

* **Triggered** when the user selects a year from the dropdown (`year_drop`).  
* **Queries the database**:  
  * `postgres.get_albums_for_year(value)` – top albums for the selected year.  
  * `postgres.get_popular_for_year(value, 'desc')` – most popular songs.  
  * `postgres.get_popular_for_year(value, 'asc')` – least popular songs.  
* **Builds UI components**:  
  * Two bar charts (`dcc.Graph`) for most/least popular songs.  
  * A table of the top 3 albums (`dbc.Table`).  
  * A header (`html.H2`).  
* **Returns** a list of Dash components that replace the children of `target_div`.

### Why the dependency on `postgres` exists

The callback relies on three helper functions from the `postgres` module to fetch:

1. **Years** – for the dropdown (in `layout`).  
2. **Albums** – for the album table.  
3. **Popular songs** – for the bar charts.

Without these functions the analytics page would have no data to display.

### What functionality is imported or relied upon

| Function | Purpose |
|----------|---------|
| `postgres.get_years()` | Provides the list of years for the dropdown. |
| `postgres.get_albums_for_year(year)` | Returns a list of tuples `(album_name, song_count)` for the selected year. |
| `postgres.get_popular_for_year(year, flag)` | Returns a list of tuples `(song_name, popularity, month)` sorted by popularity (`'desc'` or `'asc'`). |

### Interaction with downstream modules

* The callback is **self‑contained** – it only interacts with the database via `postgres`.  
* The resulting UI components are rendered by Dash; no other module consumes the callback’s output.  
* The module is registered as a page, so the application’s main Dash app will automatically include it.

---

## 5. Summary of Dependencies

| Dependency | Reason | Functionality Used |
|------------|--------|--------------------|
| `dash` | Core Dash framework | `register_page`, `html` components |
| `dash_bootstrap_components` | Bootstrap styling | `NavbarSimple`, `Table` |
| `dash.dependencies` | Callback wiring | `Input`, `Output` |
| `pandas` | Data manipulation | `DataFrame` for tables |
| `postgres` | Database access | `get_years`, `get_albums_for_year`, `get_popular_for_year` |

> **Missing relationships** – The evidence shows no modules that *use* `pages.analytics`. The `used_by` list is empty, so this page is only registered and rendered by Dash itself.

---

## 6. Suggested Improvements

1. **Add a docstring** to the module and each function to explain purpose and parameters.  
2. **Type hints** for `value` in `analytics_display` (e.g., `int | None`).  
3. **Error handling** – guard against empty query results or database errors.  
4. **Refactor** the repeated logic for building the bar charts into a helper function.  
5. **Use relative URLs** instead of hard‑coded `http://localhost:8050/...` for navigation links.

---

## 7. Quick Reference

```python
# Register page
dash.register_page(__name__, path_template='/analytics/<username>')

# Layout
def layout(username=None):
    # Build navbar + dropdown + placeholder
    ...

# Callback
@callback(Output('target_div', 'children'), [Input('year_drop', 'value')])
def analytics_display(value):
    # Query DB, build charts & table, return components
    ...
```

**File**: `/app/cloned_repos/spotifydata/pages/analytics.py`  
**Primary role**: Provide a user‑friendly analytics view for a Spotify user’s yearly data.

---

### postgres.py.md

# `postgres.py` – PostgreSQL Data Layer

**File path:** `/app/cloned_repos/spotifydata/postgres.py`

This module provides a thin wrapper around PostgreSQL operations used throughout the Spotify Analyzer application.  
It handles:

* Connection creation (`postgres_init`)
* Table creation (`create_*_table`)
* Data insertion (`add_*_dict`)
* Data retrieval (`select_*`, `get_*`)

All functions use the **`psycopg2`** driver and the **`execute_values`** helper for bulk inserts.

---

## External Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `psycopg2` | PostgreSQL driver | `psycopg2.connect`, `cursor`, `commit`, `close` |
| `psycopg2.extras.execute_values` | Bulk insert helper | `execute_values` |

These imports are the only external dependencies of the module.

---

## Core Functions

Below is a summary of each public function, its purpose, parameters, return values, and how it is used by downstream modules.

### 1. `postgres_init`

```python
def postgres_init(db='postgres', user='postgres', pw='admin', host='localhost', port='5432'):
```

* **Purpose** – Create a new database connection using the supplied credentials.
* **Parameters** – Optional connection details; defaults target a local PostgreSQL instance.
* **Return** – `psycopg2.connection` object.
* **Used by** – Every other function in this module; called at the start of each operation.

---

### 2. Table Creation

| Function | SQL file | Return | Usage |
|----------|----------|--------|-------|
| `create_liked_songs_table` | `sql/create_liked_songs.sql` | `None` | Called by `pages.cred.fetch_data` to ensure the table exists before inserting liked songs. |
| `create_recent_songs_table` | `sql/create_recent_songs.sql` | `None` | Called by `pages.cred.fetch_data` to create the recents table. |
| `create_album_table` | `sql/create_album_table.sql` + `sql/select_all_albums.sql` | `list` of rows | Called by `pages.cred.fetch_data` to create the album table and retrieve all albums for deduplication. |
| `create_artist_table` | `sql/create_artist_table.sql` | `None` | Called by `pages.cred.fetch_data` to create the artist table. |

All functions open the corresponding SQL file, execute it, commit, and close the connection.

---

### 3. Data Retrieval

| Function | SQL file | Parameters | Return | Usage |
|----------|----------|------------|--------|-------|
| `select_unique_artists` | `sql/select_unique_artist_ids.sql` | – | `list` of tuples `(artist_id,)` | Used by `pages.cred.fetch_data` to avoid inserting duplicate artists. |
| `select_unique_albums` | `sql/select_unique_album_ids.sql` | – | `list` of tuples `(album_id,)` | Used by `pages.cred.fetch_data` to avoid duplicate albums. |
| `check_liked_songs(table)` | – | `table` name (`'liked_songs'` or `'recents'`) | `(max_added_at, True)` if rows exist, else `(None, False)` | Used by `pages.cred.fetch_data` to determine if new data needs to be inserted. |
| `select_liked_songs(beg, end='all')` | `sql/view_liked_songs.sql` | `beg` index, optional `end` | Slice of rows from the view | Used by `pages.liked_songs.layout` and `pages.liked_songs.pages` for pagination. |
| `select_recent_songs(beg, end='all')` | `sql/view_recents.sql` | `beg` index, optional `end` | Slice of rows from the view | Used by `pages.recents.layout` and `pages.recents.pages`. |
| `get_years()` | `sql/get_years.sql` | – | `list` of tuples `(year,)` | Used by `pages.analytics.layout` to populate the year dropdown. |
| `get_albums_for_year(year)` | `sql/get_albums.sql` | `year` | `list` of rows | Used by `pages.analytics.analytics_display` to show top albums. |
| `get_popular_for_year(year, flag)` | `sql/get_popular.sql` | `year`, `month`, `flag` (`'asc'`/`'desc'`) | `list` of rows | Called 12 times (once per month) by `pages.analytics.analytics_display` to build popularity graphs. |

All retrieval functions open the relevant SQL file, execute the query, fetch results, and close the connection.

---

### 4. Bulk Insert Helpers

| Function | Parameters | Return | Usage |
|----------|------------|--------|-------|
| `add_liked_songs_dict(songs, table)` | `songs` – list of dicts, `table` – target table name | `None` | Called by `pages.cred.fetch_data` to insert liked songs or recents. Uses `execute_values` for efficient bulk insert. |
| `add_albums_dict(albums)` | `albums` – list of dicts | `None` | Called by `pages.cred.fetch_data` to insert new albums. |
| `add_artists_dict(artists)` | `artists` – list of dicts | `None` | Called by `pages.cred.fetch_data` to insert new artists. |

Each function:

1. Opens a connection.
2. Prepares an `INSERT` statement with column names derived from the first dictionary.
3. Calls `execute_values` to insert all rows in a single operation.
4. Commits and closes the connection.

---

## Interaction with Downstream Modules

| Downstream Module | How it uses `postgres.py` | Key Functions |
|-------------------|--------------------------|---------------|
| `pages.cred` | Fetches Spotify data, creates tables, inserts data, and deduplicates. | `create_*_table`, `check_liked_songs`, `add_*_dict`, `select_unique_*` |
| `pages.liked_songs` | Displays liked songs with pagination. | `select_liked_songs` |
| `pages.recents` | Displays recent songs with pagination. | `select_recent_songs` |
| `pages.analytics` | Provides analytics UI and graphs. | `get_years`, `get_albums_for_year`, `get_popular_for_year` |
| `pages.analytics.analytics_display` | Builds graphs and tables for a selected year. | `get_albums_for_year`, `get_popular_for_year` |

All these modules import the module simply as `import postgres`. The functions are called directly; no wrapper classes or additional abstractions are used.

---

## Design Notes

* **Connection per operation** – Each function creates and closes its own connection. This keeps the module stateless but may incur overhead for high‑frequency calls.
* **SQL files** – The module relies on external `.sql` files located in a `sql/` directory. The files are read with `open(...).read()`. If the files are missing or malformed, the corresponding function will raise an exception.
* **No type hints or docstrings** – The code is intentionally minimal; documentation is provided here instead of inline comments.
* **Error handling** – None of the functions catch exceptions; errors propagate to the caller. This is acceptable for a small application but should be considered for production use.

---

## Summary

`postgres.py` is the central data access layer for the Spotify Analyzer.  
It abstracts PostgreSQL operations into reusable functions that:

1. **Create tables** when the application starts or when new data arrives.
2. **Insert bulk data** from Spotify API responses.
3. **Retrieve data** for display and analytics.

By keeping all database logic in this module, the rest of the codebase can focus on business logic and UI rendering, while `postgres.py` handles persistence and query execution.

---

### index.py.md

# `index.py` – Application Bootstrap

**File path:** `/app/cloned_repos/spotifydata/index.py`

---

## Overview

`index.py` is the entry point for the Spotify Analyzer web application.  
It creates a **Dash** application instance, configures global styling, enables
Dash’s *pages* feature, and starts the development server.

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

| Import | Purpose | Why it exists in `index.py` |
|--------|---------|-----------------------------|
| `Dash` (from `dash`) | Creates the Dash application object. | The core of any Dash app. |
| `html` (from `dash`) | Provides HTML components (e.g., `Div`). | Used to build the root layout. |
| `dbc` (from `dash_bootstrap_components`) | Provides Bootstrap themes and components. | Supplies the `BOOTSTRAP` theme for consistent styling. |
| `dash` (top‑level module) | Exposes `dash.page_container` for page routing. | Enables the `use_pages=True` feature and renders the current page. |

> **Note:** No other modules in the codebase import or depend on `index.py`.  
> It is the sole entry point for running the application.

---

## How the Application Works

1. **App Instantiation**  
   ```python
   app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
   ```
   - `__name__` tells Dash the module name.
   - `external_stylesheets` applies the Bootstrap theme globally.
   - `use_pages=True` activates Dash’s built‑in page routing system.

2. **Root Layout**  
   ```python
   app.layout = html.Div([dash.page_container])
   ```
   - `dash.page_container` is a placeholder that automatically renders the
     component returned by the currently matched page (e.g., `pages.tools`,
     `pages.liked_songs`, etc.).
   - Wrapping it in `html.Div` gives a single root element for the app.

3. **Running the Server**  
   ```python
   if __name__ == '__main__':
       app.run_server(debug=True)
   ```
   - When executed directly (`python app.py`), the development server starts
     on `http://127.0.0.1:8050/`.
   - `debug=True` enables hot‑reloading and detailed error messages.

---

## Interaction with Other Modules

- **Pages** (`pages/*.py`)  
  Each page module registers itself with Dash using `dash.register_page`.  
  When a user navigates to a URL, `dash.page_container` automatically
  renders the corresponding page component.  
  `index.py` does **not** import these modules; Dash handles the discovery
  internally.

- **No downstream imports**  
  The `used_by` list for `index.py` is empty, indicating that no other
  module explicitly imports it.  
  Its sole responsibility is to bootstrap the app.

---

## Summary

`index.py` is a minimal, self‑contained bootstrap file that:

- Imports the necessary Dash and Bootstrap components.
- Creates a Dash app with global Bootstrap styling and page routing.
- Sets the root layout to render the current page.
- Starts the development server when run as the main script.

This file is the single point of entry for launching the Spotify Analyzer
application.

---

### tools.py.md

# `pages.tools` – Tools Page

**File path**: `/app/cloned_repos/spotifydata/pages/tools.py`

The `tools` module is a Dash page that provides a navigation bar and a simple greeting for a logged‑in Spotify user. It is registered with Dash’s page system and renders a layout that can be used by the main application.

---

## Overview

```python
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/tools/<username>')

def layout(username=None):
    ...
```

- **Purpose**: Render the “Tools” page for a specific Spotify username.
- **Key UI elements**:
  - A Bootstrap‑styled navigation bar (`dbc.NavbarSimple`) with links to *Liked Songs*, *Recents*, and *Analytics*.
  - A greeting that displays the user’s first name.
  - A simple layout wrapped in a full‑width `<div>`.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `dash` | Registers the page and provides the `Output`/`Input` decorators used elsewhere in the app. | `dash.register_page` |
| `dash.html` | Provides HTML components (`Div`, `H1`, `H5`, etc.). | `html.Div`, `html.H1`, `html.H5` |
| `dash_bootstrap_components` | Supplies Bootstrap‑styled components for the navigation bar. | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink` |

> **Note**: No external data‑access or business‑logic modules are imported here; the page is purely presentational.

---

## API

### `layout(username=None)`

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `username` | `str` | `None` | The Spotify username extracted from the URL. It may contain URL‑encoded spaces (`%20`). |

#### Returns
- `dash.html.Div`: A container that includes:
  - A navigation bar with links to other pages.
  - A greeting section that displays “Hello” and the user’s first name.
  - A subtitle encouraging navigation.

#### Implementation Details

```python
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs",
                                href=f'http://localhost:8050/liked/{username}',
                                id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents",
                                href=f'http://localhost:8050/recents/{username}',
                                id="Recents")),
        dbc.NavItem(dbc.NavLink("Analytics",
                                href=f'http://localhost:8050/analytics/{username}',
                                id="Analytics"))
    ],
    brand="Spotify Analyzer",
    brand_href="http://localhost:8050/",
    className='box-form left'
)

first_name = str(username).split('%20')[0]

return html.Div(
    [
        navbar,
        html.Div(
            [
                html.H1("Hello", style={'font-size':'10vmax','color':'white'}),
                html.H1(first_name, style={'font-size':'10vmax','color':'white'}),
                html.H5("use the navigation links to access various features of the tool",
                        style={'color':'white'})
            ],
            style={"padding-left":"25px","padding-top":'10px'}
        )
    ],
    style={'width':'100vw'}
)
```

- **Username parsing**: `first_name = str(username).split('%20')[0]` extracts the first part of the username before any URL‑encoded space.
- **Styling**: Inline CSS is used for font size, color, and padding.

---

## Usage

- **Page registration**: `dash.register_page` makes this module discoverable by the Dash app. The URL pattern `/tools/<username>` will trigger this layout.
- **Navigation**: The navbar links use the same `username` value to keep the user context when moving to *Liked Songs*, *Recents*, or *Analytics* pages.
- **Integration**: The main Dash application imports this module implicitly via the page registry; no explicit import is required elsewhere.

---

## Relationships

- **Dependencies**: None beyond the standard Dash and Bootstrap components.
- **Used by**: No explicit `used_by` entries are present in the evidence. The module is consumed by the Dash app’s page system.

---

## Summary

`pages.tools` is a lightweight, self‑contained page that:

1. Registers itself with Dash under `/tools/<username>`.
2. Builds a navigation bar linking to other user‑specific pages.
3. Greets the user by first name and encourages navigation.

It relies solely on Dash’s core and Bootstrap components, making it easy to maintain and extend.

---

### cred.py.md

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

---

### spotify.py.md

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

---

### liked_songs.py.md

# `liked_songs.py` – Page for Viewing Liked Songs

**File path**  
`/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer web app.  
It is a Dash page that displays a paginated table of the user’s liked songs
stored in a PostgreSQL database.

---

## 1. Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* **Why the dependency exists** – `dash.register_page` is used to register this
  module as a Dash page.  
* **What it does** – Exposes the page at the URL pattern `/liked/<username>`,
  where `<username>` is a dynamic segment that will be passed to the layout
  function.

---

## 2. Imports & External Dependencies

| Import | Purpose |
|--------|---------|
| `dash` | Core Dash framework. |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (Navbar, Table). |
| `dash.dependencies import Input, Output, State` | Callback wiring. |
| `dash.html` | HTML components (`Div`, `H1`, etc.). |
| `dash.dcc` | Dash Core Components (`Slider`). |
| `pandas as pd` | Data manipulation and DataFrame creation. |
| `postgres` | Custom module that provides database access functions. |
| `math` | `ceil` for page count calculation. |

All these imports are explicitly listed in the `external_dependencies` field of
the JSON evidence.

---

## 3. Layout Function

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

### What the layout does

* **Data fetch** – Calls `postgres.select_liked_songs(0)` to get the first
  slice of liked songs.  
  *Why*: The total count is needed to compute pagination.
* **Pagination** – Uses `math.ceil` to determine how many pages of 50 songs
  exist.
* **Navbar** – Provides navigation links to other pages (`Recents`, `Analytics`,
  `Back`). Each link includes the current `username` in the URL.
* **Slider** – A `dcc.Slider` component (`id='Pagination'`) that lets the user
  choose a page number. The slider’s `marks` are generated dynamically.
* **Table placeholder** – An empty `Div` (`id='liked_table'`) that will be
  populated by the callback.

### Interaction with other modules

* The layout is **used by** the Dash app when the user navigates to
  `/liked/<username>`.  
* It relies on the `postgres` module for data retrieval.

---

## 4. Callback – Pagination

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
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50,
                                                  active_page * 50)

    df = pd.DataFrame(liked_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

### Why the dependency exists

* **`postgres.select_liked_songs`** – Provides the slice of liked songs for
  the requested page.
* **`pandas`** – Converts the raw tuples into a DataFrame for easy
  manipulation.
* **`dash_bootstrap_components`** – Renders the DataFrame as a Bootstrap
  table.

### What the callback does

1. **Determine slice** – Calculates the offset and limit based on the
   `active_page`.  
   *If the user is on the last page, the end index is omitted to fetch all
   remaining rows.*
2. **Build DataFrame** – Creates a DataFrame with the specified column names,
   then drops the `song_id` and `preview_url` columns (they are not needed for
   display).
3. **Render table** – Uses `dbc.Table.from_dataframe` to produce a styled
   table that replaces the contents of the `liked_table` Div.

### Interaction with other modules

* The callback is **used by** the Dash app to update the UI when the slider
  changes.  
* It depends on the `postgres` module for data access and on `pandas` for
  data formatting.

---

## 5. Summary of Responsibilities

| Responsibility | Where it lives | Key functions / components |
|----------------|----------------|----------------------------|
| **Page registration** | `dash.register_page` | Exposes `/liked/<username>` |
| **Layout rendering** | `layout` | Builds navbar, slider, table placeholder |
| **Pagination logic** | `pages` callback | Fetches data slice, renders table |
| **Data access** | `postgres.select_liked_songs` | Retrieves liked songs from DB |
| **UI components** | `dash_bootstrap_components` | Navbar, Table |
| **Slider control** | `dcc.Slider` | Page selection |
| **Data formatting** | `pandas` | DataFrame creation & manipulation |

---

## 6. Notes on Missing Relationships

* The `used_by` list for `liked_songs` is empty in the evidence, meaning no
  other module explicitly imports or calls its functions.  
* The module is self‑contained: it only provides the layout and callback for
  the *Liked Songs* page.

---

## 7. Quick Reference

```python
# Register the page
dash.register_page(__name__, path_template='/liked/<username>')

# Layout
def layout(username=None):
    # fetch total liked songs
    liked_songs = postgres.select_liked_songs(0)
    # compute pagination
    number_of_pages = math.ceil(len(liked_songs) / 50)
    # build navbar, slider, table placeholder
    ...

# Callback to update table
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    # fetch slice of liked songs
    liked_songs = postgres.select_liked_songs(offset, limit)
    # build DataFrame and render table
    ...
```

This documentation should give developers a clear understanding of how
`liked_songs.py` fits into the overall Spotify Analyzer application,
what external modules it relies on, and how its UI components interact
with the database layer.

---

### recents.py.md

# `recents.py` – Recents Page

**File path**: `/app/cloned_repos/spotifydata/pages/recents.py`

This module implements the *Recents* page of the Spotify Analyzer Dash application.  
It displays a paginated table of the most recently played songs for a given user.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Page registration** | `dash.register_page(__name__, path_template='/recents/<username>')` registers this module as a Dash page that can be accessed via `/recents/<username>`. |
| **Layout** | `layout(username=None)` builds the page layout: a navigation bar, a pagination slider, and an empty container that will hold the table. |
| **Callback** | `pages(active_page, max)` is a Dash callback that updates the table whenever the pagination slider changes. |

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `postgres` | Provides the data source for recent songs. | `postgres.select_recent_songs(beg, end)` |
| `dash` | Core Dash framework. | `dash.register_page`, `dash.callback` |
| `dash.dcc` | Dash Core Components (slider). | `dcc.Slider` |
| `dash.html` | Dash HTML Components (divs, links). | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap styling for navbar and table. | `dbc.NavbarSimple`, `dbc.Table.from_dataframe` |
| `dash.dependencies` | Input/Output/State objects for callbacks. | `Input`, `Output`, `State` |
| `pandas` | Data manipulation and table rendering. | `pd.DataFrame` |
| `math` | Pagination calculation. | `math.ceil` |

> **Note**: The `used_by` list for this module is empty, but it is implicitly used by the Dash app as a registered page.

---

## How the Module Works

### 1. Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

- Registers the module as a page that accepts a `username` parameter in the URL.
- The `path_template` allows the app to route `/recents/<username>` to this module.

### 2. Layout Function

```python
def layout(username=None):
    recents = postgres.select_recent_songs(0)
    number_of_recent_songs = len(recents)
    page_size = 50
    number_of_pages = math.ceil(number_of_recent_songs / page_size)
    ...
    return html.Div([...], style={})
```

- **Data Fetch**: Calls `postgres.select_recent_songs(0)` to get all recent songs.  
  The result is a list of tuples returned from the database.
- **Pagination**: Calculates the number of pages (`number_of_pages`) based on a fixed page size of 50.
- **Navbar**: Uses `dbc.NavbarSimple` to provide navigation links to *Liked Songs*, *Recents*, *Analytics*, and *Back*.
- **Slider**: `dcc.Slider` with `id='Pagination'` lets the user pick a page.  
  `marks` are generated for each page number.
- **Table Container**: An empty `html.Div` with `id='recents_table'` will be populated by the callback.

### 3. Callback – Pagination

```python
@callback(
    Output('recents_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
    if active_page == max:
        recent_songs = postgres.select_recent_songs(active_page * 50 - 50)
    else:
        recent_songs = postgres.select_recent_songs(active_page * 50 - 50, active_page * 50)

    df = pd.DataFrame(recent_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

- **Inputs**:  
  - `active_page` – current slider value.  
  - `max` – maximum slider value (total pages).
- **Data Retrieval**:  
  - If the user is on the last page, fetch from `active_page*50-50` to the end.  
  - Otherwise, fetch a slice of 50 rows.
- **DataFrame**:  
  - Builds a `pandas.DataFrame` with the specified column names.  
  - Drops the `song_id` and `preview_url` columns because they are not needed for display.
- **Table Rendering**:  
  - Uses `dbc.Table.from_dataframe` to create a Bootstrap‑styled table.  
  - The table is returned as the children of the `recents_table` div.

---

## Usage in the Application

1. **Navigation**  
   Users navigate to `/recents/<username>` (e.g., `/recents/john_doe`).  
   The `layout` function renders the page with the navigation bar and pagination slider.

2. **Pagination Interaction**  
   When the slider value changes, the `pages` callback is triggered.  
   It queries the database for the appropriate slice of recent songs and updates the table.

3. **Data Source**  
   All data comes from the PostgreSQL database via the `postgres` module.  
   The `select_recent_songs` function returns rows in the order they were added to the `recents` table.

---

## Key Points for Developers

- **Extensibility**:  
  - To change the page size, modify `page_size = 50`.  
  - To add more columns to the table, update `column_names` and adjust the DataFrame accordingly.
- **Performance**:  
  - The callback fetches only the slice needed for the current page, keeping memory usage low.
- **Styling**:  
  - All UI elements use Bootstrap components (`dbc.NavbarSimple`, `dbc.Table`).  
  - Custom styles can be added via the `style` dictionaries or by extending the CSS classes.

---

## Summary

`recents.py` is a self‑contained Dash page that:

- Registers itself under `/recents/<username>`.
- Retrieves recent song data from PostgreSQL.
- Provides a paginated view using a slider.
- Renders the data in a Bootstrap‑styled table.

Its dependencies are strictly limited to the `postgres` module for data access and the Dash ecosystem for UI rendering.

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

**Purpose:** Initializes and runs a Dash web application with Bootstrap styling and page routing.

**Responsibilities:**
- Creates a Dash app instance with Bootstrap theme and page support.
- Defines the app layout to include the page container.
- Starts the development server when executed as the main module.

**Key Components:**
- `app (Dash instance)`
- `app.layout (html.Div containing dash.page_container)`

**Dependencies:** `dash`, `dash_bootstrap_components`

**Role in System:** Entry point that launches the web interface for the Spotify data application, coordinating page rendering and styling.

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Provides a dynamic analytics page for a Spotify data web app, displaying yearly statistics such as most and least popular songs per month and top albums.

**Responsibilities:**
- Creates the page layout with navigation and a year selection dropdown.
- Registers the page with Dash routing.
- Handles user input via a callback to fetch data from the PostgreSQL backend.
- Generates bar graphs for monthly popularity and a table of top albums.
- Returns appropriate UI components based on user interaction.

**Key Components:**
- `layout(username=None) – constructs the page layout and navigation.`
- `analytics_display(value) – Dash callback that builds graphs and tables when a year is selected.`
- `Uses postgres.get_years(), postgres.get_albums_for_year(), postgres.get_popular_for_year() for data retrieval.`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`

**Role in System:** Serves as the analytics view within the Dash application, enabling users to explore yearly Spotify listening trends and album popularity.

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** Provides the landing page for a Dash application that authenticates a Spotify user, fetches their music data, and stores it in a PostgreSQL database.

**Responsibilities:**
- Creates the login UI layout and handles navigation via URL changes.
- Converts Spotify timestamps to Python datetime objects.
- Fetches liked songs, recent songs, artists, and albums from the Spotify API, processes them, and persists them in Postgres tables.
- Defines a callback that triggers data fetching on login and redirects to a user‑specific tools page.

**Key Components:**
- `layout()`
- `check_date(timestamp)`
- `fetch_data(username)`
- `button_on_clicked(n_clicks,value)`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State`, `dash.html`, `datetime.datetime`, `pandas`, `postgres`, `spotify`

**Role in System:** Serves as the entry point for user authentication and data ingestion, bridging the Dash UI with Spotify API calls and PostgreSQL persistence.

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Provides the "Liked Songs" page for the Spotify Analyzer web application, displaying a paginated table of a user’s liked tracks.

**Responsibilities:**
- Registers the page route '/liked/<username>' with Dash.
- Generates the page layout including navigation bar, pagination slider, and table placeholder.
- Handles pagination callbacks to fetch the appropriate slice of liked songs from the database.
- Transforms database rows into a pandas DataFrame and renders them as a Bootstrap table.
- Drops non‑display columns (song_id, preview_url) before rendering.

**Key Components:**
- `layout(username=None) – constructs the page layout.`
- `pages(active_page,max) – Dash callback that updates the table based on pagination.`
- `navbar – navigation bar with links to other pages.`
- `Pagination slider – controls page selection.`

**Dependencies:** `dash`, `dash_bootstrap_components`, `dash.dependencies`, `dash.html`, `pandas`, `postgres`, `math`

**Role in System:** Serves as a user‑facing page within the Dash application, interfacing with the PostgreSQL backend to present liked songs and enabling navigation to other analytical views.

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's most recent songs from a PostgreSQL database.

**Responsibilities:**
- Registers the '/recents/<username>' route with Dash.
- Generates the page layout including navigation bar and pagination slider.
- Handles pagination callbacks to query recent songs and render them in a Bootstrap table.
- Formats and cleans the data before display.
- Links to other user-specific pages such as Liked Songs, Analytics, and Tools.

**Key Components:**
- `layout(username=None) – constructs the page layout.`
- `pages(active_page,max) – callback that fetches and renders recent songs.`
- `navbar – navigation bar with links to other pages.`
- `Pagination slider – controls page selection.`
- `dbc.Table.from_dataframe – renders song data as a table.`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the user-facing interface for viewing recent listening history within the Spotify Analyzer web application, integrating data retrieval from PostgreSQL with Dash UI components.

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Provides a user‑specific tools page for the Spotify Analyzer web application, displaying navigation links and a personalized greeting.

**Responsibilities:**
- Registers the page with Dash using a dynamic URL template
- Creates a Bootstrap navbar with links to Liked Songs, Recents, and Analytics pages
- Generates a layout that greets the user by first name and offers navigation guidance

**Key Components:**
- `layout(username=None) function`
- `NavbarSimple component with NavLinks`

**Dependencies:** `dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Serves as a client‑side view in the Dash app, enabling users to access various analytical tools related to their Spotify data.

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Provides a lightweight data access layer for a Spotify analytics application, handling PostgreSQL connection setup and CRUD operations for liked songs, recent songs, albums, artists, and analytical queries.

**Responsibilities:**
- Establishes and returns PostgreSQL connections via psycopg2.
- Creates database tables by executing SQL scripts located in the sql/ directory.
- Inserts bulk data into tables using execute_values for efficiency.
- Retrieves and filters data for display and analytics, including time‑based queries.
- Offers helper functions for analytics such as year extraction and popularity metrics.
- Closes connections cleanly after each operation.

**Key Components:**
- `postgres_init()`
- `create_liked_songs_table()`
- `create_recent_songs_table()`
- `create_album_table()`
- `create_artist_table()`
- `select_unique_artists()`
- `check_liked_songs()`
- `add_liked_songs_dict()`
- `add_albums_dict()`
- `add_artists_dict()`
- `select_unique_albums()`
- `select_liked_songs()`
- `select_recent_songs()`
- `get_years()`
- `get_albums_for_year()`
- `get_popular_for_year()`
- `execute_values from psycopg2.extras`

**Dependencies:** `psycopg2`, `psycopg2.extras.execute_values`

**Used By:** `pages.analytics`, `pages.analytics.analytics_display`, `pages.analytics.layout`, `pages.cred`, `pages.cred.fetch_data`, `pages.liked_songs`, `pages.liked_songs.layout`, `pages.liked_songs.pages`, `pages.recents`, `pages.recents.layout`, `pages.recents.pages`

**Role in System:** Acts as the central database interface for the Spotify data analytics web application, enabling page modules to create tables, insert data, and query analytics without handling raw SQL or connection logic.

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Provides functions to authenticate with Spotify and retrieve recent plays, liked tracks, albums, and artists, then process the data into structured dictionaries for downstream use.

**Responsibilities:**
- Authenticate a user via Spotipy and return an access token.
- Fetch a user's most recent played tracks.
- Retrieve all tracks the user has saved (liked).
- Batch fetch album and artist details by IDs.
- Transform raw Spotify responses into flat dictionaries suitable for analysis or storage.

**Key Components:**
- `spotify_init()`
- `recent_songs()`
- `get_liked_songs()`
- `get_albums()`
- `get_artists()`
- `process_liked_songs()`
- `process_albums()`
- `process_artists()`
- `username, client_id, client_secret, redirect_uri, scope constants`

**Dependencies:** `dotenv.load_dotenv`, `os`, `pandas`, `spotipy`

**Used By:** `pages.cred`, `pages.cred.fetch_data`

**Role in System:** Acts as the data acquisition layer for Spotify data, exposing a clean API that other modules (e.g., pages.cred) can call to obtain and preprocess user listening information.

---



---

### new.py.md

# `new.py`

**File Path**  
`/app/cloned_repos/spotifydata/new.py`

---

## Overview

`new.py` is a minimal module that currently contains only a single comment:

```python
#This is a new file
```

There are no functions, classes, or variables defined in this file. It serves as a placeholder or scaffold for future development.

---

## Dependencies

| Dependency | Type | Reason |
|------------|------|--------|
| None | – | The module contains no imports or external references. |

> **Note:** Because the module has no `depends_on` entries in the provided evidence, it does not rely on any other part of the codebase.

---

## Usage

| Downstream Module | Interaction | Role |
|-------------------|-------------|------|
| None | – | The module is not currently imported or referenced by any other module in the codebase. |

> **If you intend to use this module in the future, you can import it normally:**

```python
import new
```

---

## Extending `new.py`

If you plan to add functionality, consider the following guidelines:

1. **Add a proper docstring** at the module level to describe its purpose.
2. **Declare any imports** at the top of the file.
3. **Define functions or classes** that encapsulate the desired behavior.
4. **Update the `depends_on` and `used_by` metadata** accordingly so that documentation tools can reflect the new relationships.

---

## Summary

- **Purpose:** Placeholder for future code.
- **Dependencies:** None.
- **Current Usage:** None.

Feel free to expand this module as needed for your project.

---


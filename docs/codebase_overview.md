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


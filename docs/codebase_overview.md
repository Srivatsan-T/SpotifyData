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


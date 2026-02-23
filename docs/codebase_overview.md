# Codebase Overview

**Total Modules:** 9

This document provides a comprehensive overview of all modules in the codebase.

---

## Module Summaries

### `index`

**File:** `/app/cloned_repos/spotifydata/index.py`  
**UID:** `index`

**Purpose:** Initializes and runs a Dash web application with Bootstrap styling and page routing.

**Responsibilities:**
- Creates a Dash app instance with Bootstrap theme and page support.
- Defines the app layout to include the page container for multi-page navigation.
- Starts the development server when executed as the main module.
- Provides a single entry point for launching the web interface.

**Key Components:**
- `app (Dash instance)`
- `app.layout (html.Div containing dash.page_container)`

**Dependencies:** `dash`, `dash_bootstrap_components`

**Role in System:** Serves as the main application bootstrap, orchestrating the Dash framework, theming, and page routing for the Spotify data dashboard.

---

### `new`

**File:** `/app/cloned_repos/spotifydata/new.py`  
**UID:** `new`

**Purpose:** Placeholder module for testing continuous documentation.

**Role in System:** Serves as a test or example module within the project, likely used during development or documentation generation.

---

### `analytics`

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`  
**UID:** `pages.analytics`

**Purpose:** Provides a dynamic analytics dashboard for a Spotify user, displaying yearly statistics such as most and least popular songs and top albums.

**Responsibilities:**
- Renders the analytics page layout with navigation and year selection dropdown.
- Handles user interactions via a Dash callback to fetch data from the PostgreSQL database.
- Generates bar graphs for most and least popular songs and a table of top albums for the selected year.
- Formats and returns the visual components for display.
- Integrates with the Dash routing system to register the page path.
- 

**Key Components:**
- `layout(username=None) – constructs the page layout with navbar, dropdown, and target div.`
- `analytics_display(value) – Dash callback that queries postgres, builds graphs and tables, and returns them.`
- `postgres.get_years() – retrieves available years for the dropdown.`
- `postgres.get_albums_for_year(year) – fetches album data for a year.`
- `postgres.get_popular_for_year(year,order) – retrieves song popularity data.`
- `dcc.Graph – used to display bar charts.`
- `dbc.Table.from_dataframe – renders album table.`
- `dash.register_page – registers the page route.`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.html`, `dash_bootstrap_components`, `pandas`, `postgres`

**Role in System:** Serves as the analytics view within the Spotify Analyzer web application, enabling users to explore their listening data through interactive visualizations.

---

### `cred`

**File:** `/app/cloned_repos/spotifydata/pages/cred.py`  
**UID:** `pages.cred`

**Purpose:** Provides the landing page for a Dash application that authenticates a Spotify user, fetches their music data, processes it, and stores it in a Postgres database.

**Responsibilities:**
- Renders the login UI and handles user input via Dash components.
- Converts Spotify timestamps to Python datetime objects.
- Fetches liked songs, recent plays, artists, and albums from the Spotify API, processes the data, and persists it to Postgres tables.
- Defines a callback that triggers data fetching on login and redirects to a tools page.
- (Optional) Contains commented-out code for periodic data refresh via an interval component.
- 

**Key Components:**
- `layout()`
- `check_date(timestamp)`
- `fetch_data(username)`
- `button_on_clicked(n_clicks,value)`

**Dependencies:** `dash`, `dash.callback`, `dash.dcc`, `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State`, `dash.html`, `datetime`, `pandas`, `spotify`, `postgres`

**Role in System:** Acts as the entry point for user authentication and data ingestion, initializing the database with the user's Spotify data and routing to subsequent analytical tools.

---

### `liked_songs`

**File:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`  
**UID:** `pages.liked_songs`

**Purpose:** Provides a Dash page that displays a paginated table of a user's liked songs from Spotify, including navigation and pagination controls.

**Responsibilities:**
- Registers the '/liked/<username>' page with Dash.
- Builds the page layout with a navigation bar and pagination slider.
- Fetches liked songs from the PostgreSQL database and paginates the results.
- Renders the song data in a Bootstrap table via a callback.
- Handles user interaction to update the displayed page of songs.

**Key Components:**
- `layout(username=None) – constructs the page layout with navbar, slider, and table placeholder.`
- `pages(active_page,max) – Dash callback that queries liked songs, paginates, and returns a Bootstrap table.`
- `Imports: dash, dash_bootstrap_components, pandas, postgres, math, dash.dependencies (Input, Output, State).`

**Dependencies:** `dash`, `dash_bootstrap_components`, `pandas`, `math`, `postgres`

**Role in System:** Serves as the user-facing interface for viewing liked songs, integrating with the backend PostgreSQL data layer and the Dash front-end framework to provide interactive pagination and navigation within the Spotify Analyzer application.

---

### `recents`

**File:** `/app/cloned_repos/spotifydata/pages/recents.py`  
**UID:** `pages.recents`

**Purpose:** Provides a Dash web page that displays a paginated table of a user's most recent songs from a PostgreSQL database.

**Responsibilities:**
- Retrieves recent song data via postgres.select_recent_songs and calculates pagination details.
- Renders a navigation bar linking to other user pages (Liked Songs, Recents, Analytics, Back).
- Creates a layout with a slider for page selection and a placeholder for the song table.
- Defines a callback that updates the table based on the selected page, converting the data to a Bootstrap table.
- Handles page size logic and ensures the correct slice of data is fetched for each page.

**Key Components:**
- `layout(username=None) – constructs the page layout with navbar, slider, and table placeholder.`
- `pages(active_page,max) – callback that fetches and displays the appropriate slice of recent songs.`
- `postgres.select_recent_songs – external function used to query recent songs.`
- `dbc.Table.from_dataframe – renders the pandas DataFrame as a styled table.`

**Dependencies:** `postgres`, `dash`, `dash_bootstrap_components`, `pandas`, `math`

**Role in System:** Serves as the user-facing component for viewing recent songs within the Spotify Analyzer Dash application, integrating data retrieval, pagination, and UI rendering.

---

### `tools`

**File:** `/app/cloned_repos/spotifydata/pages/tools.py`  
**UID:** `pages.tools`

**Purpose:** Provides a user‑specific tools page for the Spotify Analyzer web app, featuring navigation links to liked songs, recents, and analytics.

**Responsibilities:**
- Registers the page with Dash using a username path template.
- Creates a navigation bar with links to other tool pages.
- Generates a personalized greeting using the supplied username.
- Returns the complete layout as a Dash HTML Div.
- Handles URL formatting for user navigation.
- 

**Key Components:**
- `layout(username=None) function – builds the page layout.`
- `navbar – a Dash Bootstrap Components NavbarSimple instance with NavLinks.`
- `first_name extraction – parses the username for display.`

**Dependencies:** `dash`, `dash.html`, `dash_bootstrap_components`

**Role in System:** Serves as one of the main pages in the Dash application, providing a central hub for users to access various Spotify data features.

---

### `postgres`

**File:** `/app/cloned_repos/spotifydata/postgres.py`  
**UID:** `postgres`

**Purpose:** Provides a data access layer for storing and retrieving Spotify-related data in a PostgreSQL database, including liked songs, recent songs, albums, and artists, and supports analytics queries.

**Responsibilities:**
- Initializes database connections and creates required tables
- Inserts bulk data for songs, albums, and artists
- Retrieves data slices for liked and recent songs
- Provides analytics helpers such as year lists, album listings, and monthly popularity stats

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

**Role in System:** Acts as the persistence layer for the application, enabling other modules (analytics, UI pages, credential fetchers) to interact with the PostgreSQL database without handling raw SQL or connection logic.

---

### `spotify`

**File:** `/app/cloned_repos/spotifydata/spotify.py`  
**UID:** `spotify`

**Purpose:** Provides authentication and data retrieval from the Spotify API, converting raw responses into structured dictionaries for use elsewhere in the application.

**Responsibilities:**
- Obtains OAuth tokens for a Spotify user via spotipy.
- Fetches recent plays, liked tracks, albums, and artists using the Spotify API.
- Transforms raw API responses into flat dictionaries suitable for downstream processing or storage.

**Key Components:**
- `spotify_init(username)`
- `recent_songs(token)`
- `get_liked_songs(token)`
- `get_albums(token,album_ids)`
- `get_artists(token,artist_ids)`
- `process_liked_songs(liked_songs)`
- `process_albums(albums)`
- `process_artists(artists)`

**Dependencies:** `dotenv.load_dotenv`, `os`, `pandas`, `spotipy`

**Used By:** `pages.cred`, `pages.cred.fetch_data`

**Role in System:** Serves as the data access layer for Spotify-related information, enabling other modules (e.g., credential handling and data fetching pages) to obtain and normalize user listening data.

---


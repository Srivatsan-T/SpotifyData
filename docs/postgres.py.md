# `postgres.py` – PostgreSQL Helper Module  
**File Path:** `/app/cloned_repos/spotify_data/postgres.py`

The `postgres` module is the single point of contact between the application and the PostgreSQL database.  
All database‑related logic (connection handling, table creation, data insertion, and query helpers) lives here, so the rest of the codebase can remain agnostic of the underlying SQL implementation.

---

## External Dependencies
| Dependency | Purpose |
|------------|---------|
| `psycopg2` | Low‑level PostgreSQL driver used to establish a connection and execute SQL statements. |
| `psycopg2.extras.execute_values` | Utility for bulk inserting rows efficiently (used in `add_*_dict` functions). |

---

## Core Functions

| Function | Signature | Purpose | Key Points |
|----------|-----------|---------|------------|
| `postgres_init` | `def postgres_init(db='postgres', user='postgres', pw='admin', host='localhost', port='5432')` | Creates and returns a new database connection. | Uses default credentials; can be overridden by passing arguments. |
| `create_liked_songs_table` | `def create_liked_songs_table()` | Executes the SQL file `sql/create_liked_songs.sql` to create the *liked_songs* table. | Commits the transaction and closes the connection. |
| `create_recent_songs_table` | `def create_recent_songs_table()` | Executes `sql/create_recent_songs.sql` to create the *recents* table. | Same pattern as above. |
| `create_album_table` | `def create_album_table()` | Creates the *album* table (`sql/create_album_table.sql`) **and** returns all rows (`sql/select_all_albums.sql`). | Useful for pre‑loading album data. |
| `create_artist_table` | `def create_artist_table()` | Creates the *artist* table (`sql/create_artist_table.sql`). | No data is returned. |
| `select_unique_artists` | `def select_unique_artists()` | Returns a list of unique artist IDs from the *artist* table (`sql/select_unique_artist_ids.sql`). | Used to avoid duplicate artist inserts. |
| `check_liked_songs` | `def check_liked_songs(table)` | Queries `SELECT MAX(added_at)` on the given table to determine if any rows exist. | Returns `(max_date, True)` if data exists, otherwise `(None, False)`. |
| `add_liked_songs_dict` | `def add_liked_songs_dict(songs, table)` | Bulk‑inserts a list of song dictionaries into the specified table. | Uses `execute_values` for performance; escapes single quotes in song names. |
| `add_albums_dict` | `def add_albums_dict(albums)` | Bulk‑inserts album dictionaries into the *album* table. | Escapes single quotes in album names. |
| `add_artists_dict` | `def add_artists_dict(artists)` | Bulk‑inserts artist dictionaries into the *artist* table. | Escapes single quotes in artist names. |
| `select_unique_albums` | `def select_unique_albums()` | Returns a list of unique album IDs (`sql/select_unique_album_ids.sql`). | Used to prevent duplicate album inserts. |
| `select_liked_songs` | `def select_liked_songs(beg, end='all')` | Retrieves all rows from the *liked_songs* view (`sql/view_liked_songs.sql`) and slices the result. | `beg` is the start index; `end` can be a slice end or `'all'`. |
| `select_recent_songs` | `def select_recent_songs(beg, end='all')` | Same as `select_liked_songs` but for the *recents* view (`sql/view_recents.sql`). |
| `get_years` | `def get_years()` | Executes `sql/get_years.sql` to fetch distinct years present in the data. | Returns a list of tuples `(year,)`. |
| `get_albums_for_year` | `def get_albums_for_year(year)` | Executes `sql/get_albums.sql` with the supplied year to fetch album statistics for that year. | Uses string formatting to inject the year. |
| `get_popular_for_year` | `def get_popular_for_year(year, flag)` | Loops over all 12 months, executing `sql/get_popular.sql` for each month and aggregating the results. | `flag` determines sort order (`'asc'` or `'desc'`). |

---

## How the Module Is Used

| Downstream Module | Interaction | Role of `postgres` |
|-------------------|-------------|--------------------|
| **`pages.cred`** | Calls `create_*_table` and `add_*_dict` to populate tables during data ingestion. | Provides a clean API for inserting Spotify data into the database. |
| **`pages.liked_songs`** | Calls `select_liked_songs` to fetch data for display. | Supplies the table data that the Dash callback renders. |
| **`pages.recents`** | Calls `select_recent_songs` for the same purpose. | Supplies recent play data to the UI. |
| **`pages.analytics`** | Calls `get_years`, `get_albums_for_year`, and `get_popular_for_year` to build analytics dashboards. | Supplies aggregated data for charts and tables. |
| **`pages.tools`** | No direct interaction. | N/A |
| **`spotify`** | No direct interaction. | N/A |

The module is deliberately *stateless*: each function opens a new connection, performs its operation, and closes the connection. This keeps the rest of the application simple and avoids connection‑leak issues.

---

## Why These Dependencies Exist

- **`psycopg2`** – The only Python library capable of communicating with PostgreSQL at the level required (executing raw SQL, handling transactions, etc.).  
- **`psycopg2.extras.execute_values`** – Provides a fast bulk‑insert helper that reduces round‑trips to the database. It is used in `add_liked_songs_dict`, `add_albums_dict`, and `add_artists_dict` to insert many rows efficiently.

---

## Usage Example

```python
# In a Dash callback or a data‑fetching routine
import postgres

# 1. Ensure tables exist
postgres.create_liked_songs_table()
postgres.create_recent_songs_table()
postgres.create_album_table()
postgres.create_artist_table()

# 2. Insert data
postgres.add_liked_songs_dict(song_dicts, 'liked_songs')
postgres.add_albums_dict(album_dicts)
postgres.add_artists_dict(artist_dicts)

# 3. Retrieve data for display
liked = postgres.select_liked_songs(0, 50)          # first 50 liked songs
recent = postgres.select_recent_songs(0, 50)        # first 50 recent songs
years = postgres.get_years()                       # available years
albums_2021 = postgres.get_albums_for_year(2021)   # album stats for 2021
popular_monthly = postgres.get_popular_for_year(2021, 'desc')
```

---

## Summary

- **Centralizes all PostgreSQL interactions** in a single module.  
- **Provides a clean, reusable API** for creating tables, inserting data, and querying aggregated results.  
- **Ensures data integrity** by checking for existing rows before inserting new data.  
- **Supports the Dash UI** by supplying the data required for tables, graphs, and analytics.  

The `postgres` module is the backbone of the data‑storage layer in this Spotify‑analysis application. All other modules rely on it for persistent storage and retrieval of user data.
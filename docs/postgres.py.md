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
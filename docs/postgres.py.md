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
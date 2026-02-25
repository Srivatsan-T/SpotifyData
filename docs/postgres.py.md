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
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
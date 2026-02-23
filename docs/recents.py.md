# `recents.py` – Recents Page

**Location**: `/app/cloned_repos/spotify_data/pages/recents.py`

The *Recents* page is a Dash component that displays a paginated table of the most recently played songs for a given user.  
It is part of the `pages` package and is registered as a dynamic route (`/recents/<username>`).

---

## 1. Overview

| Feature | Description |
|---------|-------------|
| **Route** | `/recents/<username>` |
| **Purpose** | Show a table of recent songs with pagination. |
| **Navigation** | Links to *Liked Songs*, *Recents*, *Analytics*, and *Back* pages. |
| **Data Source** | PostgreSQL table `recents` accessed via `postgres.select_recent_songs`. |
| **UI Components** | `dcc.Slider` for page selection, `dbc.Table` for data display. |

---

## 2. Dependencies

| Module | Why it is needed | Key functionality used |
|--------|------------------|------------------------|
| `dash` | Registers the page and provides the Dash app context. | `dash.register_page` |
| `dash_bootstrap_components` | Provides Bootstrap‑styled components (navbar, table). | `dbc.NavbarSimple`, `dbc.Table.from_dataframe` |
| `dash.dependencies` | Handles reactive callbacks. | `Input`, `Output`, `State` |
| `dash.html` | Builds the page layout with HTML tags. | `html.Div`, `html.H1`, etc. |
| `dash.dcc` | Provides interactive components. | `dcc.Slider` |
| `pandas` | Transforms raw tuples into a DataFrame for rendering. | `pd.DataFrame` |
| `math` | Calculates pagination limits. | `math.ceil` |
| `postgres` | Executes SQL queries to fetch recent songs. | `postgres.select_recent_songs` |

> **Note**: All imports are explicitly listed in the file; no implicit or dynamic imports are used.

---

## 3. API

### 3.1 `layout(username=None)`

```python
def layout(username=None):
    ...
```

* **Purpose** – Returns the Dash layout for the Recents page.
* **Parameters** – `username` (optional string) used only for constructing navigation URLs.
* **Returns** – `html.Div` containing:
  * A Bootstrap navbar (`dbc.NavbarSimple`) with links to other pages.
  * A `dcc.Slider` (`id='Pagination'`) for selecting the page number.
  * An empty `html.Div` (`id='recents_table'`) that will be populated by the callback.

**Key Steps**

1. **Data Retrieval**  
   ```python
   recents = postgres.select_recent_songs(0)
   ```
   Fetches all recent songs from the database.

2. **Pagination Calculation**  
   ```python
   number_of_recent_songs = len(recents)
   page_size = 50
   number_of_pages = math.ceil(number_of_recent_songs / page_size)
   ```

3. **Navbar Construction** – Uses `dbc.NavbarSimple` with links that embed the `username`.

4. **Slider Setup** –  
   ```python
   dcc.Slider(
       id='Pagination',
       min=1,
       max=number_of_pages,
       step=1,
       value=1,
       marks={i: str(i) for i in range(1, number_of_pages + 1)}
   )
   ```

5. **Return Layout** – The outer `html.Div` has an empty style dictionary (`style={}`).

---

### 3.2 `pages(active_page, max)`

```python
@callback(
    Output('recents_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    ...
```

* **Purpose** – Callback that updates the table whenever the pagination slider changes.
* **Parameters**  
  * `active_page` – Current slider value (selected page).  
  * `max` – Maximum slider value (total pages), provided as `State`.
* **Returns** – A `dbc.Table` component rendered from a `pandas.DataFrame`.

**Logic**

1. **Column Names** – Fixed list used to label the DataFrame columns.
   ```python
   column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
   ```

2. **Data Fetching**  
   * If the user is on the last page (`active_page == max`), fetch all rows from the start of that page to the end:
     ```python
     recent_songs = postgres.select_recent_songs(active_page * 50 - 50)
     ```
   * Otherwise, fetch a slice of 50 rows:
     ```python
     recent_songs = postgres.select_recent_songs(active_page * 50 - 50, active_page * 50)
     ```

3. **DataFrame Construction**  
   ```python
   df = pd.DataFrame(recent_songs, columns=column_names)
   df = df.drop(['song_id', 'preview_url'], axis=1)
   ```

4. **Table Rendering**  
   ```python
   return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
   ```

---

## 4. Usage Flow

1. **User navigates** to `/recents/<username>`.  
2. Dash calls `layout(username)` to render the page.  
3. The slider is displayed with the correct number of pages.  
4. When the user moves the slider, the `pages` callback is triggered.  
5. The callback fetches the appropriate slice of recent songs, builds a DataFrame, and returns a Bootstrap table that replaces the contents of `recents_table`.

---

## 5. Interaction with Other Modules

| Module | Interaction |
|--------|-------------|
| `postgres` | `recents.py` calls `postgres.select_recent_songs` to read data. |
| `pages.liked_songs` | Shares the same navigation structure and pagination logic. |
| `pages.analytics` | Shares the navigation bar but no direct data dependency. |
| `pages.tools` | Provides the “Back” link to return to the tools page. |

> **Dependency Data** – The only explicit dependency listed for `recents.py` is the `postgres` module. No other modules import or depend on `recents.py`.

---

## 6. Design Decisions & Rationale

| Decision | Reason |
|----------|--------|
| **Pagination via `dcc.Slider`** | Provides a simple, intuitive UI for page selection without requiring a separate pagination component. |
| **Fixed page size (50)** | Matches the page size used in the liked songs page, ensuring consistent UX. |
| **Dropping `song_id` and `preview_url`** | These fields are not needed for display; removing them keeps the table concise. |
| **Using `dbc.Table.from_dataframe`** | Leverages Pandas’ DataFrame to quickly generate a styled table without manual column handling. |
| **`math.ceil` for page count** | Guarantees that any remainder songs are shown on an additional page. |
| **`postgres.select_recent_songs` with optional `beg`/`end`** | Allows efficient slicing of the database result set, reducing memory usage. |

---

## 7. Potential Extensions

* **Sorting** – Add column headers that allow sorting by popularity or album.  
* **Filtering** – Provide a search box to filter songs by name or artist.  
* **Caching** – Cache the DataFrame for a page to reduce database load on repeated slider moves.  
* **Error Handling** – Gracefully handle database connection failures or empty result sets.  

---

## 8. Summary

`recents.py` is a lightweight, self‑contained Dash page that:

1. **Registers** itself at `/recents/<username>`.
2. **Builds** a navigation bar and a pagination slider.
3. **Fetches** recent songs from PostgreSQL.
4. **Displays** the data in a Bootstrap‑styled table.

All functionality is explicitly defined in the file, with clear dependencies on `dash`, `dash_bootstrap_components`, `pandas`, `math`, and the custom `postgres` module. The page is designed to be consistent with the rest of the application’s UI patterns.
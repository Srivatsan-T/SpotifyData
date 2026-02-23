# `liked_songs.py` – Liked Songs Page

**File path**  
`/app/cloned_repos/spotify_data/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer Dash application.  
It is responsible for:

- Registering the page route (`/liked/<username>`) with Dash.
- Rendering a navigation bar, a pagination slider, and a table of liked songs.
- Updating the table when the user changes the pagination slider.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `dash` | Provides the core Dash framework and `register_page` helper. | `dash.register_page` |
| `dash_bootstrap_components` (`dbc`) | Bootstrap‑styled components for the UI. | `dbc.NavbarSimple`, `dbc.Table` |
| `dash.dependencies` (`Input`, `Output`, `State`) | Decorator arguments for callbacks. | `@callback`, `Input`, `Output`, `State` |
| `dash` (`dcc`, `html`) | Core Dash components. | `dcc.Slider`, `html.Div`, `html.H1`, etc. |
| `pandas` | Data manipulation and conversion to a table. | `pd.DataFrame`, `df.drop`, `df.to_dict` |
| `math` | Calculate number of pages. | `math.ceil` |
| `postgres` | Retrieve liked‑song data from the PostgreSQL database. | `postgres.select_liked_songs` |

> **Note**: The module has no external dependencies beyond those listed above.

---

## Core Functions & Components

### 1. `layout(username=None)`

```python
def layout(username=None):
    ...
```

- **Purpose**: Builds the static layout of the page.
- **Key Steps**:
  1. **Data Query** – Calls `postgres.select_liked_songs(0)` to fetch all liked songs.  
     *Why*: The page needs the total count to compute pagination.
  2. **Pagination Calculation** –  
     ```python
     number_of_liked_songs = len(liked_songs)
     page_size = 50
     number_of_pages = math.ceil(number_of_liked_songs / page_size)
     ```
  3. **Navigation Bar** – Uses `dbc.NavbarSimple` with links to *Liked Songs*, *Recents*, *Analytics*, and *Back*.  
     The `username` parameter is interpolated into each link’s URL.
  4. **Slider** – `dcc.Slider` with `id='Pagination'` controls the current page.  
     Marks are generated for every page number.
  5. **Table Container** – `html.Div` with `id='liked_table'` will hold the table rendered by the callback.

- **Return Value**: A `html.Div` containing the navbar, slider, and table container.

---

### 2. `pages(active_page, max)`

```python
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    ...
```

- **Purpose**: Dynamically updates the liked‑songs table when the pagination slider changes.
- **Key Steps**:
  1. **Determine Slice** –  
     ```python
     if active_page == max:
         liked_songs = postgres.select_liked_songs(active_page*50-50)
     else:
         liked_songs = postgres.select_liked_songs(active_page*50-50, active_page*50)
     ```
     *Why*: The `select_liked_songs` function accepts a start index and an optional end index.  
     The slice size is 50 (the page size).
  2. **DataFrame Construction** –  
     ```python
     column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
     df = pd.DataFrame(liked_songs, columns=column_names)
     df = df.drop(['song_id', 'preview_url'], axis=1)
     ```
     *Why*: `song_id` and `preview_url` are not displayed; the rest are shown in the table.
  3. **Render Table** –  
     ```python
     return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
     ```
     *Why*: `dbc.Table.from_dataframe` creates a Bootstrap‑styled table from the DataFrame.

- **Return Value**: A `dbc.Table` component that replaces the children of the `liked_table` div.

---

## How the Module Fits into the System

| Component | Interaction | Role |
|-----------|-------------|------|
| **Dash App** | Imports `pages.liked_songs` and registers it via `dash.register_page`. | Provides a route `/liked/<username>` that users can navigate to. |
| **`postgres.select_liked_songs`** | Called by `layout` and `pages` to fetch data. | Supplies the liked‑song data stored in the PostgreSQL database. |
| **`dbc.NavbarSimple`** | Rendered in `layout`. | Offers navigation to other pages (Recents, Analytics, Back). |
| **`dcc.Slider`** | Rendered in `layout`; its value triggers `pages`. | Allows users to paginate through the liked‑song list. |
| **`dbc.Table`** | Rendered in `pages`. | Displays the current page of liked songs. |

> **Note**: The module has no `used_by` entries in the evidence, meaning no other modules explicitly import or call its functions. However, the Dash framework automatically loads the page when the route is accessed.

---

## Usage Summary

1. **User navigates** to `/liked/<username>` (e.g., `/liked/johndoe`).
2. **`layout`** is invoked:
   - Queries the database for all liked songs.
   - Calculates pagination.
   - Renders the navbar, slider, and empty table container.
3. **User moves the slider**:
   - The `pages` callback is triggered.
   - It fetches the appropriate slice of liked songs.
   - Builds a DataFrame, drops unnecessary columns, and renders a Bootstrap table.
4. **Table updates** in real time as the slider changes.

---

## Key Code Snippets

```python
# Register the page
dash.register_page(__name__, path_template='/liked/<username>')

# Layout
def layout(username=None):
    liked_songs = postgres.select_liked_songs(0)
    number_of_liked_songs = len(liked_songs)
    page_size = 50
    number_of_pages = math.ceil(number_of_liked_songs / page_size)
    ...
    return html.Div([...])

# Callback
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    if active_page == max:
        liked_songs = postgres.select_liked_songs(active_page*50-50)
    else:
        liked_songs = postgres.select_liked_songs(active_page*50-50, active_page*50)
    df = pd.DataFrame(liked_songs, columns=column_names).drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

---

## Summary

- **Primary Role**: Provides a paginated view of a user’s liked songs.
- **Dependencies**: Relies on `postgres` for data, `dash`/`dash_bootstrap_components` for UI, and `pandas` for data manipulation.
- **Interaction**: The page is registered with Dash, renders a navigation bar, slider, and table, and updates the table via a callback when the slider changes.

This documentation should give developers a clear understanding of how `liked_songs.py` fits into the Spotify Analyzer application, what external modules it depends on, and how its functions are used to render and update the liked‑songs page.
# `liked_songs.py` – Page for Viewing Liked Songs

**File path**  
`/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer web app.  
It is a Dash page that displays a paginated table of the user’s liked songs
stored in a PostgreSQL database.

---

## 1. Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* **Why the dependency exists** – `dash.register_page` is used to register this
  module as a Dash page.  
* **What it does** – Exposes the page at the URL pattern `/liked/<username>`,
  where `<username>` is a dynamic segment that will be passed to the layout
  function.

---

## 2. Imports & External Dependencies

| Import | Purpose |
|--------|---------|
| `dash` | Core Dash framework. |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (Navbar, Table). |
| `dash.dependencies import Input, Output, State` | Callback wiring. |
| `dash.html` | HTML components (`Div`, `H1`, etc.). |
| `dash.dcc` | Dash Core Components (`Slider`). |
| `pandas as pd` | Data manipulation and DataFrame creation. |
| `postgres` | Custom module that provides database access functions. |
| `math` | `ceil` for page count calculation. |

All these imports are explicitly listed in the `external_dependencies` field of
the JSON evidence.

---

## 3. Layout Function

```python
def layout(username=None):
    liked_songs = postgres.select_liked_songs(0)
    number_of_liked_songs = len(liked_songs)
    page_size = 50
    number_of_pages = math.ceil(number_of_liked_songs / page_size)

    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Liked Songs", href=f'http://localhost:8050/liked/{username}', id='LikedSongs')),
            dbc.NavItem(dbc.NavLink("Recents", href=f'http://localhost:8050/recents/{username}', id="Recents")),
            dbc.NavItem(dbc.NavLink("Analytics", href=f'http://localhost:8050/analytics/{username}', id="Analytics")),
            dbc.NavItem(dbc.NavLink("Back", href=f'http://localhost:8050/tools/{username}', id="Back"))
        ],
        brand="Spotify Analyzer",
        brand_href="http://localhost:8050/",
        className='box-form left'
    )

    return html.Div([
        navbar,
        html.Div([dcc.Slider(id='Pagination', min=1, max=number_of_pages, step=1, value=1,
                             marks={i: str(i) for i in range(1, number_of_pages + 1)})],
                 style={'margin': '0 40px'}),
        html.Div(children=[], id='liked_table', style={'margin': '0 40px'})
    ], style={})
```

### What the layout does

* **Data fetch** – Calls `postgres.select_liked_songs(0)` to get the first
  slice of liked songs.  
  *Why*: The total count is needed to compute pagination.
* **Pagination** – Uses `math.ceil` to determine how many pages of 50 songs
  exist.
* **Navbar** – Provides navigation links to other pages (`Recents`, `Analytics`,
  `Back`). Each link includes the current `username` in the URL.
* **Slider** – A `dcc.Slider` component (`id='Pagination'`) that lets the user
  choose a page number. The slider’s `marks` are generated dynamically.
* **Table placeholder** – An empty `Div` (`id='liked_table'`) that will be
  populated by the callback.

### Interaction with other modules

* The layout is **used by** the Dash app when the user navigates to
  `/liked/<username>`.  
* It relies on the `postgres` module for data retrieval.

---

## 4. Callback – Pagination

```python
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']

    if active_page == max:
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50)
    else:
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50,
                                                  active_page * 50)

    df = pd.DataFrame(liked_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

### Why the dependency exists

* **`postgres.select_liked_songs`** – Provides the slice of liked songs for
  the requested page.
* **`pandas`** – Converts the raw tuples into a DataFrame for easy
  manipulation.
* **`dash_bootstrap_components`** – Renders the DataFrame as a Bootstrap
  table.

### What the callback does

1. **Determine slice** – Calculates the offset and limit based on the
   `active_page`.  
   *If the user is on the last page, the end index is omitted to fetch all
   remaining rows.*
2. **Build DataFrame** – Creates a DataFrame with the specified column names,
   then drops the `song_id` and `preview_url` columns (they are not needed for
   display).
3. **Render table** – Uses `dbc.Table.from_dataframe` to produce a styled
   table that replaces the contents of the `liked_table` Div.

### Interaction with other modules

* The callback is **used by** the Dash app to update the UI when the slider
  changes.  
* It depends on the `postgres` module for data access and on `pandas` for
  data formatting.

---

## 5. Summary of Responsibilities

| Responsibility | Where it lives | Key functions / components |
|----------------|----------------|----------------------------|
| **Page registration** | `dash.register_page` | Exposes `/liked/<username>` |
| **Layout rendering** | `layout` | Builds navbar, slider, table placeholder |
| **Pagination logic** | `pages` callback | Fetches data slice, renders table |
| **Data access** | `postgres.select_liked_songs` | Retrieves liked songs from DB |
| **UI components** | `dash_bootstrap_components` | Navbar, Table |
| **Slider control** | `dcc.Slider` | Page selection |
| **Data formatting** | `pandas` | DataFrame creation & manipulation |

---

## 6. Notes on Missing Relationships

* The `used_by` list for `liked_songs` is empty in the evidence, meaning no
  other module explicitly imports or calls its functions.  
* The module is self‑contained: it only provides the layout and callback for
  the *Liked Songs* page.

---

## 7. Quick Reference

```python
# Register the page
dash.register_page(__name__, path_template='/liked/<username>')

# Layout
def layout(username=None):
    # fetch total liked songs
    liked_songs = postgres.select_liked_songs(0)
    # compute pagination
    number_of_pages = math.ceil(len(liked_songs) / 50)
    # build navbar, slider, table placeholder
    ...

# Callback to update table
@callback(
    Output('liked_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    # fetch slice of liked songs
    liked_songs = postgres.select_liked_songs(offset, limit)
    # build DataFrame and render table
    ...
```

This documentation should give developers a clear understanding of how
`liked_songs.py` fits into the overall Spotify Analyzer application,
what external modules it relies on, and how its UI components interact
with the database layer.
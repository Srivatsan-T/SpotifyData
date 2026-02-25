# `pages.liked_songs` – Liked Songs Page

**File path**  
`/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer Dash application.  
It is responsible for:

* Registering the page with a dynamic URL (`/liked/<username>`).  
* Rendering a navigation bar, a pagination slider, and a placeholder for the songs table.  
* Providing a Dash callback that populates the table with the current page of liked songs.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `postgres` | The page pulls data from the PostgreSQL database. | `postgres.select_liked_songs()` |
| `dash` | Core Dash functionality (page registration). | `dash.register_page` |
| `dash.callback` | Decorator for the callback. | `@callback` |
| `dash.dcc` | Dash Core Components – used for the pagination slider. | `dcc.Slider` |
| `dash.dependencies` | Input/Output/State objects for callbacks. | `Input`, `Output`, `State` |
| `dash.html` | HTML components for layout. | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap‑styled components. | `dbc.NavbarSimple`, `dbc.Table` |
| `math` | Pagination calculations. | `math.ceil` |
| `pandas` | DataFrame creation and manipulation. | `pd.DataFrame` |

> **Note:** The module has no downstream consumers (`used_by` is empty).

---

## Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* Registers this module as a Dash page.  
* The URL contains a `<username>` placeholder that is passed to the `layout` function.

---

## `layout(username=None)`

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

### What it does

1. **Data fetch** – Calls `postgres.select_liked_songs(0)` to get the full list of liked songs.  
2. **Pagination** – Calculates the number of pages (`page_size = 50`) and creates a `dcc.Slider` that lets the user choose a page.  
3. **Navigation bar** – Uses `dbc.NavbarSimple` to provide links to other pages (`Recents`, `Analytics`, `Back`).  
4. **Table placeholder** – An empty `html.Div` with `id='liked_table'` that will be populated by the callback.

### Interaction with the rest of the system

* The `layout` function is called by Dash when the user navigates to `/liked/<username>`.  
* The `username` parameter is used only for constructing navigation links; the actual data is independent of the username (the database stores all users’ data).

---

## Callback – `pages(active_page, max)`

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
        liked_songs = postgres.select_liked_songs(active_page * 50 - 50, active_page * 50)

    df = pd.DataFrame(liked_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

### Why the dependency exists

* **`postgres`** – Provides `select_liked_songs(beg, end)` to fetch a slice of the liked songs table.  
* **`pandas`** – Converts the raw tuples into a DataFrame for easy manipulation.  
* **`dash_bootstrap_components`** – Renders the DataFrame as a Bootstrap‑styled table.  
* **`dash.dependencies`** – Supplies `Input`, `Output`, and `State` objects for the callback.

### Functionality

1. **Pagination logic** – Determines the slice of data to fetch based on the current slider value (`active_page`).  
2. **Data retrieval** – Calls `postgres.select_liked_songs` with appropriate `beg` and `end` indices.  
3. **DataFrame creation** – Builds a DataFrame with the specified columns.  
4. **Column pruning** – Drops `song_id` and `preview_url` before rendering.  
5. **Table rendering** – Uses `dbc.Table.from_dataframe` to create a styled table that replaces the contents of `liked_table`.

### Interaction with the rest of the system

* The callback is triggered whenever the user moves the pagination slider.  
* It updates the `liked_table` component in the layout, providing a dynamic, paginated view of liked songs.

---

## Summary

* **Purpose** – Display a paginated table of a user’s liked songs.  
* **Key components** – Navigation bar, pagination slider, and a table placeholder.  
* **Data source** – PostgreSQL via `postgres.select_liked_songs`.  
* **Rendering** – Uses `pandas` for data manipulation and `dash_bootstrap_components` for UI.  
* **Integration** – Registered as a Dash page (`/liked/<username>`) and interacts with the rest of the app through navigation links and the pagination slider.

This module is self‑contained: it has no downstream consumers, but it is a core part of the user interface for exploring liked songs.
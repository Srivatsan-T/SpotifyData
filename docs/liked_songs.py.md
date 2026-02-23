# `pages.liked_songs` – Liked Songs Page

**File path:** `/app/cloned_repos/spotifydata/pages/liked_songs.py`

This module implements the *Liked Songs* page of the Spotify Analyzer web‑app.  
It is a Dash page that displays a paginated table of the user’s liked songs
stored in a PostgreSQL database.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Page registration** | `dash.register_page(__name__, path_template='/liked/<username>')` registers the page with a dynamic `<username>` segment. |
| **Layout** | `layout(username=None)` builds the page layout: a navigation bar, a pagination slider, and a container for the song table. |
| **Callback** | `pages(active_page, max)` updates the table whenever the pagination slider changes. |
| **Dependencies** | Relies on the local `postgres` module to fetch data, and on Dash, Dash‑Bootstrap‑Components, Pandas, and the standard `math` library. |

---

## Imports & External Dependencies

```python
from dash import dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import html
import dash
import pandas as pd
import postgres
import math
```

* **Dash** – Core framework for building the web UI.
* **Dash‑Bootstrap‑Components** – Provides Bootstrap‑styled components (e.g., `NavbarSimple`, `Table`).
* **Dash dependencies** – `Input`, `Output`, `State` are used to wire the callback.
* **Pandas** – Converts query results into a DataFrame for easy table rendering.
* **Postgres** – Custom module that exposes `select_liked_songs` for database access.
* **Math** – `ceil` is used to calculate the number of pagination pages.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/liked/<username>')
```

* Registers this module as a Dash page.
* The URL pattern `/liked/<username>` allows the page to be accessed for any Spotify username.

---

## Layout Function

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

### Why the dependencies exist

| Dependency | Reason |
|------------|--------|
| `postgres` | Provides `select_liked_songs` to fetch liked songs from the database. |
| `math` | `ceil` calculates the number of pages needed for pagination. |
| `dash_bootstrap_components` | Builds a Bootstrap‑styled navigation bar. |
| `dash` / `dash.dependencies` | Creates the slider and defines the callback wiring. |
| `pandas` | Not used directly in `layout`, but imported for consistency with the rest of the module. |

### How the layout works

1. **Data fetch** – Calls `postgres.select_liked_songs(0)` to get all liked songs.  
   *The function returns a list of tuples; the length determines pagination.*

2. **Pagination** – With a fixed `page_size` of 50, the number of pages is computed.

3. **Navigation bar** – Provides links to other pages (`Recents`, `Analytics`, `Back`) with URLs that include the current `username`.

4. **Slider** – A `dcc.Slider` with id `Pagination` lets the user choose a page number.  
   *`marks` are generated for each page.*

5. **Table container** – An empty `html.Div` with id `liked_table` will be populated by the callback.

---

## Callback – `pages`

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

### Why the dependencies exist

| Dependency | Reason |
|------------|--------|
| `postgres` | `select_liked_songs(beg, end)` retrieves the appropriate slice of liked songs for the requested page. |
| `pandas` | Converts the list of tuples into a DataFrame for easy manipulation and rendering. |
| `dash_bootstrap_components` | `dbc.Table.from_dataframe` creates a Bootstrap‑styled table from the DataFrame. |
| `dash.dependencies` | `Input` and `State` wire the slider value to the callback. |

### How the callback works

1. **Input** – The slider’s current value (`active_page`) triggers the callback.  
   The `max` state provides the total number of pages.

2. **Query** –  
   * If the user is on the last page (`active_page == max`), the query fetches all remaining songs starting from `(active_page * 50 - 50)` to the end.  
   * Otherwise, it fetches a fixed slice of 50 songs: from `(active_page * 50 - 50)` to `active_page * 50`.

3. **DataFrame** – The raw tuples are turned into a DataFrame with the specified column names.

4. **Column pruning** – `song_id` and `preview_url` are dropped because they are not needed for display.

5. **Table rendering** – `dbc.Table.from_dataframe` creates a styled table that is returned as the children of the `liked_table` div.

---

## Interaction with the Rest of the System

* **User Flow** – After logging in via `pages.cred`, the user is redirected to `/tools/<username>`.  
  From there, clicking “Liked Songs” navigates to `/liked/<username>`, which loads this page.

* **Data Source** – The liked songs are stored in the PostgreSQL table `liked_songs`.  
  The `postgres.select_liked_songs` function (defined in `postgres.py`) reads from this table.

* **Pagination** – The slider allows the user to navigate through the liked songs in chunks of 50.  
  The callback ensures that only the relevant slice is fetched and displayed.

---

## Summary

`pages.liked_songs` is a self‑contained Dash page that:

1. **Registers** itself with a dynamic URL.
2. **Builds** a navigation bar and pagination slider.
3. **Fetches** liked songs from a PostgreSQL database via the `postgres` module.
4. **Displays** the songs in a Bootstrap‑styled table, updating on slider changes.

All interactions are driven by Dash callbacks, and the module relies on the `postgres` helper for database access, `pandas` for data manipulation, and `dash_bootstrap_components` for UI styling.
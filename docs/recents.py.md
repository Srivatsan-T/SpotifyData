# `recents.py` – Recents Page

**File path**  
`/app/cloned_repos/spotifydata/pages/recents.py`

---

## Overview

`recents.py` implements the **Recents** page of the Spotify Analyzer web application.  
It is a Dash page that displays a paginated table of the most recently played songs for a
given user. The page is registered with the URL pattern `/recents/<username>`.

The module relies on:

| Dependency | Purpose |
|------------|---------|
| `postgres` | Fetches recent‑song data from the PostgreSQL database. |
| `dash` & `dash_bootstrap_components` | Build the page layout and UI components. |
| `pandas` | Convert raw database rows into a DataFrame for easy rendering. |
| `math` | Compute the number of pagination pages. |

---

## Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

* Registers this module as a Dash page.  
* The `<username>` placeholder is passed to the `layout` function.

---

## `layout(username=None)`

### Purpose
Creates the static part of the page: a navigation bar, a pagination slider, and an empty
container that will be filled with the recent‑songs table.

### Key Steps

1. **Data Retrieval**  
   ```python
   recents = postgres.select_recent_songs(0)
   ```
   * Calls `postgres.select_recent_songs` to fetch all recent songs (starting at offset 0).  
   * The `postgres` module is responsible for executing the SQL query that returns the
     recent‑songs view.

2. **Pagination Calculation**  
   ```python
   number_of_recent_songs = len(recents)
   page_size = 50
   number_of_pages = math.ceil(number_of_recent_songs / page_size)
   ```
   * Uses `math.ceil` to determine how many pages are needed when showing 50 songs per page.

3. **Navigation Bar**  
   ```python
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
   ```
   * Provides quick navigation to other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).

4. **Return Structure**  
   ```python
   return html.Div([
       navbar,
       html.Div([dcc.Slider(id='Pagination', min=1, max=number_of_pages,
                            step=1, value=1,
                            marks={i: str(i) for i in range(1, number_of_pages+1)})],
                style={'margin':'0 40px'}),
       html.Div(children=[], id='recents_table', style={'margin':'0 40px'})
   ], style={})
   ```
   * The slider (`Pagination`) controls the current page.  
   * The `recents_table` div will be populated by the callback below.

---

## Callback `pages(active_page, max)`

```python
@callback(
    Output('recents_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    ...
```

### Purpose
Dynamically updates the table of recent songs whenever the user changes the pagination slider.

### Logic

1. **Column Definition**  
   ```python
   column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
   ```

2. **Data Retrieval with Pagination**  
   ```python
   if active_page == max:
       recent_songs = postgres.select_recent_songs(active_page*50-50)
   else:
       recent_songs = postgres.select_recent_songs(active_page*50-50, active_page*50)
   ```
   * Calls `postgres.select_recent_songs` with `beg` and optional `end` parameters to fetch
     only the rows for the current page.

3. **DataFrame Construction**  
   ```python
   df = pd.DataFrame(recent_songs, columns=column_names)
   df = df.drop(['song_id', 'preview_url'], axis=1)
   ```

4. **Render Table**  
   ```python
   return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
   ```
   * Uses `dash_bootstrap_components` to create a styled table from the DataFrame.

---

## Dependencies Explained

| Module | Why it is imported | What functionality is used |
|--------|--------------------|----------------------------|
| `postgres` | Provides database access functions (`select_recent_songs`). | `select_recent_songs` is called to fetch recent‑song records. |
| `dash` | Core Dash framework. | `dash.register_page` registers the page. |
| `dash_bootstrap_components` | Bootstrap‑styled components. | `NavbarSimple`, `NavItem`, `NavLink`, `Table`. |
| `dash.dependencies` (`Input`, `Output`, `State`) | Defines callback inputs/outputs. | `@callback` decorator and its arguments. |
| `dash` (`dcc`, `html`) | UI components. | `dcc.Slider`, `html.Div`, `html.H1`, etc. |
| `pandas` | Data manipulation. | `pd.DataFrame` and `drop`. |
| `math` | Mathematical utilities. | `math.ceil` for pagination calculation. |

---

## Interaction Flow

1. **User navigates** to `/recents/<username>`.  
2. Dash calls `layout(username)` to render the page skeleton.  
3. The slider (`Pagination`) is displayed with marks for each page.  
4. When the slider value changes, the `pages` callback is triggered.  
5. The callback fetches the appropriate slice of recent songs from the database, builds a
   DataFrame, removes unnecessary columns, and renders a Bootstrap table inside
   `recents_table`.  
6. The user can navigate between pages using the slider; the table updates accordingly.

---

## Notes

* The module does **not** directly handle authentication or data fetching from Spotify;
  that logic resides in `pages.cred` and the `spotify` module.
* The `recents` page relies on the database schema defined in the SQL files referenced by
  `postgres.select_recent_songs`.  
* No other modules list `recents` as a dependency in the provided evidence, but the
  `postgres` module lists `recents` as a consumer.

---

### Summary

`recents.py` is a self‑contained Dash page that:

1. **Registers** itself under `/recents/<username>`.  
2. **Builds** a navigation bar, pagination slider, and placeholder for a table.  
3. **Fetches** recent‑song data from PostgreSQL via the `postgres` module.  
4. **Displays** the data in a paginated, Bootstrap‑styled table using `pandas` and
   `dash_bootstrap_components`.  

This module is the primary entry point for viewing a user’s recently played songs within
the Spotify Analyzer application.
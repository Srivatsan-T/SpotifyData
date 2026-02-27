# `recents.py` – Recents Page

**File path**: `/app/cloned_repos/spotifydata/pages/recents.py`

This module implements the *Recents* page of the Spotify Analyzer Dash application.  
It displays a paginated table of the most recently played songs for a given user.

---

## Overview

| Feature | Description |
|---------|-------------|
| **Page registration** | `dash.register_page(__name__, path_template='/recents/<username>')` registers this module as a Dash page that can be accessed via `/recents/<username>`. |
| **Layout** | `layout(username=None)` builds the page layout: a navigation bar, a pagination slider, and an empty container that will hold the table. |
| **Callback** | `pages(active_page, max)` is a Dash callback that updates the table whenever the pagination slider changes. |

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `postgres` | Provides the data source for recent songs. | `postgres.select_recent_songs(beg, end)` |
| `dash` | Core Dash framework. | `dash.register_page`, `dash.callback` |
| `dash.dcc` | Dash Core Components (slider). | `dcc.Slider` |
| `dash.html` | Dash HTML Components (divs, links). | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap styling for navbar and table. | `dbc.NavbarSimple`, `dbc.Table.from_dataframe` |
| `dash.dependencies` | Input/Output/State objects for callbacks. | `Input`, `Output`, `State` |
| `pandas` | Data manipulation and table rendering. | `pd.DataFrame` |
| `math` | Pagination calculation. | `math.ceil` |

> **Note**: The `used_by` list for this module is empty, but it is implicitly used by the Dash app as a registered page.

---

## How the Module Works

### 1. Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

- Registers the module as a page that accepts a `username` parameter in the URL.
- The `path_template` allows the app to route `/recents/<username>` to this module.

### 2. Layout Function

```python
def layout(username=None):
    recents = postgres.select_recent_songs(0)
    number_of_recent_songs = len(recents)
    page_size = 50
    number_of_pages = math.ceil(number_of_recent_songs / page_size)
    ...
    return html.Div([...], style={})
```

- **Data Fetch**: Calls `postgres.select_recent_songs(0)` to get all recent songs.  
  The result is a list of tuples returned from the database.
- **Pagination**: Calculates the number of pages (`number_of_pages`) based on a fixed page size of 50.
- **Navbar**: Uses `dbc.NavbarSimple` to provide navigation links to *Liked Songs*, *Recents*, *Analytics*, and *Back*.
- **Slider**: `dcc.Slider` with `id='Pagination'` lets the user pick a page.  
  `marks` are generated for each page number.
- **Table Container**: An empty `html.Div` with `id='recents_table'` will be populated by the callback.

### 3. Callback – Pagination

```python
@callback(
    Output('recents_table', 'children'),
    [Input('Pagination', 'value')],
    [State('Pagination', 'max')]
)
def pages(active_page, max):
    column_names = ['song_id', 'SONG', 'ALBUM', 'ARTISTS', 'POPULARITY', 'preview_url']
    if active_page == max:
        recent_songs = postgres.select_recent_songs(active_page * 50 - 50)
    else:
        recent_songs = postgres.select_recent_songs(active_page * 50 - 50, active_page * 50)

    df = pd.DataFrame(recent_songs, columns=column_names)
    df = df.drop(['song_id', 'preview_url'], axis=1)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
```

- **Inputs**:  
  - `active_page` – current slider value.  
  - `max` – maximum slider value (total pages).
- **Data Retrieval**:  
  - If the user is on the last page, fetch from `active_page*50-50` to the end.  
  - Otherwise, fetch a slice of 50 rows.
- **DataFrame**:  
  - Builds a `pandas.DataFrame` with the specified column names.  
  - Drops the `song_id` and `preview_url` columns because they are not needed for display.
- **Table Rendering**:  
  - Uses `dbc.Table.from_dataframe` to create a Bootstrap‑styled table.  
  - The table is returned as the children of the `recents_table` div.

---

## Usage in the Application

1. **Navigation**  
   Users navigate to `/recents/<username>` (e.g., `/recents/john_doe`).  
   The `layout` function renders the page with the navigation bar and pagination slider.

2. **Pagination Interaction**  
   When the slider value changes, the `pages` callback is triggered.  
   It queries the database for the appropriate slice of recent songs and updates the table.

3. **Data Source**  
   All data comes from the PostgreSQL database via the `postgres` module.  
   The `select_recent_songs` function returns rows in the order they were added to the `recents` table.

---

## Key Points for Developers

- **Extensibility**:  
  - To change the page size, modify `page_size = 50`.  
  - To add more columns to the table, update `column_names` and adjust the DataFrame accordingly.
- **Performance**:  
  - The callback fetches only the slice needed for the current page, keeping memory usage low.
- **Styling**:  
  - All UI elements use Bootstrap components (`dbc.NavbarSimple`, `dbc.Table`).  
  - Custom styles can be added via the `style` dictionaries or by extending the CSS classes.

---

## Summary

`recents.py` is a self‑contained Dash page that:

- Registers itself under `/recents/<username>`.
- Retrieves recent song data from PostgreSQL.
- Provides a paginated view using a slider.
- Renders the data in a Bootstrap‑styled table.

Its dependencies are strictly limited to the `postgres` module for data access and the Dash ecosystem for UI rendering.
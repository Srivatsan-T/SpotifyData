# `analytics.py`

**File path**: `/app/cloned_repos/spotify_data/pages/analytics.py`

The `analytics` module implements the *Analytics* page of the Spotify Analyzer Dash application.  
It registers a page route, builds the page layout, and defines a callback that renders
interactive charts and tables based on data stored in a PostgreSQL database.

---

## 1. Module Overview

| Feature | Description |
|---------|-------------|
| **Page registration** | `dash.register_page(__name__, path_template='/analytics/<username>')` registers the module as a Dash page that accepts a `<username>` URL parameter. |
| **Layout** | `layout(username=None)` returns a `html.Div` containing a navigation bar, a year‑selection dropdown, and a placeholder `div` (`id='target_div'`) where analytics results are injected. |
| **Callback** | `analytics_display(value)` is triggered when the user selects a year from the dropdown. It queries the database for album and popularity data, builds bar charts and a table, and returns them as children of `target_div`. |
| **Dependencies** | The module relies on the `postgres` helper module for database access and on Dash/Dash‑Bootstrap‑Components for UI components. |

---

## 2. Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `postgres` (module) | Provides database access functions (`get_years`, `get_albums_for_year`, `get_popular_for_year`). | `postgres.get_years()`, `postgres.get_albums_for_year(year)`, `postgres.get_popular_for_year(year, flag)` |
| `dash` | Core Dash framework for page registration and callbacks. | `dash.register_page`, `dash.callback` |
| `dash.dcc` | Dash Core Components for dropdowns and graphs. | `dcc.Dropdown`, `dcc.Graph` |
| `dash.html` | Dash HTML Components for layout elements. | `html.Div`, `html.H1`, `html.H2` |
| `dash_bootstrap_components` | Bootstrap‑styled components (navbar, table). | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink`, `dbc.Table` |
| `dash.dependencies` | Input/Output objects for callbacks. | `Input`, `Output` |
| `pandas` | DataFrame creation for table rendering. | `pd.DataFrame` |

> **Note**: All imports are explicit in the source code; no implicit or dynamic imports are used.

---

## 3. Page Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

*Registers the module as a Dash page.*  
The `<username>` placeholder allows the URL to be `/analytics/<username>` where `<username>` is the Spotify user’s name.  
This registration is required for Dash’s multi‑page routing system.

---

## 4. Layout Function

```python
def layout(username=None):
    years  = list(postgres.get_years())
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Liked Songs", href=f'http://localhost:8050/liked/{username}', id='LikedSongs')),
            dbc.NavItem(dbc.NavLink("Recents", href=f'http://localhost:8050/recents/{username}', id="Recents")),
            dbc.NavItem(dbc.NavLink("Analytics", href=f'http://localhost:8050/analytics/{username}', id="Analytics")),
            dbc.NavItem(dbc.NavLink("Back", href=f'http://localhost:8050/tools/{username}', id="Back")),
        ],
        brand="Spotify Analyzer",
        brand_href="http://localhost:8050/",
        className='box-form left'
    )

    return html.Div([
        navbar,
        html.Div([dcc.Dropdown([year[0] for year in years], placeholder='Select year', id='year_drop')],
                 style={'margin':'0 500px',"padding-top":'20px'}),
        html.Div(children=[], id='target_div', style={'margin':'30px 200px'})
    ])
```

### What it does

1. **Fetch available years**  
   Calls `postgres.get_years()` to populate the dropdown with years extracted from the database.

2. **Build navigation bar**  
   Uses `dbc.NavbarSimple` with links to other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).  
   Each link includes the current `username` in its URL.

3. **Return the page structure**  
   The outer `html.Div` contains:
   * The navbar
   * A centered `dcc.Dropdown` (`id='year_drop'`) for year selection
   * An empty `html.Div` (`id='target_div'`) that will hold the analytics output

### Styling

* The dropdown container is centered with `margin: 0 500px` and padded top 20 px.
* The result container (`target_div`) has a margin of `30px 200px`.

---

## 5. Analytics Callback

```python
@callback(
    Output('target_div', 'children'),
    [Input('year_drop', 'value')]
)
def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)
        ...
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results",
                        style={'border-style':'solid','font-size':'7vmax',
                               'color':'white','text-align':'center'})]
```

### Trigger

* The callback fires whenever the `value` of the `year_drop` dropdown changes.

### Logic Flow

| Step | Action | Data |
|------|--------|------|
| 1 | **Check selection** | If `value` is `None`, return a placeholder message. |
| 2 | **Retrieve albums** | `postgres.get_albums_for_year(value)` → list of `(album_name, song_count)` tuples. |
| 3 | **Compute most popular songs** | `postgres.get_popular_for_year(value, 'desc')` returns a list of tuples where `j[4]` is the month index. For each month (1‑12) the callback builds:
   * `most_pop_list` – y‑values (`j[2]*10 + 100`)
   * `most_names_list` – song names (`j[0]`) |
| 4 | **Compute least popular songs** | Same as step 3 but with `flag='asc'`. |
| 5 | **Create bar charts** | Two `dcc.Graph` objects (`most_popular`, `least_popular`) with bar traces and month x‑axis. |
| 6 | **Create album table** | `pd.DataFrame(albums, columns=['ALBUM', 'SONGS COUNT'])` → `dbc.Table.from_dataframe`. |
| 7 | **Assemble result** | A list of components:
   * `html.H2` heading
   * Album table
   * Most popular graph
   * Least popular graph |
| 8 | **Return** | The list is set as `children` of `target_div`. |

### Data Transformation Details

* **Popularity calculation**  
  `most_pop_list[i-1] = j[2]*10 + 100` scales the raw popularity score (`j[2]`) to a visual range suitable for the bar chart.

* **Month mapping**  
  The loop iterates `i` from 1 to 12, matching `j[4]` (month index) to place each song in the correct bar.

* **Fallback values**  
  If no data is found for a month, the list entries remain `0` and the name `'NONE'`.

### Styling

* Graph titles: `'Most Popular Songs Graph'` and `'Least Popular Songs Graph'`.
* Heading: white text, solid border, centered.
* Table: striped, bordered, hoverable, centered, with top padding.

---

## 6. Interaction with the Rest of the Application

| Interaction | How it occurs |
|-------------|---------------|
| **Navigation** | The navbar links in `layout()` point to other pages (`liked_songs`, `recents`, `tools`). |
| **Data source** | All analytics data comes from the PostgreSQL database via the `postgres` module. |
| **User flow** | After logging in (handled by `pages.cred`), the user is redirected to `/tools/<username>`. From there they can navigate to `/analytics/<username>` to view analytics. |
| **Callback wiring** | The `analytics_display` callback is automatically wired by Dash because it is decorated with `@callback` and references the `year_drop` input and `target_div` output. |

> **No other modules directly import or call functions from `analytics.py`.**  
> The module is self‑contained: it registers its own page and defines the layout and callback needed for that page.

---

## 7. Summary

`analytics.py` is the core of the *Analytics* page in the Spotify Analyzer Dash app.  
It:

1. **Registers** the page route `/analytics/<username>`.
2. **Builds** a UI with a navbar, year selector, and placeholder for results.
3. **Queries** the PostgreSQL database for yearly album and popularity data.
4. **Renders** interactive bar charts and a table of top albums.
5. **Provides** user feedback when no year is selected.

All functionality is explicitly imported and used, with no hidden or implicit dependencies. The module’s design follows Dash’s best practices for multi‑page applications and leverages Bootstrap styling for a polished UI.
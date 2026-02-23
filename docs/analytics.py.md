# `pages.analytics` – Analytics Page

**File path**  
`/app/cloned_repos/spotifydata/pages/analytics.py`

The `analytics` module implements the *Analytics* page of the Spotify Analyzer web‑app.  
It is a Dash page that displays:

* A navigation bar with links to the other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).
* A dropdown to select a year.
* A dynamic container (`target_div`) that shows:
  * A table of the top 3 albums for the selected year.
  * Two bar charts – most popular and least popular songs for each month of that year.

---

## Imports & Dependencies

| Import | Purpose | Source |
|--------|---------|--------|
| `dash`, `dash.html`, `dash.dcc`, `dash.callback`, `dash.dependencies.Input`, `dash.dependencies.Output` | Core Dash components and callback decorators. | `dash` package |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (Navbar, Table). | `dash_bootstrap_components` package |
| `pandas as pd` | Data manipulation and DataFrame creation. | `pandas` package |
| `postgres` | Database helper functions (`get_years`, `get_albums_for_year`, `get_popular_for_year`). | Local module `postgres.py` |

> **Why these dependencies exist**  
> *Dash* provides the web UI framework.  
> *Bootstrap* gives a ready‑made navigation bar and table styling.  
> *Pandas* is used to convert raw tuples from PostgreSQL into a DataFrame for easy rendering.  
> The `postgres` module contains all SQL helpers that fetch the data needed for the analytics.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* Registers this module as a Dash page.  
* The URL pattern includes a `<username>` placeholder that is passed to `layout` and the callback.

---

## `layout(username=None)`

```python
def layout(username = None):
    years  = list(postgres.get_years())
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
        html.Div([dcc.Dropdown([year[0] for year in years], placeholder='Select year', id='year_drop')],
                 style={'margin':'0 500px',"padding-top":'20px'}),
        html.Div(children=[], id='target_div', style={'margin':'30px 200px'})
    ])
```

### What it does

1. **Fetch available years** – `postgres.get_years()` returns a list of tuples like `[(2020,), (2021,), …]`.  
2. **Build navigation bar** – `dbc.NavbarSimple` contains links that keep the current `username` in the URL.  
3. **Year selector** – a `dcc.Dropdown` with the list of years.  
4. **Result container** – an empty `Div` (`id='target_div'`) that will be populated by the callback.

### Interaction with the rest of the system

* The `layout` function is called by Dash when the user navigates to `/analytics/<username>`.  
* The `username` is used only for constructing navigation links; the analytics data is independent of the user (the database is shared).

---

## `analytics_display(value)`

```python
@callback(
    Output('target_div','children'),
    [Input('year_drop','value')]
)
def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)
        ...
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results", ...)]
```

### Callback flow

| Step | Action | Data Source | Notes |
|------|--------|-------------|-------|
| 1 | User selects a year in the dropdown (`year_drop`). | UI | Triggers callback. |
| 2 | `postgres.get_albums_for_year(value)` | PostgreSQL | Returns tuples `(album_name, song_count)` for the selected year. |
| 3 | `postgres.get_popular_for_year(value, 'desc')` | PostgreSQL | Returns tuples `(song_name, popularity, month)` sorted descending. |
| 4 | Build `most_pop_list` & `most_names_list` | Loop over months 1‑12 | For each month, find the song with the highest popularity. |
| 5 | Build `most_popular` graph | `dcc.Graph` | Bar chart with months on x‑axis and popularity on y‑axis. |
| 6 | `postgres.get_popular_for_year(value, 'asc')` | PostgreSQL | Same as step 3 but ascending. |
| 7 | Build `least_pop_list` & `least_names_list` | Loop over months 1‑12 | For each month, find the song with the lowest popularity. |
| 8 | Build `least_popular` graph | `dcc.Graph` | Bar chart similar to step 5. |
| 9 | Convert `albums` to a `pandas.DataFrame` | `pd.DataFrame` | Columns: `ALBUM`, `SONGS COUNT`. |
|10 | Assemble final children list | `html.H2`, `dbc.Table`, `most_popular`, `least_popular` | Returned to `target_div`. |
|11 | If no year selected | Return a prompt message | `html.H1` with instructions. |

### Data processing details

* **Popularity calculation** – The code multiplies the raw popularity (`j[2]`) by 10 and adds 100.  
  This scaling is arbitrary but keeps the bar heights in a readable range.  
* **Month mapping** – `j[4]` holds the month number (1‑12).  
  The lists `most_pop_list` and `least_pop_list` are indexed by month‑1.  
* **Graph construction** – Each graph uses a single bar trace with `x=[1..12]`.  
  The `text` property holds the song name for tooltip display.

### Interaction with other modules

* **`postgres`** – All database queries are performed through this module.  
  The callback relies on `get_years`, `get_albums_for_year`, and `get_popular_for_year`.  
* **`pages.cred`** – After a user logs in, `cred.fetch_data` populates the database tables that `analytics_display` reads.  
* **`pages.liked_songs` & `pages.recents`** – These pages use the same navigation bar and share the same database schema.

---

## Usage Summary

1. **User logs in** → `pages.cred` fetches data and stores it in PostgreSQL.  
2. **User navigates** to `/analytics/<username>` → Dash calls `layout` to render the page.  
3. **User selects a year** → `analytics_display` callback runs, queries the database, and renders the table + graphs.  
4. **Navigation links** keep the user on the same `username` context across pages.

---

## Key Code Snippets

```python
# Register the page
dash.register_page(__name__, path_template='/analytics/<username>')

# Build the year dropdown
dcc.Dropdown([year[0] for year in years], placeholder='Select year', id='year_drop')

# Callback signature
@callback(
    Output('target_div','children'),
    [Input('year_drop','value')]
)
def analytics_display(value):
    ...
```

---

## Dependencies Recap

- **Dash** – UI framework and callback system.  
- **dash_bootstrap_components** – Styled navigation bar and tables.  
- **pandas** – DataFrame conversion for table rendering.  
- **postgres** – SQL helper functions that provide the data for analytics.

All dependencies are explicitly listed in the `external_dependencies` field of the JSON evidence. No other modules are required for `analytics.py` to function.
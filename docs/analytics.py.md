# `pages.analytics` – Analytics Page

**File path**  
`/app/cloned_repos/spotifydata/pages/analytics.py`

The *Analytics* page is a Dash page that displays a year‑based analytics view for a Spotify user.  
It is registered with Dash’s page system and contains two main components:

| Component | Purpose |
|-----------|---------|
| `layout` | Builds the page layout (navbar, year selector, placeholder for results). |
| `analytics_display` | Callback that populates the placeholder with charts and tables when a year is chosen. |

Below is a developer‑friendly breakdown of the module, its dependencies, and how it is used in the application.

---

## 1. Module Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* **Why** – Registers the module as a Dash page that can be accessed via `/analytics/<username>`.  
* **What** – The `dash` package provides the `register_page` function that hooks the module into Dash’s routing system.

---

## 2. Imports & External Dependencies

| Import | Source | Reason |
|--------|--------|--------|
| `from dash import dcc, callback` | `dash` | `dcc` provides Dash core components (e.g., `Dropdown`, `Graph`). `callback` is a decorator for defining callbacks. |
| `import dash_bootstrap_components as dbc` | `dash_bootstrap_components` | Provides Bootstrap‑styled components (`NavbarSimple`, `Table`). |
| `from dash.dependencies import Input, Output` | `dash.dependencies` | Used to declare callback inputs/outputs. |
| `from dash import html` | `dash` | Provides HTML components (`Div`, `H1`, etc.). |
| `import pandas as pd` | `pandas` | Used to create DataFrames for tables. |
| `import postgres` | `postgres` | Custom module that exposes database helper functions (`get_years`, `get_albums_for_year`, `get_popular_for_year`). |

> **Note** – All external dependencies are listed in the `external_dependencies` field of the evidence.

---

## 3. `layout(username=None)`

```python
def layout(username=None):
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

1. **Fetches available years** – Calls `postgres.get_years()` to populate the year dropdown.  
2. **Builds a navigation bar** – Links to other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).  
3. **Creates the main layout** –  
   * A `Dropdown` (`id='year_drop'`) for selecting a year.  
   * An empty `Div` (`id='target_div'`) that will be filled by the callback.

### Why the dependency on `postgres` exists

`postgres.get_years()` queries the database for distinct years present in the user’s data.  
Without this call the dropdown would have no options, so the analytics page would be unusable.

### Interaction with downstream modules

* The page itself is not directly used by other modules in the evidence (`used_by` is empty).  
* However, the callback inside this module will be triggered by user interaction on the page, and the resulting UI elements will be rendered by Dash.

---

## 4. `analytics_display(value)`

```python
@callback(
    Output('target_div', 'children'),
    [Input('year_drop', 'value')]
)
def analytics_display(value):
    if value is not None:
        albums = postgres.get_albums_for_year(value)

        # Build most popular songs bar
        most_pop_list = [0]*12
        most_names_list = ['NONE']*12
        most_populars = postgres.get_popular_for_year(value, 'desc')
        for i in range(1,13):
            for j in most_populars:
                if j[4] == i:
                    most_pop_list[i-1] = j[2]*10 + 100
                    most_names_list[i-1] = j[0]
        most_popular = dcc.Graph(
            figure={'data': [{'x': list(range(1,13)), 'type':'bar', 'y':most_pop_list, 'text':most_names_list}],
                     'layout':{'title':'Most Popular Songs Graph'}}
        )

        # Build least popular songs bar
        least_pop_list = [0]*12
        least_names_list = ['NONE']*12
        least_populars = postgres.get_popular_for_year(value, 'asc')
        for i in range(1,13):
            for j in least_populars:
                if j[4] == i:
                    least_pop_list[i-1] = j[2]*10 + 100
                    least_names_list[i-1] = j[0]
        least_popular = dcc.Graph(
            figure={'data': [{'x': list(range(1,13)), 'type':'bar', 'y':least_pop_list, 'text':least_names_list}],
                     'layout':{'title':'Least Popular Songs Graph'}}
        )

        df = pd.DataFrame(albums, columns=['ALBUM', 'SONGS COUNT'])

        result = [
            html.H2("Your top 3 albums from that year are",
                    style={'color':'white','border-style':'solid','text-align':'center'}),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,
                                     index=False, style={'padding-top':'45px','text-align':'center'}),
            most_popular,
            least_popular
        ]
        return result
    else:
        return [html.H1("Choose a year from the dropdown to see results",
                        style={'border-style':'solid','font-size':'7vmax','color':'white','text-align':'center'})]
```

### What it does

* **Triggered** when the user selects a year from the dropdown (`year_drop`).  
* **Queries the database**:  
  * `postgres.get_albums_for_year(value)` – top albums for the selected year.  
  * `postgres.get_popular_for_year(value, 'desc')` – most popular songs.  
  * `postgres.get_popular_for_year(value, 'asc')` – least popular songs.  
* **Builds UI components**:  
  * Two bar charts (`dcc.Graph`) for most/least popular songs.  
  * A table of the top 3 albums (`dbc.Table`).  
  * A header (`html.H2`).  
* **Returns** a list of Dash components that replace the children of `target_div`.

### Why the dependency on `postgres` exists

The callback relies on three helper functions from the `postgres` module to fetch:

1. **Years** – for the dropdown (in `layout`).  
2. **Albums** – for the album table.  
3. **Popular songs** – for the bar charts.

Without these functions the analytics page would have no data to display.

### What functionality is imported or relied upon

| Function | Purpose |
|----------|---------|
| `postgres.get_years()` | Provides the list of years for the dropdown. |
| `postgres.get_albums_for_year(year)` | Returns a list of tuples `(album_name, song_count)` for the selected year. |
| `postgres.get_popular_for_year(year, flag)` | Returns a list of tuples `(song_name, popularity, month)` sorted by popularity (`'desc'` or `'asc'`). |

### Interaction with downstream modules

* The callback is **self‑contained** – it only interacts with the database via `postgres`.  
* The resulting UI components are rendered by Dash; no other module consumes the callback’s output.  
* The module is registered as a page, so the application’s main Dash app will automatically include it.

---

## 5. Summary of Dependencies

| Dependency | Reason | Functionality Used |
|------------|--------|--------------------|
| `dash` | Core Dash framework | `register_page`, `html` components |
| `dash_bootstrap_components` | Bootstrap styling | `NavbarSimple`, `Table` |
| `dash.dependencies` | Callback wiring | `Input`, `Output` |
| `pandas` | Data manipulation | `DataFrame` for tables |
| `postgres` | Database access | `get_years`, `get_albums_for_year`, `get_popular_for_year` |

> **Missing relationships** – The evidence shows no modules that *use* `pages.analytics`. The `used_by` list is empty, so this page is only registered and rendered by Dash itself.

---

## 6. Suggested Improvements

1. **Add a docstring** to the module and each function to explain purpose and parameters.  
2. **Type hints** for `value` in `analytics_display` (e.g., `int | None`).  
3. **Error handling** – guard against empty query results or database errors.  
4. **Refactor** the repeated logic for building the bar charts into a helper function.  
5. **Use relative URLs** instead of hard‑coded `http://localhost:8050/...` for navigation links.

---

## 7. Quick Reference

```python
# Register page
dash.register_page(__name__, path_template='/analytics/<username>')

# Layout
def layout(username=None):
    # Build navbar + dropdown + placeholder
    ...

# Callback
@callback(Output('target_div', 'children'), [Input('year_drop', 'value')])
def analytics_display(value):
    # Query DB, build charts & table, return components
    ...
```

**File**: `/app/cloned_repos/spotifydata/pages/analytics.py`  
**Primary role**: Provide a user‑friendly analytics view for a Spotify user’s yearly data.
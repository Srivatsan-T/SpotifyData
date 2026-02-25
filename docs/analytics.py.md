# `pages.analytics` – Analytics Dashboard

**File:** `/app/cloned_repos/spotifydata/pages/analytics.py`

The `analytics` module implements the *Analytics* page of the Spotify Analyzer web‑app.  
It is a **Dash page** that shows:

* A navigation bar with links to the other pages (`Liked Songs`, `Recents`, `Analytics`, `Back`).
* A year selector (`dcc.Dropdown`) that pulls the list of years from the database.
* A dynamic content area (`target_div`) that displays:
  * A table of the top 3 albums for the selected year.
  * Two bar charts – *Most Popular Songs* and *Least Popular Songs* – for that year.

The page is registered with the URL pattern `/analytics/<username>`.

---

## 1. Imports & Dependencies

| Import | Purpose | File Path |
|--------|---------|-----------|
| `dash`, `dash.callback`, `dash.dcc`, `dash.html` | Core Dash components and callback decorators. | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (navbar, tables). | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `pandas as pd` | Data manipulation and DataFrame creation. | `/app/cloned_repos/spotifydata/pages/analytics.py` |
| `postgres` | Database helper functions for retrieving analytics data. | `/app/cloned_repos/spotifydata/pages/analytics.py` |

> **Note:** The `postgres` module is the only *external* dependency that provides data for this page.  
> All other imports are standard Dash or Python libraries.

---

## 2. Page Registration

```python
dash.register_page(__name__, path_template='/analytics/<username>')
```

* Registers the module as a Dash page.
* The `<username>` part of the URL is passed to the `layout` and callback functions.

---

## 3. `layout(username=None)`

### Purpose
Creates the static layout of the Analytics page.

### Key Elements

| Element | Description | Notes |
|---------|-------------|-------|
| `navbar` | `dbc.NavbarSimple` with four navigation links. | Uses `username` to build URLs. |
| `dcc.Dropdown` | Dropdown for selecting a year. | Options are the first element of each tuple returned by `postgres.get_years()`. |
| `target_div` | Empty container that will be populated by the callback. | Styled with margins for visual spacing. |

### Flow

1. Calls `postgres.get_years()` to obtain a list of available years.
2. Builds the navigation bar with links that include the current `username`.
3. Returns a `html.Div` containing the navbar, the year selector, and the empty `target_div`.

---

## 4. `analytics_display(value)`

### Purpose
Callback that updates `target_div` when a year is selected.

### Trigger
```python
@callback(
    Output('target_div', 'children'),
    [Input('year_drop', 'value')]
)
```

### Logic

| Step | Description | Data Source |
|------|-------------|-------------|
| 1 | **Check** if a year (`value`) is selected. | `value` from the dropdown. |
| 2 | **Retrieve albums** for the year. | `postgres.get_albums_for_year(value)` |
| 3 | **Compute most popular songs** (descending). | `postgres.get_popular_for_year(value, 'desc')` |
| 4 | **Compute least popular songs** (ascending). | `postgres.get_popular_for_year(value, 'asc')` |
| 5 | **Build bar charts** (`dcc.Graph`) for both popularity lists. | Uses the lists `most_pop_list`, `most_names_list`, `least_pop_list`, `least_names_list`. |
| 6 | **Create a DataFrame** of albums and convert it to a Bootstrap table. | `pd.DataFrame(albums, columns=['ALBUM', 'SONGS COUNT'])` |
| 7 | **Return** a list of components: heading, table, and two graphs. | These are rendered inside `target_div`. |
| 8 | **If no year selected**, return a placeholder message. | Simple `html.H1` with styling. |

#### Data Transformation Details

* `most_populars` and `least_populars` are lists of tuples where the 5th element (`j[4]`) represents the month (1‑12).  
* For each month, the popularity score is transformed to `j[2]*10 + 100` (arbitrary scaling) and the song name is stored.  
* The resulting lists are used as the `y` and `text` data for the bar charts.

---

## 5. Interaction with Other Modules

| Module | Interaction | Purpose |
|--------|-------------|---------|
| `pages.cred` | Calls `fetch_data(username)` to populate the database tables before the analytics page is accessed. | Ensures that `liked_songs`, `recents`, `artists`, and `albums` tables are up‑to‑date. |
| `pages.liked_songs` & `pages.recents` | Provide navigation links to the analytics page. | User can move between pages. |
| `postgres` | Supplies all data needed for analytics. | `get_years`, `get_albums_for_year`, `get_popular_for_year`. |

> **Dependency Rationale**  
> The analytics page relies on the `postgres` module because all analytics data (years, albums, popularity metrics) are stored in PostgreSQL.  
> The page does not directly interact with the Spotify API; that work is performed in `pages.cred.fetch_data`.

---

## 6. Usage Summary

1. **User logs in** via the root page (`pages.cred`).  
2. **Data is fetched** from Spotify and stored in PostgreSQL tables.  
3. **User navigates** to `/analytics/<username>`.  
4. The **dropdown** is populated with years from the database.  
5. When a year is selected, the **callback** queries the database, builds charts and a table, and displays them in `target_div`.

---

## 7. File‑Level Summary

```text
File: /app/cloned_repos/spotifydata/pages/analytics.py
- Registers a Dash page at /analytics/<username>
- Provides a layout with a navbar, year selector, and placeholder div
- Implements a callback that renders album table and popularity charts
- Depends on postgres module for data retrieval
- Uses Dash, Dash Bootstrap Components, and pandas for UI and data handling
```

---

### Missing Relationship Data

The evidence shows no `used_by` entries for `pages.analytics`.  
Therefore, no other modules explicitly import or call functions from this module beyond the Dash framework’s internal routing.  
If additional relationships exist, they are not captured in the provided evidence.
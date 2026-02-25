# `recents.py`

**File path**  
`/app/cloned_repos/spotifydata/pages/recents.py`

---

## Overview

`recents.py` defines a **Dash page** that displays a paginated table of the user’s most recently played songs.  
The page is registered with the Dash app under the URL pattern `/recents/<username>`.  
It pulls data from the PostgreSQL database via the `postgres` module, formats it with `pandas`, and renders it with `dash_bootstrap_components`.

---

## Dependencies

| Dependency | Why it exists | What functionality is imported / relied upon |
|------------|---------------|----------------------------------------------|
| `postgres` | The page needs to read the list of recent songs that have already been stored in the database. | `postgres.select_recent_songs(beg, end)` – returns a list of song tuples. |
| `dash` | Core Dash framework for building the app. | `dash.register_page` – registers the page with the app. |
| `dash.callback` | Declares the callback that updates the table when the pagination slider changes. | `@callback` decorator. |
| `dash.dcc` | Provides the `Slider` component used for pagination. | `dcc.Slider`. |
| `dash.dependencies.Input`, `dash.dependencies.Output`, `dash.dependencies.State` | Connects UI components to the callback. | `Input`, `Output`, `State`. |
| `dash.html` | Basic HTML components for layout. | `html.Div`, `html.H1`, etc. |
| `dash_bootstrap_components` | Bootstrap‑styled components for a nicer UI. | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink`, `dbc.Table`. |
| `math` | Calculates the number of pages needed for pagination. | `math.ceil`. |
| `pandas` | Converts raw tuples into a DataFrame for easy table rendering. | `pd.DataFrame`. |

> **Note:** All imports are explicitly listed in the module’s `external_dependencies` section of the evidence.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/recents/<username>')
```

* Registers this module as a page in the Dash app.  
* The `<username>` part of the URL is passed to the `layout` and `pages` functions as the `username` argument.

---

## Functions

### `layout(username=None)`

* **Purpose** – Builds the static part of the page (navbar, slider, empty table placeholder).  
* **Key Steps**  
  1. **Fetch data** – Calls `postgres.select_recent_songs(0)` to get all recent songs.  
  2. **Pagination** – Calculates `number_of_pages` using `math.ceil(number_of_recent_songs / 50)`.  
  3. **Navbar** – Uses `dbc.NavbarSimple` with links to *Liked Songs*, *Recents*, *Analytics*, and *Back*.  
  4. **Slider** – `dcc.Slider` with `min=1`, `max=number_of_pages`, `step=1`, and `marks` for each page number.  
  5. **Table placeholder** – An empty `html.Div` with `id='recents_table'` that will be populated by the callback.  
* **Return Value** – A `html.Div` containing the navbar, slider, and table placeholder.

### `pages(active_page, max)`

* **Purpose** – Callback that updates the table when the slider value changes.  
* **Inputs** – `active_page` (current slider value) and `max` (maximum slider value).  
* **Logic**  
  1. **Determine slice** – If the active page is the last page, call `postgres.select_recent_songs(active_page*50-50)`; otherwise call `postgres.select_recent_songs(active_page*50-50, active_page*50)`.  
  2. **Create DataFrame** – `pd.DataFrame(recent_songs, columns=column_names)`.  
  3. **Drop unnecessary columns** – `song_id` and `preview_url`.  
  4. **Render table** – `dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)`.  
* **Output** – The rendered table is returned to the `recents_table` component.

---

## Interaction with Other Modules

| Module | Relationship | Explanation |
|--------|--------------|-------------|
| `postgres` | **Used by** | `recents` calls `postgres.select_recent_songs` to fetch data. |
| `pages.liked_songs`, `pages.analytics`, `pages.tools` | **Not used by** | These pages are separate routes; they do not import or depend on `recents`. |
| `pages.cred` | **Not used by** | The login page does not import `recents`. |

> **Evidence**: The `used_by` list for `recents` is empty, indicating no downstream modules depend on it.

---

## Role in the System

* **User Interface** – Provides a visual, paginated view of the user’s recent listening history.  
* **Data Access** – Delegates data retrieval to the `postgres` module, keeping database logic separate.  
* **Reusability** – The layout and callback are self‑contained; they can be imported or modified without affecting other pages.  
* **Navigation** – The navbar links integrate the page into the overall application flow.

---

## Summary

`recents.py` is a self‑contained Dash page that:

1. Registers itself under `/recents/<username>`.  
2. Builds a navbar, pagination slider, and empty table placeholder.  
3. Uses a callback to fetch a slice of recent songs from PostgreSQL, format them with `pandas`, and render a Bootstrap table.  

All dependencies are explicitly imported, and the module does not influence or rely on any other page modules.
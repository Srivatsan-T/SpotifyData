# `pages.tools` – Tools Page

**File path**: `/app/cloned_repos/spotifydata/pages/tools.py`

The `tools` module is a Dash page that provides a navigation bar and a simple greeting for a logged‑in Spotify user. It is registered with Dash’s page system and renders a layout that can be used by the main application.

---

## Overview

```python
import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path_template='/tools/<username>')

def layout(username=None):
    ...
```

- **Purpose**: Render the “Tools” page for a specific Spotify username.
- **Key UI elements**:
  - A Bootstrap‑styled navigation bar (`dbc.NavbarSimple`) with links to *Liked Songs*, *Recents*, and *Analytics*.
  - A greeting that displays the user’s first name.
  - A simple layout wrapped in a full‑width `<div>`.

---

## Dependencies

| Dependency | Why it exists | Functionality used |
|------------|---------------|--------------------|
| `dash` | Registers the page and provides the `Output`/`Input` decorators used elsewhere in the app. | `dash.register_page` |
| `dash.html` | Provides HTML components (`Div`, `H1`, `H5`, etc.). | `html.Div`, `html.H1`, `html.H5` |
| `dash_bootstrap_components` | Supplies Bootstrap‑styled components for the navigation bar. | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink` |

> **Note**: No external data‑access or business‑logic modules are imported here; the page is purely presentational.

---

## API

### `layout(username=None)`

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `username` | `str` | `None` | The Spotify username extracted from the URL. It may contain URL‑encoded spaces (`%20`). |

#### Returns
- `dash.html.Div`: A container that includes:
  - A navigation bar with links to other pages.
  - A greeting section that displays “Hello” and the user’s first name.
  - A subtitle encouraging navigation.

#### Implementation Details

```python
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Liked Songs",
                                href=f'http://localhost:8050/liked/{username}',
                                id='LikedSongs')),
        dbc.NavItem(dbc.NavLink("Recents",
                                href=f'http://localhost:8050/recents/{username}',
                                id="Recents")),
        dbc.NavItem(dbc.NavLink("Analytics",
                                href=f'http://localhost:8050/analytics/{username}',
                                id="Analytics"))
    ],
    brand="Spotify Analyzer",
    brand_href="http://localhost:8050/",
    className='box-form left'
)

first_name = str(username).split('%20')[0]

return html.Div(
    [
        navbar,
        html.Div(
            [
                html.H1("Hello", style={'font-size':'10vmax','color':'white'}),
                html.H1(first_name, style={'font-size':'10vmax','color':'white'}),
                html.H5("use the navigation links to access various features of the tool",
                        style={'color':'white'})
            ],
            style={"padding-left":"25px","padding-top":'10px'}
        )
    ],
    style={'width':'100vw'}
)
```

- **Username parsing**: `first_name = str(username).split('%20')[0]` extracts the first part of the username before any URL‑encoded space.
- **Styling**: Inline CSS is used for font size, color, and padding.

---

## Usage

- **Page registration**: `dash.register_page` makes this module discoverable by the Dash app. The URL pattern `/tools/<username>` will trigger this layout.
- **Navigation**: The navbar links use the same `username` value to keep the user context when moving to *Liked Songs*, *Recents*, or *Analytics* pages.
- **Integration**: The main Dash application imports this module implicitly via the page registry; no explicit import is required elsewhere.

---

## Relationships

- **Dependencies**: None beyond the standard Dash and Bootstrap components.
- **Used by**: No explicit `used_by` entries are present in the evidence. The module is consumed by the Dash app’s page system.

---

## Summary

`pages.tools` is a lightweight, self‑contained page that:

1. Registers itself with Dash under `/tools/<username>`.
2. Builds a navigation bar linking to other user‑specific pages.
3. Greets the user by first name and encourages navigation.

It relies solely on Dash’s core and Bootstrap components, making it easy to maintain and extend.
# `pages.tools` – Tool Page for the Spotify Analyzer

**File path**  
`/app/cloned_repos/spotifydata/pages/tools.py`

---

## Overview

`pages.tools` is a Dash page that provides a simple navigation bar and a greeting for the user.  
It is registered as a dynamic route (`/tools/<username>`) and is intended to be the landing page after a user logs in.

The module has no internal dependencies on other parts of the codebase – it only relies on external libraries for UI rendering.

---

## Imports & External Dependencies

| Import | Purpose |
|--------|---------|
| `dash` | Core Dash framework for page registration and callbacks. |
| `dash.html` | HTML component helpers (`html.Div`, `html.H1`, etc.). |
| `dash_bootstrap_components as dbc` | Bootstrap‑styled components (`NavbarSimple`, `NavItem`, `NavLink`). |

These dependencies are required to build the page layout and navigation bar.

---

## Page Registration

```python
dash.register_page(__name__, path_template='/tools/<username>')
```

* **Why** – Registers this module as a Dash page that accepts a dynamic `username` segment.  
* **What** – Makes the page discoverable by Dash’s page routing system.  
* **File reference** – `pages/tools.py`

---

## `layout` Function

```python
def layout(username=None):
```

### Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `username` | `str` | `None` | The Spotify username extracted from the URL. It is used to build navigation links and to display a personalized greeting. |

### Functionality

1. **Navbar Construction**  
   * Uses `dbc.NavbarSimple` with three navigation links:  
     * **Liked Songs** → `/liked/<username>`  
     * **Recents** → `/recents/<username>`  
     * **Analytics** → `/analytics/<username>`  
   * The navbar is styled with the class `box-form left`.

2. **Greeting**  
   * Splits the `username` on `%20` (URL‑encoded space) and takes the first part as `first_name`.  
   * Displays a large, white‑text greeting:  
     * `"Hello"`  
     * `<first_name>`  
     * A subtitle prompting the user to use the navigation links.

3. **Return Value**  
   * An `html.Div` containing the navbar and the greeting section.  
   * The outer `Div` is styled with `{'width': '100vw'}` to span the viewport width.

### Example Return Structure

```html
<div style="width:100vw;">
  <div class="box-form left">  <!-- Navbar -->
    ...
  </div>
  <div style="padding-left:25px; padding-top:10px;">
    <h1 style="font-size:10vmax;color:white;">Hello</h1>
    <h1 style="font-size:10vmax;color:white;"><first_name></h1>
    <h5 style="color:white;">use the navigation links to access various features of the tool</h5>
  </div>
</div>
```

### Usage

* The Dash application automatically calls `layout` when the user navigates to `/tools/<username>`.  
* The returned layout is rendered as the page content.  
* The navigation links rely on the same `username` to keep the session context.

---

## Dependencies Summary

| Dependency | Reason | Functionality Used |
|------------|--------|--------------------|
| `dash` | Page registration and callback infrastructure | `dash.register_page` |
| `dash.html` | Building HTML components | `html.Div`, `html.H1`, `html.H5` |
| `dash_bootstrap_components` | Bootstrap‑styled navigation bar | `dbc.NavbarSimple`, `dbc.NavItem`, `dbc.NavLink` |

No internal modules are imported; therefore, there are no downstream dependencies (`used_by` is empty).

---

## Documentation Summary

- **Module**: `pages.tools` – provides a simple, user‑friendly landing page after login.  
- **Key Function**: `layout(username)` – builds the page layout with a navbar and greeting.  
- **External Libraries**: Dash core, Dash HTML, Dash Bootstrap Components.  
- **Routing**: Registered as `/tools/<username>`.  
- **No downstream usage** – the module is self‑contained and only renders UI.

Feel free to extend the page with additional components or callbacks as needed, but keep in mind that the current implementation is intentionally lightweight.
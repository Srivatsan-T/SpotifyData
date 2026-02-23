# `pages.tools` – Tool Page for the Spotify Analyzer

**File path**  
`/app/cloned_repos/spotifydata/pages/tools.py`

---

## Overview

`pages.tools` is a Dash page that provides a simple navigation bar and a greeting for a logged‑in user.  
It is registered with Dash using a dynamic URL template (`/tools/<username>`), so the page can be accessed as:

```
http://localhost:8050/tools/<username>
```

The page is the landing spot after a user logs in and fetches their Spotify data.

---

## Imports & External Dependencies

| Import | Purpose | Why it exists |
|--------|---------|---------------|
| `dash` | Core Dash framework | Provides `dash.register_page` and the `callback` decorator. |
| `dash.html` | HTML component factory | Used to create `<div>`, `<h1>`, `<h5>` elements. |
| `dash_bootstrap_components` (aliased as `dbc`) | Bootstrap‑styled components | Supplies `NavbarSimple`, `NavItem`, and `NavLink` for a responsive navigation bar. |

> **Note:** No other modules import `pages.tools`, and it is not referenced by any other part of the codebase (`used_by` is empty).

---

## Page Registration

```python
dash.register_page(__name__, path_template='/tools/<username>')
```

- **`__name__`** – Registers this module as a Dash page.
- **`path_template`** – Enables a dynamic segment (`<username>`) in the URL, which is passed to the `layout` function.

---

## `layout` Function

```python
def layout(username=None):
    ...
```

### Parameters

- `username` (str, optional) – The Spotify username extracted from the URL.  
  It defaults to `None` when the page is accessed without a username, but in practice the app always supplies it.

### Workflow

1. **Navigation Bar (`navbar`)**  
   - Built with `dbc.NavbarSimple`.  
   - Contains three navigation links:
     - **Liked Songs** → `/liked/<username>`
     - **Recents** → `/recents/<username>`
     - **Analytics** → `/analytics/<username>`
   - Uses `brand="Spotify Analyzer"` and a custom CSS class `box-form left`.

2. **User Greeting**  
   - `first_name` is extracted by splitting the `username` on `%20` (URL‑encoded space) and taking the first part.  
   - Two large white headings display `"Hello"` and the extracted first name.  
   - A smaller instruction heading tells the user to use the navigation links.

3. **Return Value**  
   - A top‑level `html.Div` containing the navbar and greeting.  
   - The outer div is styled with `{'width': '100vw'}` to span the full viewport width.

### Example Output

```html
<div style="width:100vw;">
  <div class="navbar-simple box-form left">
    <!-- Navigation links -->
  </div>
  <div style="padding-left:25px; padding-top:10px;">
    <h1 style="font-size:10vmax;color:white;">Hello</h1>
    <h1 style="font-size:10vmax;color:white;"><first_name></h1>
    <h5 style="color:white;">use the navigation links to access various features of the tool</h5>
  </div>
</div>
```

---

## Usage in the Application

- **Entry Point** – After a user logs in via `pages.cred`, the callback `button_on_clicked` redirects to `/tools/<username>`.  
- **Navigation** – The navbar links allow the user to jump to the Liked Songs, Recents, or Analytics pages, each of which also accepts the same `<username>` parameter.  
- **No Further Dependencies** – The module does not import or call any functions from other modules; it only builds UI components.

---

## Summary

- **Purpose** – Provide a welcoming, navigable landing page for a logged‑in Spotify user.  
- **Key Components** – Dash page registration, Bootstrap navbar, dynamic greeting.  
- **Dependencies** – `dash`, `dash.html`, `dash_bootstrap_components`.  
- **Integration** – Registered as `/tools/<username>` and used as the default landing page after login.  
- **No downstream consumers** – The module is self‑contained and not referenced by any other part of the codebase.
---
name: fasthtml
description: Build, debug, and extend FastHTML apps that use FastTags, HTMX, Starlette primitives, and optionally fastlite or MonsterUI. Use when Codex is asked to create a FastHTML project, add or change routes and FT components, wire forms or HTMX swaps, implement session/auth Beforeware, add SSE or websocket flows, work with fastlite CRUD, style a FastHTML UI, or troubleshoot FastHTML-specific APIs and idioms.
---

# FastHTML

## Overview
Use this skill for HTML-first Python apps built with FastHTML. Prefer server-rendered FT trees, HTMX swaps, and Starlette-compatible responses over SPA patterns or FastAPI-style abstractions.

## Core Rules
- Import `from fasthtml.common import *` unless a narrower import is clearly better.
- Prefer `app, rt = fast_app()` for straightforward apps; use `FastHTML(...)` when explicit app configuration is needed.
- Treat FastHTML as HTML-first. Do not default to FastAPI syntax or API-first design.
- Use route function objects directly in `href`, `action`, `hx_get`, and `hx_post`; call `.to(...)` when query params are needed.
- Use `Titled(...)` when a page title and H1 are needed. Do not wrap it in another `Container`.
- Use `serve()`; do not add a manual `if __name__ == "__main__"` guard around it.
- Prefer Python and FT composition over handwritten JS. Do not reach for React, Vue, or Svelte.
- Remember that Pico CSS is included by default; disable it with `pico=False` only when needed.

## Workflow
1. Inspect the current app shape: `fast_app()` vs `FastHTML(...)`, headers/extensions, beforeware, database layer, and styling approach.
2. Pick the narrowest implementation path:
   - page or partial rendering
   - form or CRUD flow
   - auth/session gate
   - SSE or websocket flow
   - fastlite-backed data
   - MonsterUI-based presentation
3. Implement server-rendered first. Let HTMX request and swap partials; add JS only for small client behavior or library wrappers.
4. Verify changed routes with `TestClient` when practical, including `HX-Request: 1` when partial behavior matters.

## FastHTML Patterns

### Routing and Handlers
- Decorate handlers with `@rt` or `@app.route(...)`.
- Omit the path when the function name should become the route. `index()` maps to `/`.
- Expect GET and POST to be available by default unless you restrict methods explicitly.
- Use type annotations for query, path, and form coercion.
- Rely on special injected params when useful: `request` or `req`, `session` or `sess`, `auth`, `htmx`, and `app`.
- Remember plain parameter lookup order: path, query, cookies, headers, session, then form data.
- Use `APIRouter` when routes need to live across modules.

### FT Composition and Responses
- Treat positional args as children and keyword args as HTML attributes.
- Use `cls`, `_for` or `fr`, and dict unpacking for special attributes such as `@click`.
- Return FT components or tuples of FT components for HTML responses.
- Return Starlette response classes directly when status codes, redirects, file responses, or custom media types matter.
- Define reusable UI as Python functions or with `__ft__` on domain objects.
- Treat strings as escaped text; only use trusted raw HTML helpers such as `NotStr(...)` when necessary.

### Forms and Data Binding
- Use `Form(...)`; it defaults to `multipart/form-data`.
- Bind dataclasses, namedtuples, TypedDict-like objects, or flexiclasses directly from form submissions.
- Use `fill_form()` to populate edit forms from existing objects.
- Use `CheckboxX` when a boolean field must still submit a value when unchecked.
- Accept `UploadFile` or `list[UploadFile]` for file uploads and prefer `async` handlers around IO.

### HTMX, SSE, and Websockets
- Reach for `hx_get`, `hx_post`, `hx_target`, `hx_swap`, `hx_trigger`, and `hx_swap_oob` first.
- Use `HtmxResponseHeaders(...)` or redirects when HTMX-specific response behavior is required.
- Add `exts='ws'` plus `ws_send=True` and `ws_connect=...` for websocket flows.
- Use `EventStream(...)` and `sse_message(...)` for SSE.
- Return partials that update the target cleanly; use out-of-band swaps for side updates and form resets.

### State, Auth, and Storage
- Put auth and session gating in `Beforeware`.
- Set `req.scope['auth']` in beforeware and consume it through the injected `auth` handler arg.
- Prefer `RedirectResponse(..., status_code=303)` after POST-style actions such as login or logout.
- Use `fastlite` for simple SQLite-backed CRUD and `xtra()` for per-user scoping.
- Reach for raw Starlette middleware, request objects, or background tasks only when FastHTML helpers are not enough.

### Styling
- Keep Pico defaults for simple work.
- Use MonsterUI when richer UI components or Tailwind/Uikit-style building blocks are required.
- Prefer MonsterUI defaults, `Label*` form helpers, and `ButtonT.*` classes instead of hand-assembling repeated class strings.

## Reference Workflow
- Start with `references/topic-map.md`.
- Open only the relevant slice of `references/fasthtml-llms-ctx.txt`; it is large.
- Use these search anchors before reading the full reference:

```bash
rg -n '^## (Minimal App|Responses|Testing|Form Handling and Data Binding|Auth|Server-Side Events \\(SSE\\)|Websockets|Fastlite|MonsterUI)$' references/fasthtml-llms-ctx.txt
rg -n '^## fasthtml\\.(components|core|fastapp|js|jupyter|live_reload|oauth|pico|svg|xtend)$' references/fasthtml-llms-ctx.txt
rg -n 'hx_(get|post|target|swap|trigger)|hx_swap_oob|ws_connect|ws_send|EventStream|fill_form|Beforeware|RedirectResponse' references/fasthtml-llms-ctx.txt
```

## References
- Topic guide: `references/topic-map.md`
- Bundled source context: `references/fasthtml-llms-ctx.txt`

# FastHTML Topic Map

Use this file to decide which slice of `fasthtml-llms-ctx.txt` to load. Open the smallest range that answers the current task.

## Section Map
- Lines `1-16`: Source list and high-level project reminders.
- Lines `17-576`: Core FastHTML guide.
- Lines `577-687`: `fastlite` overview and CRUD usage.
- Lines `688-797`: MonsterUI overview and examples.
- Lines `798-1079`: HTMX attribute, class, header, event, JS API, and config reference.
- Lines `1081-1376`: Starlette quick guide for responses, redirects, request context, exceptions, background tasks, and middleware.
- Lines `1377-1909`: FastHTML API list by module.
- Lines `1910-2104`: End-to-end todo app walkthrough.

## Targeted Reads
- App skeleton, routing, FT basics, and response behavior:
  - `sed -n '51,324p' references/fasthtml-llms-ctx.txt`
- Auth, sessions, router organization, toasts, SSE, websockets, and uploads:
  - `sed -n '325,576p' references/fasthtml-llms-ctx.txt`
- `fastlite` data layer:
  - `sed -n '577,687p' references/fasthtml-llms-ctx.txt`
- MonsterUI usage:
  - `sed -n '688,797p' references/fasthtml-llms-ctx.txt`
- HTMX lookup:
  - `sed -n '798,1079p' references/fasthtml-llms-ctx.txt`
- Starlette interop:
  - `sed -n '1081,1376p' references/fasthtml-llms-ctx.txt`
- Function and class lookup by module:
  - `sed -n '1377,1909p' references/fasthtml-llms-ctx.txt`
- Full CRUD example:
  - `sed -n '1910,2104p' references/fasthtml-llms-ctx.txt`

## Search Hints
- Find core FastHTML sections:
  - `rg -n '^## (Minimal App|Testing|Form Handling and Data Binding|Auth|Server-Side Events \\(SSE\\)|Websockets|Fastlite|MonsterUI)$' references/fasthtml-llms-ctx.txt`
- Find HTMX attribute or event help:
  - `rg -n 'hx-|HX-|htmx:' references/fasthtml-llms-ctx.txt`
- Find FastHTML module APIs:
  - `rg -n '^## fasthtml\\.' references/fasthtml-llms-ctx.txt`
- Find the idiomatic todo sample:
  - `rg -n 'Todo list application|Walkthrough of an idiomatic fasthtml app' references/fasthtml-llms-ctx.txt`

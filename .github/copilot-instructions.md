Purpose
-------
Short, actionable notes for an AI coding agent to be productive in this repository.

Big picture (what this repo does)
---------------------------------
- Single-file Flask app (app.py) that serves a small frontend (templates/index.html + static/*) and exposes one JSON endpoint: POST /api/jules.
- The server proxies user-provided inputs to the external Jules API at https://jules.googleapis.com/v1alpha/sessions. The external API is the primary integration point.
- Sphinx docs live under `docs/`; Render deployment configuration is in `render.yaml`.

Essential data flow (read these files)
-------------------------------------
- Frontend form -> `templates/index.html` (fields: org, repo, branch, title, prompt)
- Client JS -> `static/js/scripts.js` (serializes form, POSTs to /api/jules, expects JSON)
- Server handler -> `app.py` (route: `jules_api`) builds payload and sends to Jules. Key payload fields: `prompt`, `sourceContext.source` (format: `sources/github/{org}/{repo}`), `githubRepoContext.startingBranch`, `title`.

Important dev commands and workflows
-----------------------------------
- Local dev (fast):
  - Create venv and install deps: `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt` (see `requirements.txt`).
  - Set the Jules API key env var: `export JULES_API_KEY=...` (app reads `JULES_API_KEY`).
  - Run locally: `python app.py` — Flask runs in debug on 127.0.0.1:5000.
- Production / container: `render.yaml` expects `buildCommand: pip install -r requirements.txt` and `startCommand: gunicorn app:app`.
- Docs: `cd docs && make html` to build Sphinx HTML (`docs/conf.py`).

Project-specific conventions & gotchas
-------------------------------------
- Secrets: Jules key must be provided via environment variable `JULES_API_KEY`. The server forwards it as header `X-Goog-Api-Key`.
- No GitHub API calls are made locally — the string `sources/github/{org}/{repo}` is passed to Jules so Jules will resolve repo context. Do not attempt to fetch GitHub content locally unless adding that feature.
- Error handling pattern: `app.py` returns JSON error objects with HTTP 500 on upstream failures. Client code in `static/js/scripts.js` expects JSON `{ error: '...' }` on failure.
- Single-file service: this codebase uses a small, monolithic structure (no blueprints or factories). New features should follow the same simple pattern or be refactored into blueprints explicitly.

Integration points and payload shape (explicit)
----------------------------------------------
- Request to Jules (constructed in `app.py`):
  {
    "prompt": string,
    "sourceContext": { "source": "sources/github/{org}/{repo}", "githubRepoContext": { "startingBranch": "{branch}" } },
    "title": string
  }
- Header: `X-Goog-Api-Key: <JULES_API_KEY>`

Where to make safe changes / tests
----------------------------------
- To add unit tests: create `tests/test_api.py` and use Flask's `app.test_client()` to POST to `/api/jules`. Mock `requests.post` (the external call) to assert payload and simulate responses.
- For retries/backoff on the Jules call, create a `requests.Session()` with a Retry adapter in `app.py` and replace the inline `requests.post` usage.

Files to inspect first
---------------------
- `app.py` — core server logic and Jules integration (line: jules_api handler)
- `templates/index.html` and `static/js/scripts.js` — client-side expectations/shape
- `render.yaml` — deployment commands (gunicorn) and env var key name
- `requirements.txt` — pinned deps (Flask, requests, gunicorn)
- `docs/` — sphinx docs and build process

If you change the external payload shape
--------------------------------------
- Update both `app.py` and `static/js/scripts.js` (the server expects specific fields and the client emits them). Add validation on the server to fail fast and return clear JSON errors.

What I did / merge notes
------------------------
- No existing `.github/copilot-instructions.md` detected, so this file was created.

Questions for the repo owner
---------------------------
- Do you want automated tests added to this repo (pytest + a simple test that mocks the Jules call)?
- Should the agent add a health-check endpoint and basic logging before PRs that change networking code?

End of instructions.
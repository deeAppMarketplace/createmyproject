# Contributing

Quick start for local development and commits.

1. Create and activate virtualenv:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Enable local git hooks to prevent committing `.env`:

```bash
git config core.hooksPath .githooks
```

4. Run tests:

```bash
pytest -q
```

If you add or change environment-sensitive behavior, update `README.md` and include tests where practical.

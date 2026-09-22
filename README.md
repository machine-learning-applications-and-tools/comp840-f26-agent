# COMP840 / COMP740 — ML Applications and Tools

**This repository is yours for the rest of the term.** Weeks 3 to 12 all
build on it. Do not start a new one each week.

This file stays stable all term -- it only ever gains one new line in
"This week" below. Everything week-specific lives in that week's own
`weekNN-README.md`.

## Setup

One-time, from Week 3. If your `.venv` still works, you do not need to
redo this.

```bash
python3 -m venv .venv          # Windows: python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Your `.env` holds `GEMINI_API_KEY`, also set up once, in Week 3.

## Pulling each week's files

See `UPDATING.md` for the one-time remote setup and how the weekly pull
works. Each week's own `weekNN-README.md` has that week's exact file
list to pull.

## This week

Open the README for the current week:

- `week03-README.md` — The harness
- `week04-README.md` — The planner

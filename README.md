# Transformers-v1

> "Autobots, transform and roll out!"

Transformers-v1 is a small Python engine, inspired by the Transformers movies, that
transforms one software artifact into another. Point it at a file and tell it what
you want back — a specialist **Autobot** handles the conversion, dispatched by their
leader, **Optimus Prime**.

## The fleet

| Bot | Conversions |
|---|---|
| **Optimus Prime** | Detects the input format and rolls out the right bot for the job |
| **Bumblebee** | `json` ⇄ `yaml` |
| **Ironhide** | `csv` ⇄ `json` |
| **Ratchet** | `markdown` → `html` |
| **Jazz** | `python` → `python-min` (strip comments/blank lines), `python` → `python-pretty` (canonical reformat) |

The engine is also available over HTTP (FastAPI) with an **Angular** web console on
top, so you can roll out an Autobot from the browser instead of the CLI.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,api]"
```

## Usage

```bash
# See the fleet and what each bot can do
transformers-v1 list-bots

# Transform a file — output format/extension is auto-picked from --to
transformers-v1 transform data.json --to yaml
transformers-v1 transform team.csv --to json
transformers-v1 transform notes.md --to html
transformers-v1 transform script.py --to python-min

# Or point it at an explicit output path
transformers-v1 transform data.json --to yaml -o out/data.yaml
```

Example:

```
$ transformers-v1 transform data.json --to yaml
Optimus Prime scanning data.json... detected: json
Rolling out Bumblebee (json -> yaml)...
Wrote data.yaml
```

You can also run it as a module without installing the console script:

```bash
python -m transformers_v1 transform data.json --to yaml
```

## Web console (FastAPI + Angular)

The Angular frontend talks to a small FastAPI backend that wraps the same
Optimus Prime / Autobot registry used by the CLI — no logic is duplicated.

**1. Start the backend** (from the repo root, with the venv above active):

```bash
uvicorn transformers_v1.api:app --port 8000
```

This exposes:
- `GET /api/bots` — the roster and each bot's supported conversions
- `POST /api/transform` — `{ "content", "from_format", "to_format" }` → `{ "bot_name", "result" }`

**2. Start the frontend** (in another terminal):

```bash
cd frontend
npm install
npm start   # ng serve — proxies /api to http://127.0.0.1:8000, see proxy.conf.json
```

Then open http://localhost:4200 — pick a format, paste content, and hit **Roll Out!**

Frontend unit tests: `cd frontend && npm test`.

## Extending the fleet

Every bot is a small class in `transformers_v1/bots/` implementing `TransformerBot`:
declare which `(from_format, to_format)` pairs it supports and a `transform()` method.
Register a new bot in `OptimusPrime.__init__` (`transformers_v1/registry.py`) and it
joins the roster automatically — `list-bots` and the CLI pick it up for free.

## Tests

```bash
pytest
```

# stmtool

Standalone CLI (Typer + Rich) for the [stm32-sdk](https://github.com/khosta77/stm32-sdk)
bare-metal C++20 SDK. Scaffolds projects, builds firmware in the SDK Docker
image, runs host tests, flashes boards, manages the SDK cache. Ships with **no
SDK content** — a thin client over an SDK checkout (west-style separation).

## Relationship to stm32-sdk (must follow)

`stmtool` used to live inside the SDK monorepo at `tools/stmtool/`. Since v0.2.1
it is a **separate repository** (`khosta77/stmtool`, this repo). Consequences:

- Any change to the tool goes **here**, never back into `stm32-sdk/tools/`
  (that path is gone). If a task in the SDK repo turns out to need a `stmtool`
  change, make it in this repo and release it (a new `v0.N` tag), then point the
  SDK at it.
- The SDK repo consumes `stmtool` by installing it from this repo
  (`pip install git+https://github.com/khosta77/stmtool.git`) in its
  `build.yml`; it does not vendor the code.
- The tool must stay SDK-content-free: templates, drivers, and the CMake
  toolchain live in the SDK repo and are resolved at runtime via the SDK root
  (`STMSDK_PATH` / cache / clone). Do not bundle SDK assets into this package.

## Layout

`src/stmtool/` (src-layout) — `cli.py` (Typer app + Docker orchestration),
`project.py` (SDK-root resolution, cache clone/checkout, template scaffolding —
the SDK-coupling hub), `sdk.py` (`stmtool sdk` cache backend), `config.py`
(`stmproject.toml` loader), `completions.py`, `i18n.py` (en/ru). Tests in
`tests/`.

## Versioning

`0.N`: major pinned at `0`, minor auto-bumped by CI on every merge to `master`
(`.github/workflows/autotag.yml` pushes the next `v0.N` tag;
`poetry-dynamic-versioning` reads it). **No hand-edited version constant** —
`__version__` comes from `importlib.metadata`. Do not add a static version or
tag manually except to bootstrap.

## Python rules

Senior Python (3.10+). PEP 8, full type hints on signatures. `snake_case`
functions/vars, `PascalCase` classes, `UPPER_SNAKE_CASE` constants. Specific
exception types (no bare `except`). Do **not** write code comments unless asked.

- **`poetry run poe ci` must pass before any commit**: ruff, flake8, black,
  isort, mypy (strict), bandit, pylint, pytest with >= 70% coverage.
- Do **not** add `# noqa`, `# type: ignore`, `--ignore=`, or `disable=`
  without explicit user approval. If a linter floods with errors, stop and ask
  whether to disable the rule or fix every occurrence — never decide unilaterally.
- `poetry run poe fix` runs the auto-fixers (ruff, isort, black, ruff format);
  results must still pass `poe ci`.
- Commit messages are English **Conventional Commits**. Pull requests target
  `master`.

## Docs to keep in sync

New / changed command or flag → update `README.md` (command + env-var tables)
and, in the SDK repo, `docs/stmtool.md` + `docs/stmtool.ru.md` and the README
command table (the SDK docs site is the user-facing reference).

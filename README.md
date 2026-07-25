# stmtool

[![CI](https://github.com/khosta77/stmtool/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/khosta77/stmtool/actions/workflows/ci.yml)

`stmtool` is the command-line companion for the
[stm32-sdk](https://github.com/khosta77/stm32-sdk) bare-metal C++20 SDK. It
scaffolds projects from templates, builds firmware inside the SDK Docker image,
runs the host unit tests, flashes boards, and manages the local SDK cache.

The tool ships **without any SDK content** — like `west` for Zephyr, it is
installed once and points at whichever SDK checkout you tell it to (via
`STMSDK_PATH`, the `~/.stmtool/stm32-sdk/` cache, or an auto-clone). The SDK it
manages lives in its own repository and carries the drivers, templates, and
CMake toolchain.

## Install

Recommended (isolated, via pipx):

```bash
pipx install git+https://github.com/khosta77/stmtool.git
```

Pin to a specific release tag:

```bash
pipx install "git+https://github.com/khosta77/stmtool.git@v0.1"
```

Upgrade later with `pipx upgrade stmtool`. Plain `pip install
git+https://github.com/khosta77/stmtool.git` also works if you prefer a shared
environment.

Requires Python >= 3.10 and Docker (all firmware builds run inside the SDK
image). `stmtool doctor` verifies the environment.

## Quick start

```bash
stmtool project create my-blink --chip STM32F407VG
cd my-blink
stmtool build          # builds in the SDK Docker image; artifacts in out/
stmtool flash
```

## Commands

| Command | Description |
|---------|-------------|
| `stmtool project create <name> --chip <chip> [--template <tpl>] [--with-claude]` | Create a new project from a template |
| `stmtool project templates` | List available templates |
| `stmtool build [--release] [--clean] [--chip <chip>] [--verbose]` | Build the current project in Docker (artifacts in `out/`) |
| `stmtool test [--verbose]` | Build and run the SDK host unit tests in Docker |
| `stmtool flash [--tool <tool>] [--erase]` | Flash firmware onto the connected board |
| `stmtool sdk update [--version <tag>]` | Update the cached SDK to a tag or `develop` |
| `stmtool sdk list-versions` | List available SDK versions (git tags) |
| `stmtool sdk path` | Print the resolved SDK root path |
| `stmtool doctor` | Check the development environment |
| `stmtool completion <shell>` | Print a shell-completion script (`bash`/`zsh`/`fish`) |
| `stmtool show-version` | Print the `stmtool` version |

## Environment variables

| Variable | Description |
|----------|-------------|
| `STMSDK_PATH` | Explicit SDK root. Overrides the cache lookup. |
| `STMTOOL_SDK_REPO` | SDK git URL to clone into the cache (default: upstream `stm32-sdk`). |
| `STMTOOL_DOCKER_IMAGE` | SDK build image (default: `ghcr.io/khosta77/stm32-sdk-build:latest`). |
| `STMTOOL_LANG` | UI language: `en` (default), `ru`. |

## SDK resolution order

When a command needs the SDK root, `stmtool` looks in this order:

1. `STMSDK_PATH` environment variable.
2. A parent directory of the running executable that contains both `sdk/` and
   `templates/` (in-source checkouts).
3. `~/.stmtool/stm32-sdk/` cache — created on first use by cloning
   `STMTOOL_SDK_REPO`.

`stmtool sdk update` / `list-versions` / `path` manage that cache.

## Versioning

The version is `0.N`: the major is pinned at `0`, the minor is a running release
counter bumped automatically by CI on every merge to `main` (an `autotag`
workflow pushes the next `v0.N` tag; `poetry-dynamic-versioning` reads it at
build time). There is no hand-edited version constant — `stmtool version`
reports whatever the installed distribution metadata says.

## Development

```bash
poetry install --with dev
poetry run poe ci     # ruff, flake8, black, isort, mypy (strict), bandit, pylint, pytest >=70%
poetry run poe fix    # auto-fixers
```

Commits follow Conventional Commits (English). See
[CONTRIBUTING is folded into CLAUDE.md / AGENTS.md]. Changes are opened as pull
requests against `main`.

## License

MIT.

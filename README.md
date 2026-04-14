# morpheus — Autonomous Coding Agent. Autonomous coding agent orchestrator

Autonomous Coding Agent. Autonomous coding agent orchestrator. morpheus gives you a focused, inspectable implementation of that idea.

## Why morpheus

morpheus exists to make this workflow practical. Autonomous coding agent. autonomous coding agent orchestrator. It favours a small, inspectable surface over sprawling configuration.

## Features

- CLI command `morpheus`
- `TaskStatus` — exported from `src/morpheus/core.py`
- `Task` — exported from `src/morpheus/core.py`
- `CodeBlock` — exported from `src/morpheus/core.py`
- Included test suite
- Dedicated documentation folder

## Tech Stack

- **Runtime:** Python
- **Frameworks:** Click
- **Tooling:** Pydantic, Rich

## How It Works

The codebase is organised into `docs/`, `src/`, `tests/`. The primary entry points are `src/morpheus/core.py`, `src/morpheus/cli.py`, `src/morpheus/__init__.py`. `src/morpheus/core.py` exposes `TaskStatus`, `Task`, `CodeBlock` — the core types that drive the behaviour. `src/morpheus/cli.py` exposes functions like `main`, `plan`, `run`.

## Getting Started

```bash
pip install -e .
morpheus --help
```

## Usage

```bash
morpheus --help
```

## Project Structure

```
morpheus/
├── .env.example
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── README.md
├── docs/
├── pyproject.toml
├── src/
├── tests/
```

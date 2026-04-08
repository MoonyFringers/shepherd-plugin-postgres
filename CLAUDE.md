# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository layout

```
plugin.yaml                  # Shepherd plugin descriptor (required at archive root)
src/
  postgres_plugin/
    __init__.py              # Package marker
    main.py                  # ShepherdPlugin subclass (entrypoint)
    commands.py              # All Click commands and groups
    completion.py            # Tab-completion provider and verb/subcommand tables
  tests/                     # pytest test suite
  resources/
    plugin.conf              # Logging configuration (log_level, log_stdout, log_format)
  pyproject.toml         # black / isort / pyright / pytest configuration
  requirements.txt       # runtime dependencies
  requirements-dev.txt   # dev-only dependencies
  .flake8                # flake8 configuration
  .coveragerc            # coverage configuration
  version                # plain-text semver, kept in sync with plugin.yaml
shepherd/                # git submodule — upstream Shepherd runtime (read-only)
```

> `shepherd/` is a **read-only reference**.  Never modify files under it.

---

## Development environment

### Virtual environment (project root)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r src/requirements.txt -r src/requirements-dev.txt
```

### PYTHONPATH

Both `src/` (plugin package) and `shepherd/src/` (Shepherd runtime symbols)
must be on `PYTHONPATH`.  The canonical approach is via `direnv`:

```bash
direnv allow .   # reads .envrc which sets PYTHONPATH automatically
```

Without `direnv`:

```bash
export PYTHONPATH="$PWD/src:$PWD/shepherd/src${PYTHONPATH:+:$PYTHONPATH}"
```

### VS Code / Pylance

Create local, **untracked** workspace files:

`.vscode/settings.json`

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.extraPaths": [
    "${workspaceFolder}/src",
    "${workspaceFolder}/shepherd/src"
  ],
  "python.envFile": "${workspaceFolder}/.env"
}
```

`.env`

```
PYTHONPATH=src:shepherd/src
```

---

## Quality checks

Run all checks (mirrors CI / pre-commit):

```bash
pre-commit run --all-files
```

Run individually (all scoped to `src/`):

```bash
black --config src/pyproject.toml src
isort --sp src/pyproject.toml src
flake8 --config src/.flake8 src
pyright --project src/pyproject.toml
```

---

## Tests

Run from `src/` so that pytest configuration and `pythonpath` resolve
correctly:

```bash
cd src && pytest
```

Run a single file or test case:

```bash
cd src && pytest tests/test_<name>.py
cd src && pytest tests/test_<name>.py::test_<case>
cd src && pytest -k <expression>
```

---

## Code style

- Line length: **80 columns** (`black`, `isort`, `flake8` all share this
  limit).
- Formatter: `black` with `target-version = py312`.
- Import order: `isort` with `profile = "black"`.
- Type checking: `pyright` in `strict` mode — all signatures must be fully
  typed.
- Use strict Sequence type aliases from the plugin API:
  `Sequence[PluginCommandSpec]`, etc.
- Only add comments when clarification is genuinely needed; avoid
  self-documenting noise.

---

## Git conventions

- **Sign every commit** with GPG/SSH: `git commit -S`
  (amend with `git commit --amend -S`).
- **Do not** include `Co-authored-by: Copilot ...` or `Co-Authored-By: Claude ...` trailers in commit messages.
- Use the repository / user `.gitconfig` identity for author metadata.

---

## Shepherd plugin architecture

### `plugin.yaml`

Declarative descriptor consumed by the Shepherd runtime.  Required fields:

| Field | Notes |
|---|---|
| `id` | Unique plugin identifier; used to namespace registry entries as `plugin-id/local-id`. |
| `name` | Human-readable display name. |
| `version` | Semver string; must match `src/version`. |
| `plugin_api_version` | Integer; must match the Shepherd API version. |
| `entrypoint.module` | Dotted Python module path of the plugin class. |
| `entrypoint.class` | Name of the `ShepherdPlugin` subclass. |
| `capabilities` | Real YAML booleans (`true`/`false`, unquoted).  Set to `true` only for contributions the plugin actually provides. |
| `default_config` | Plugin-specific config defaults (may be empty `{}`). |

Optional sections: `env_templates`, `service_templates`.

### `ShepherdPlugin` subclass (`src/postgres_plugin/main.py`)

Import from the `plugin` namespace (resolved via `shepherd/src`):

```python
from plugin import (
    PluginCommandSpec,
    PluginCompletionSpec,
    PluginEnvFactorySpec,
    PluginSvcFactorySpec,
    ShepherdPlugin,
)

# Commands live in commands.py; completion in completion.py.
# main.py imports and wires them together.
```

Override only the contribution methods relevant to `capabilities` in
`plugin.yaml`:

```python
class MyPlugin(ShepherdPlugin):
    def get_commands(self) -> Sequence[PluginCommandSpec]: ...
    def get_completion_providers(self) -> Sequence[PluginCompletionSpec]: ...
    def get_env_factories(self) -> Sequence[PluginEnvFactorySpec]: ...
    def get_service_factories(self) -> Sequence[PluginSvcFactorySpec]: ...
```

Return `()` for extension areas not used by the plugin.

### `PluginContext`

Shepherd injects a `PluginContext` at instantiation time:

```python
@dataclass
class PluginContext:
    config: PluginConfigView          # always populated
    environment: PluginEnvironmentView | None   # None during tab-completion
    service: PluginServiceView | None           # None during tab-completion
```

`environment` and `service` are `None` during Click command resolution
(tab completion).  By the time a command handler executes, both are set.

### Commands — `PluginCommandSpec`

Each command contribution names a `scope` and a `verb`.  The `command` value
must be a Click `Command` whose `.name` attribute matches `verb`:

```python
@click.command(name="up")
def up() -> None:
    """Start the service."""
    ...

PluginCommandSpec(scope="myservice", verb="up", command=up)
```

Shepherd exposes the command as `myservice up`.

### Completion — `PluginCompletionSpec`

Completion providers are callables `f(args: list[str]) -> list[str]`.
`args` is the full raw argument list from the shell.  Return matching
suggestions; Shepherd merges results from all providers registered for the
active scope:

```python
def complete_myservice(args: list[str]) -> list[str]:
    if len(args) >= 2 and args[0] == "myservice":
        if args[1] in {"logs", "shell"}:
            return ["primary", "secondary"]
    return []

PluginCompletionSpec(scope="myservice", provider=complete_myservice)
```

### Environment factories — `PluginEnvFactorySpec`

Pass the **class** of your `EnvironmentFactory` subclass.  Shepherd calls
it with `(configMng, svc_factory, cli_flags)`:

```python
PluginEnvFactorySpec(id="my-env-factory", provider=MyEnvironmentFactory)
```

### Service factories — `PluginSvcFactorySpec`

Pass the **class** of your `ServiceFactory` subclass.  Shepherd calls it
with `(configMng,)`:

```python
PluginSvcFactorySpec(id="my-svc-factory", provider=MyServiceFactory)
```

---

## Packaging

Build an installable archive (run from the repository root):

```bash
tar -czf shepherd-plugin-postgres.tar.gz plugin.yaml -C src postgres_plugin
```

The archive must contain `plugin.yaml` **at the root** and the plugin
module directly beneath.

Install into Shepherd:

```bash
shepctl plugin install shepherd-plugin-postgres.tar.gz
shepctl plugin enable postgres
```

Shepherd installs the package under `~/.shpd/plugins/postgres/` and
loads it via `importlib`.

---

## `plugin.yaml` capabilities vs. contribution methods

Keep `capabilities` flags in `plugin.yaml` in sync with what the plugin
actually returns.  If a getter returns a non-empty sequence, the
corresponding capability must be `true`.

| `plugin.yaml` key | Getter |
|---|---|
| `capabilities.commands` | `get_commands` |
| `capabilities.completion` | `get_completion_providers` |
| `capabilities.env_factories` | `get_env_factories` |
| `capabilities.svc_factories` | `get_service_factories` |
| `capabilities.templates` | `env_templates` / `service_templates` sections |

# Copyright (c) 2026 Moony Fringers
# SPDX-License-Identifier: AGPL-3.0-only
#
# This file is part of the Shepherd Postgres Plugin.
# Open-source: see LICENSE (AGPL-3.0-only).
# Commercial: see LICENSE-COMMERCIAL or contact licensing@moonyfringers.net.

from __future__ import annotations

from unittest.mock import MagicMock

from plugin import PluginCommandSpec, PluginCompletionSpec

from postgres_plugin.completion import PG_VERBS, complete_pg
from postgres_plugin.main import PostgresPlugin

_EXPECTED_SPECS: list[tuple[str, str]] = [
    ("pg", "up"),
    ("pg", "halt"),
    ("pg", "stdout"),
    ("pg", "shell"),
    ("pg", "sql-shell"),
    ("pg", "sync"),
    ("pg", "create"),
    ("pg", "drop"),
    ("pg", "import"),
    ("pg", "exec"),
    ("pg", "list"),
    ("pg", "snapshot"),
]


def _make_plugin() -> PostgresPlugin:
    ctx = MagicMock()
    return PostgresPlugin(ctx)


def test_get_commands_returns_expected_specs() -> None:
    specs = _make_plugin().get_commands()
    pairs = [(s.scope, s.verb) for s in specs]
    assert sorted(pairs) == sorted(_EXPECTED_SPECS)


def test_command_names_match_verbs() -> None:
    specs = _make_plugin().get_commands()
    for spec in specs:
        assert isinstance(spec, PluginCommandSpec)
        assert spec.command.name == spec.verb


def test_get_completion_providers_returns_pg_scope() -> None:
    providers = _make_plugin().get_completion_providers()
    assert len(providers) == 1
    spec = providers[0]
    assert isinstance(spec, PluginCompletionSpec)
    assert spec.scope == "pg"


def test_complete_pg_top_level() -> None:
    result = complete_pg(["pg"])
    assert sorted(result) == sorted(PG_VERBS)


def test_complete_pg_verb_prefix() -> None:
    result = complete_pg(["pg", "sn"])
    assert result == ["snapshot"]


def test_complete_pg_subcommand() -> None:
    result = complete_pg(["pg", "snapshot", ""])
    assert result == ["list", "take", "apply", "delete"]

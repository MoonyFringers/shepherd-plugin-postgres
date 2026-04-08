# Copyright (c) 2026 Moony Fringers
# SPDX-License-Identifier: AGPL-3.0-only
#
# This file is part of the Shepherd Postgres Plugin.
# Open-source: see LICENSE (AGPL-3.0-only).
# Commercial: see LICENSE-COMMERCIAL or contact licensing@moonyfringers.net.

from __future__ import annotations

PG_VERBS: list[str] = [
    "up",
    "halt",
    "stdout",
    "shell",
    "sql-shell",
    "sync",
    "create",
    "drop",
    "exec",
    "import",
    "list",
    "snapshot",
]

PG_SUBCOMMANDS: dict[str, list[str]] = {
    "create": ["user", "dir"],
    "drop": ["user"],
    "import": ["dump"],
    "exec": ["script"],
    "list": ["users"],
    "snapshot": ["list", "take", "apply", "delete"],
}


def complete_pg(args: list[str]) -> list[str]:
    if len(args) < 2:
        return PG_VERBS
    verb = args[1]
    if len(args) == 2:
        return [v for v in PG_VERBS if v.startswith(verb)]
    if len(args) == 3 and verb in PG_SUBCOMMANDS:
        partial = args[2]
        return [s for s in PG_SUBCOMMANDS[verb] if s.startswith(partial)]
    return []

# Copyright (c) 2026 Moony Fringers
# SPDX-License-Identifier: AGPL-3.0-only
#
# This file is part of the Shepherd Postgres Plugin.
# Open-source: see LICENSE (AGPL-3.0-only).
# Commercial: see LICENSE-COMMERCIAL or contact licensing@moonyfringers.net.

from __future__ import annotations

from typing import Sequence

from plugin import (
    PluginCommandSpec,
    PluginCompletionSpec,
    PluginContext,
    ShepherdPlugin,
)

from postgres_plugin.commands import (
    create,
    drop,
    exec_cmd,
    halt,
    import_cmd,
    list_cmd,
    shell,
    snapshot,
    sql_shell,
    stdout,
    sync,
    up,
)
from postgres_plugin.completion import complete_pg


class PostgresPlugin(ShepherdPlugin):
    def __init__(self, context: PluginContext) -> None:
        super().__init__(context)

    def get_commands(self) -> Sequence[PluginCommandSpec]:
        return [
            PluginCommandSpec(scope="pg", verb="up", command=up),
            PluginCommandSpec(scope="pg", verb="halt", command=halt),
            PluginCommandSpec(scope="pg", verb="stdout", command=stdout),
            PluginCommandSpec(scope="pg", verb="shell", command=shell),
            PluginCommandSpec(scope="pg", verb="sql-shell", command=sql_shell),
            PluginCommandSpec(scope="pg", verb="sync", command=sync),
            PluginCommandSpec(scope="pg", verb="create", command=create),
            PluginCommandSpec(scope="pg", verb="drop", command=drop),
            PluginCommandSpec(scope="pg", verb="import", command=import_cmd),
            PluginCommandSpec(scope="pg", verb="exec", command=exec_cmd),
            PluginCommandSpec(scope="pg", verb="list", command=list_cmd),
            PluginCommandSpec(scope="pg", verb="snapshot", command=snapshot),
        ]

    def get_completion_providers(self) -> Sequence[PluginCompletionSpec]:
        return [
            PluginCompletionSpec(scope="pg", provider=complete_pg),
        ]

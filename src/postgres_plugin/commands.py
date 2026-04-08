# Copyright (c) 2026 Moony Fringers
# SPDX-License-Identifier: AGPL-3.0-only
#
# This file is part of the Shepherd Postgres Plugin.
# Open-source: see LICENSE (AGPL-3.0-only).
# Commercial: see LICENSE-COMMERCIAL or contact licensing@moonyfringers.net.

from __future__ import annotations

import click

# ------------------------------------------------------------------
# Flat commands
# ------------------------------------------------------------------


@click.command(name="up")
def up() -> None:
    """Start database service."""
    pass


@click.command(name="halt")
def halt() -> None:
    """Halt database service."""
    pass


@click.command(name="stdout")
def stdout() -> None:
    """Show database service stdout."""
    pass


@click.command(name="shell")
def shell() -> None:
    """Get a shell session for the database service."""
    pass


@click.command(name="sql-shell")
def sql_shell() -> None:
    """Get a SQL session for the database service."""
    pass


@click.command(name="sync")
@click.argument("upstream", required=False)
def sync(upstream: str | None) -> None:
    """Sync the local service's status with an upstream database."""
    pass


# ------------------------------------------------------------------
# create group
# ------------------------------------------------------------------


@click.group(name="create")
def create() -> None:
    """Create database objects."""


@create.command(name="user")
@click.argument("user")
@click.argument("psw")
def create_user(user: str, psw: str) -> None:
    """Create a new user in the database."""
    pass


@create.command(name="dir")
@click.argument("user")
@click.argument("directory_name")
def create_dir(user: str, directory_name: str) -> None:
    """Create a new directory object in the database."""
    pass


# ------------------------------------------------------------------
# drop group
# ------------------------------------------------------------------


@click.group(name="drop")
def drop() -> None:
    """Drop database objects."""


@drop.command(name="user")
@click.argument("user")
def drop_user(user: str) -> None:
    """Drop an existing user from the database."""
    pass


# ------------------------------------------------------------------
# import group
# ------------------------------------------------------------------


@click.group(name="import")
def import_cmd() -> None:
    """Import data into the database."""


@import_cmd.command(name="dump")
@click.argument("dump_file")
def import_dump(dump_file: str) -> None:
    """Import a dump file into the database."""
    pass


# ------------------------------------------------------------------
# exec group
# ------------------------------------------------------------------


@click.group(name="exec")
def exec_cmd() -> None:
    """Execute scripts against the database."""


@exec_cmd.command(name="script")
@click.argument("sql_file")
@click.argument("user", required=False)
@click.argument("pwd", required=False)
def exec_script(sql_file: str, user: str | None, pwd: str | None) -> None:
    """Execute a SQL script as sys or a given user."""
    pass


# ------------------------------------------------------------------
# list group
# ------------------------------------------------------------------


@click.group(name="list")
def list_cmd() -> None:
    """List database objects."""


@list_cmd.command(name="users")
def list_users() -> None:
    """List all database users."""
    pass


# ------------------------------------------------------------------
# snapshot group
# ------------------------------------------------------------------


@click.group(name="snapshot")
def snapshot() -> None:
    """Manage database snapshots."""


@snapshot.command(name="list")
def snapshot_list() -> None:
    """Show all available snapshots."""
    pass


@snapshot.command(name="take")
@click.argument("snapshot_name", required=False)
def snapshot_take(snapshot_name: str | None) -> None:
    """Take a snapshot (timestamp by default)."""
    pass


@snapshot.command(name="apply")
@click.argument("snapshot_name")
def snapshot_apply(snapshot_name: str) -> None:
    """Restore a previously taken snapshot."""
    pass


@snapshot.command(name="delete")
@click.argument("snapshot_name")
def snapshot_delete(snapshot_name: str) -> None:
    """Delete a previously taken snapshot."""
    pass

from pathlib import Path
from typing import List, Optional

import typer

from empuje import ERRORS, __app_name__, __version__, config, database, empuje

app = typer.Typer()


@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt="empuje database location",
    ),
) -> None:
    """Initialize the application configuration."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The empuje database is {db_path}", fg=typer.colors.GREEN)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


def get_empuje() -> empuje.Empujer:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Kindly, run "empuje init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    if db_path.exists():
        return empuje.Empujer(db_path)
    else:
        typer.secho(
            'Database not found. Kindly, run "empuje init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)


@app.command()
def add(
    description: List[str] = typer.Argument(...),
    priority: int = typer.Option(2, "--priority", "-p", min=1, max=3),
) -> None:
    """Add a new empuje with a DESCRIPTION."""
    empujer = get_empuje()
    empuje, error = empujer.add(description, priority)
    if error:
        typer.secho(f'Adding empuje failed with "{ERRORS[error]}"', fg=typer.colors.RED)
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""empuje: "{empuje['Description']}" was added """
            f"""with priority: {priority}""",
            fg=typer.colors.GREEN,
        )


@app.command(name="list")
def list_all() -> None:
    """List all empujes"""
    empujer = get_empuje()
    empuje_list = empujer.get_all_empuje()
    if len(empuje_list) == 0:
        typer.secho("There  are no empujes", fg=typer.colors.RED)
        raise typer.Exit()
    typer.secho("\nempuje list:", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Priority  ",
        "| Done  ",
        "| Description  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id in enumerate(empuje_list, 1):
        desc, priority, done = empuje.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| ({priority}){(len(columns[1]) - len(str(priority)) - 4) * ' '}"
            f"| {done}{(len(columns[2]) - len(str(done)) - 2) * ' '}"
            f"| {desc}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


@app.command(name="complete")
def set_done(empuje_id: int = typer.Argument(...)) -> None:
    """Complete empuje by setting is as done using empuje_id"""
    empujer = get_empuje()
    empuje, error = empujer.set_done(empuje_id)
    if error:
        typer.secho(
            f'Completing empuje # "{empuje_id}" failed with "{ERRORS[error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""empuje # {empuje_id}" {empuje['Description']}" completed! """,
            fg=typer.colors.GREEN,
        )


@app.command()
def remove(
    empuje_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove a empuje using its empuje_id"""
    empujer = get_empuje()

    def _remove():
        empuje, error = empujer.remove(empuje_id)
        if error:
            typer.secho(
                f'Removing empuje # {empuje} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""empuje # {empuje}: '{empuje["Description"]}' was removed""",
                fg=typer.colors.GREEN,
            )

    if force:
        _remove()
    else:
        empuje_list = empujer.get_all_empuje()
        try:
            empuje = empuje_list[empuje_id - 1]
        except IndexError:
            typer.secho("Invalid Empuje_id", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(f"Delete empuje # {empuje_id}: {empuje['Description']}?")
        if delete:
            _remove()
        else:
            typer.echo("Operation canceled")


@app.command(name="clear")
def remove_all(
    force: bool = typer.Option(
        ...,
        prompt="Delete all empujes?",
        help="Force deletion without confirmation.",
    ),
) -> None:
    """Remove all empujes."""
    empujer = get_empuje()
    if force:
        error = empujer.remove_all().error
        if error:
            typer.secho(
                f'Removing empujes failed with "{ERRORS[error]}"',
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
        else:
            typer.secho("All empujes were removed", fg=typer.colors.GREEN)
    else:
        typer.echo("Operation canceled")

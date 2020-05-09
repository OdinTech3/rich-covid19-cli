import typer
from rich_covid19_cli import console, cli, api, cli_ui
from rich.panel import Panel


@cli.command()
def run():
    console.print(Panel("Hello, [red]World!"))


@cli.command()
def summary(country: str = typer.Argument(None)):
    """
    A summary of new and total cases per country updated daily.

    To see summary for a country specify by providing a COUNTRY argument
    """
    if country is None:
        g_summary = api.get_global_summary()

        table = cli_ui.gen_summary(g_summary)

        console.print(table)


if __name__ == "__main__":
    cli()

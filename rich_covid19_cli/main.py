import typer
import json
from rich_covid19_cli import console, cli, api, cli_ui, config
from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, TypedDict


class Country(TypedDict):
    Country: str
    Slug: str
    ISO2: str


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

        for table in cli_ui.gen_summary(g_summary):
            console.print(table)


@cli.command()
def getcode(country: str):
    """
    Get the code of a given [COUNTRY]
    """

    with open(config.DATA_DIR / "country.json") as f:
        countries: List[Country] = json.loads(f.read())

        target_country = [
            c for c in countries if c["Country"].lower() == country.lower()
        ]

        if target_country:
            pretty_json = json.dumps(target_country[0], indent=4)
            console.print(Panel(pretty_json))
        else:
            console.print(f"Unable to get country code for [code]{country}[/code]")
            typer.Exit(code=1)


if __name__ == "__main__":
    cli()

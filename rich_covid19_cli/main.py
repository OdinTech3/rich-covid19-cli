import typer
import json
from rich_covid19_cli import console, cli, api, cli_ui, config
from rich_covid19_cli.models import CountryDict
from rich import box
from rich.panel import Panel
from rich.markdown import Markdown
from typing import List, Optional


def find_byname(name: str, countries: List[CountryDict]) -> Optional[CountryDict]:
    target_country = [c for c in countries if c["Country"].lower() == name.lower()]

    return target_country[0] if target_country else None


def find_bycode(code: str, countries: List[CountryDict]) -> Optional[CountryDict]:
    target_country = [c for c in countries if c["ISO2"].lower() == code.lower()]

    return target_country[0] if target_country else None


@cli.command()
def run():
    console.print(Panel("Hello, [red]World!"))


@cli.command()
def summary(country: str):
    """
    A summary of new and total cases per country updated daily.

    To see summary for a country specify by providing a COUNTRY argument
    """
    if country is None:
        g_summary = api.get_global_summary()

        for table in cli_ui.gen_summary(g_summary):
            console.print(table)

    else:
        c_summary = api.get_country_summary(country)

        for table in cli_ui.gen_summary(c_summary):
            console.print(table)


@cli.command()
def getcountry(
    country: str = typer.Option("", help="country name"),
    code: str = typer.Option("", help="ISO2 country code"),
):
    """
    Get details like slug and ISO2 country code of a given [COUNTRY]

    If --code is present then you can get country details
    by providing the ISO2 country code
    """

    with open(config.DATA_DIR / "country.json") as f:
        countries: List[CountryDict] = json.loads(f.read())

        target_country = (
            find_byname(country, countries) if country else find_bycode(code, countries)
        )

        if target_country:
            pretty_json = json.dumps(target_country, indent=4)
            console.print(Panel(pretty_json))
        else:
            console.print(f"Unable to get country code for [code]{country}[/code]")
            typer.Exit(code=1)


@cli.command()
def dayone(
    country: str = typer.Option("", help="country name"),
    code: str = typer.Option("", help="ISO2 country code"),
):
    with open(config.DATA_DIR / "country.json") as f:
        countries: List[CountryDict] = json.loads(f.read())

    target_country = (
        find_byname(country, countries) if country else find_bycode(code, countries)
    )

    if target_country:
        country_slug = target_country["Slug"]
        country_stats = api.get_dayone_stats(country_slug)

        cli_ui.gen_summary(country_stats)
    else:
        console.print(f"Unable to get country code for [code]{country}[/code]")
        typer.Exit(code=1)


if __name__ == "__main__":
    cli()

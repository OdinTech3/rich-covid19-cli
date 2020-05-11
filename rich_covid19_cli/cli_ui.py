import humanize as hstr
from rich.table import Table
from rich_covid19_cli.models import GlobalSummary, CountrySummary
from functools import singledispatch
from rich.style import Style
from typing import Generator, Optional

UIGenerator = Generator[Table, None, None]
danger_style = Style(color="white", bgcolor="black")


def intword(x: int) -> str:
    og_x = str(x)
    humanized_x = hstr.intword(x)

    return hstr.intcomma(x) if og_x == humanized_x else humanized_x


@singledispatch
def gen_summary(data, title: Optional[str] = None) -> Table:
    raise NotImplementedError("Unsupported type for argument data")


@gen_summary.register(GlobalSummary)
def _global(data: GlobalSummary, title: Optional[str] = None) -> UIGenerator:
    title_ = title if title is not None else "\nGlobal Covid-19 Summary"
    totalstats_table = Table(title=title_)

    totalstats_table.add_column("Total Confirmed Deaths", style=danger_style)
    totalstats_table.add_column("Total Confirmed Cases", style=danger_style)
    totalstats_table.add_column("Total Recovered Cases", style=danger_style)

    totalstats_table.add_row(
        intword(data.total_deaths),
        intword(data.total_confirmed),
        intword(data.total_recovered),
    )

    yield totalstats_table

    newstats_table = Table()

    newstats_table.add_column("Total New Confirmed Deaths", style=danger_style)
    newstats_table.add_column("Total New Confirmed Cases", style=danger_style)
    newstats_table.add_column("Total New Recovered Cases", style=danger_style)

    newstats_table.add_row(
        intword(data.new_deaths),
        intword(data.new_confirmed),
        intword(data.total_recovered),
    )

    yield newstats_table


@gen_summary.register(CountrySummary)
def _country(data: CountrySummary, title: Optional[str] = None) -> UIGenerator:
    title = title if title is not None else f"{data.country}'s Covid-19 Summary"
    totalstats_table = Table(title=title)

    totalstats_table.add_column("Total Confirmed Deaths", style=danger_style)
    totalstats_table.add_column("Total Confirmed Cases", style=danger_style)
    totalstats_table.add_column("Total Recovered Cases", style=danger_style)

    totalstats_table.add_row(
        intword(data.total_deaths),
        intword(data.total_confirmed),
        intword(data.total_recovered),
    )

    yield totalstats_table

    newstats_table = Table()

    newstats_table.add_column("Total New Confirmed Deaths", style=danger_style)
    newstats_table.add_column("Total New Confirmed Cases", style=danger_style)
    newstats_table.add_column("Total New Recovered Cases", style=danger_style)

    newstats_table.add_row(
        intword(data.new_deaths),
        intword(data.new_confirmed),
        intword(data.total_recovered),
    )

    yield newstats_table

    yield f"[italic]Updated {data.date.ctime()}[/]"

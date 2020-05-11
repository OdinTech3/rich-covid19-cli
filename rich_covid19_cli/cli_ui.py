import humanize as hstr
from rich.table import Table
from rich_covid19_cli import models
from functools import singledispatch
from rich.style import Style
from typing import Generator

UIGenerator = Generator[Table, None, None]

danger_style = Style(color="white", bgcolor="black")


@singledispatch
def gen_summary(data, title: str = None) -> Table:
    raise NotImplementedError("Unsupported type for argument data")


@gen_summary.register(models.GlobalSummary)
def _(
    data: models.GlobalSummary, title: str = "\nGlobal Covid-19 Summary"
) -> UIGenerator:
    totalstats_table = Table(title=title)

    totalstats_table.add_column("Total Confirmed Deaths", style=danger_style)
    totalstats_table.add_column("Total Confirmed Cases", style=danger_style)
    totalstats_table.add_column("Total Recovered Cases", style=danger_style)

    totalstats_table.add_row(
        hstr.intword(data.total_deaths),
        hstr.intword(data.total_confirmed),
        hstr.intword(data.total_recovered),
    )

    yield totalstats_table

    newstats_table = Table()

    newstats_table.add_column("Total New Confirmed Deaths", style=danger_style)
    newstats_table.add_column("Total New Confirmed Cases", style=danger_style)
    newstats_table.add_column("Total New Recovered Cases", style=danger_style)

    newstats_table.add_row(
        hstr.intword(data.new_deaths),
        hstr.intword(data.new_confirmed),
        hstr.intword(data.total_recovered),
    )

    yield newstats_table

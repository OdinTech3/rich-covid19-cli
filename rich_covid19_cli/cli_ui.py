import humanize as hstr
from rich.table import Table
from rich_covid19_cli import models
from functools import singledispatch
from rich.style import Style

danger_style = Style(color="white", bgcolor="black")


@singledispatch
def gen_summary(data, title: str = None) -> Table:
    raise NotImplementedError("Unsupported type for argument data")


@gen_summary.register(models.GlobalSummary)
def _(data: models.GlobalSummary, title: str = "\nGlobal Covid-19 Summary") -> Table:
    table = Table(title=title)

    table.add_column("Total Confirmed Deaths", style=danger_style)
    table.add_column("Total Number of New Cases", style=danger_style)
    table.add_column("Total Number of Recovered Cases", style=danger_style)

    table.add_row(
        hstr.intword(data.total_confirmed),
        hstr.intword(data.new_confirmed),
        hstr.intword(data.total_recovered),
    )

    return table

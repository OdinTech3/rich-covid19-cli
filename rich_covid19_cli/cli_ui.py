import time
import humanize as hstr
from rich.table import Table
from rich_covid19_cli.models import GlobalSummary, CountrySummary, DayOneStats
from functools import singledispatch
from rich.style import Style
from rich.progress import Progress, BarColumn, ProgressColumn, Task
from typing import Generator, Optional, Iterator, List
from rich.text import Text
from datetime import datetime, date

UIGenerator = Generator[Table, None, None]
danger_style = Style(color="white", bgcolor="black")


class DayOneStatDateColumn(ProgressColumn):
    """Renders Day one stat"""

    # Only refresh twice a second to prevent jitter
    max_refresh = 0.5
    last_date = date.today().strftime("%b %d %Y %H:%M:%S")

    def render(self, task: Task) -> Text:
        """Show stat dates """

        if "stat_dates" not in task.fields:
            return Text("•", style="progress.remaining")

        try:
            stat_date: datetime = next(task.fields["stat_dates"])
            fmt_stat_date = stat_date.strftime("%b %d %Y")
            self.last_date = fmt_stat_date

            return Text(fmt_stat_date, style="progress.remaining")
        except StopIteration:
            return Text(self.last_date, style="progress.remaining")


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


@gen_summary.register(list)
def _dayone(data: List[DayOneStats]):
    stats_sorted: List[DayOneStats] = sorted(data, key=lambda d: d.Date)
    latest_stats: DayOneStats = max(data, key=lambda d: d.Date)

    def get_deltas(stat: str) -> Iterator[int]:
        deltas = [
            getattr(j, stat) - getattr(i, stat)
            for i, j in zip(stats_sorted[:-1], stats_sorted[1:])
        ]

        return iter(deltas)

    def get_dates() -> Iterator[datetime]:
        dates = [s.Date for s in stats_sorted]

        return iter(dates)

    prog_tmpl = (
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.completed ]{task.completed}",
        DayOneStatDateColumn(),
    )

    stat_dates = get_dates()

    all_deltas = zip(
        get_deltas("confirmed"),
        get_deltas("deaths"),
        get_deltas("recovered"),
        get_deltas("active"),
    )

    with Progress(*prog_tmpl) as progress:
        date_task = progress.add_task(
            "Date", total=len(stats_sorted) + 1, stat_dates=stat_dates
        )

        confirmed_task = progress.add_task(
            "[blue on white]Confirmed Cases...", total=latest_stats.confirmed,
        )
        death_task = progress.add_task("[red]Deaths...", total=latest_stats.deaths)
        recovered_task = progress.add_task(
            "[green]Recovered.Cases..", total=latest_stats.recovered
        )
        active_task = progress.add_task(
            "[yellow]Active Cases...", total=latest_stats.active
        )

        for confirmed_delta, death_delta, recovered_delta, active_delta in all_deltas:
            progress.update(date_task, advance=1, visible=False)

            progress.update(confirmed_task, advance=confirmed_delta)
            progress.update(death_task, advance=death_delta)
            progress.update(recovered_task, advance=recovered_delta)
            progress.update(active_task, advance=active_delta)

            time.sleep(0.2)

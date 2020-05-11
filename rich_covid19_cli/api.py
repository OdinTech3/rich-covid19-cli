import requests
from rich_covid19_cli.models import GlobalSummary, CountrySummary, DayOneStats
from typing import Dict, List


def url(endpoint: str) -> str:
    return f"https://api.covid19api.com/{endpoint}"


def get_global_summary() -> GlobalSummary:
    resp = requests.get(url("summary"))
    payload: Dict = resp.json()

    return GlobalSummary.from_dict(payload.get("Global", {}))


def get_country_summary(country: str) -> CountrySummary:
    resp = requests.get(url("summary"))
    payload: Dict = resp.json()
    countries: List[Dict] = payload.get("Countries", {})

    target_country = [c for c in countries if c["Country"].lower() == country.lower()]

    return CountrySummary.from_dict(target_country[0])


def get_dayone_stats(slug: str) -> List[DayOneStats]:
    resp = requests.get(url(f"/dayone/country/{slug}"))
    payload: str = resp.text
    stats: List[DayOneStats] = DayOneStats.schema().loads(payload, many=True)

    return stats

import requests
from rich_covid19_cli.models import GlobalSummary
from typing import Dict


def url(endpoint: str) -> str:
    return f"https://api.covid19api.com/{endpoint}"


def get_global_summary() -> GlobalSummary:
    resp = requests.get(url("summary"))
    payload: Dict = resp.json()
    return GlobalSummary.from_dict(payload.get("Global", {}))

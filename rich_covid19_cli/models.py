from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, config
from typing import Dict, TypeVar, Union
from datetime import datetime
from marshmallow import fields

# Create a generic variable that can be 'IDataClass', or any subclass.F
D = TypeVar("D", bound="IDataClass")
SummaryModel = Union["GlobalSummary", "CountrySummary"]


def fromisoformat(datestr: str) -> datetime:
    new_datestr = datestr.replace('Z', '+00:00')

    return datetime.fromisoformat(new_datestr)

class IDataClass:
    @staticmethod
    def from_dict(d: Dict) -> D:
        pass

    def to_dict(self) -> Dict:
        pass


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class GlobalSummary(IDataClass):
    new_confirmed: int
    total_confirmed: int
    new_deaths: int
    total_deaths: int
    new_recovered: int
    total_recovered: int


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class CountrySummary(IDataClass):
    country: str
    country_code: str
    slug: str
    new_confirmed: int
    total_confirmed: int
    new_deaths: int
    total_deaths: int
    new_recovered: int
    total_recovered: int
    date: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )

from dataclasses import dataclass, field
from enum import Enum
from province import Province
from building import Building
from unit import Unit

class Season(Enum):
    SPRING = 0 # new year
    SUMMER = 1 # new game
    AUTUMN = 2 # profit arrives on this turn end
    WINTER = 3 # brace yourselves

@dataclass
class Japan:
    provinces: list["Province"]
    buildings: list["Building"]
    units: list["Unit"]
    current_season: "Season" = Season.SUMMER
    current_year: int = 1530
    provinces: list["Province"] = field(default_factory=list)
    current_money: int = 1000
    debts_by_season: list[int] = field(default_factory=list)
from dataclasses import dataclass, field
from enum import Enum
from building import Building
from unit import Unit, Category, Weapon

class Minerium(Enum):
    NOTHING = 0
    COPPER = 1
    SILVER = 2
    GOLD = 3

@dataclass
class Province:
    id: str
    name: str
    farm_income: int

    water: bool = False
    minerium: "Minerium" = 0
    bonus: str | "Category" | "Weapon" | None = None
    owned: bool = False

    buildings: list["Building"] = field(default_factory=list)
    units_trainable: list["Unit"] = field(default_factory=list)

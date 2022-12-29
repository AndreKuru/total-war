from dataclasses import dataclass, field
from enum import Enum
from building import Building
from unit import Unit, Category, Weapon

class Minerium(Enum):
    NOTHING = 0
    COPPER = 1
    SILVER = 2
    GOLD = 3

def get_province(provinces: list["Province"], id: str):
    for province in provinces:
        if province.id == id:
            return province

def get_provinces(provinces: list["Province"], ids: list[str]):
    selected_provinces = list()

    for province in provinces:
        for id in ids:
            if province.id == id:
                selected_provinces.append(province)
                ids.remove(id)
                pass

    return selected_provinces


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

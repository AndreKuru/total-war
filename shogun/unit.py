from dataclasses import dataclass
from enum import Enum

class Category(Enum):
    INFANTARY = 0
    CALVALRY = 1

class Class(Enum):
    MELEE = 0
    MISSILE = 1

class Weapon(Enum):
    SPEAR = 0
    BOW_AND_ARROW = 1
    POLEARM = 2
    SWORD = 3
    FIREARM = 4
    SWORD_AND_NINJA_STARS = 5
    JAVELIN_SWORD_AND_SHIELD = 6

def get_units(units: list["Unit"], ids: list[str]):
    selected_units = list()
    breaked = False

    for id in ids:
        for unit in units:
            if unit.id == id:
                if unit in selected_units:
                    print(unit.name  + "duplicate ignored.")
                else:
                    selected_units.append(unit)
                breaked = True
                break
        if not breaked:
            raise Exception("Unit " + id + " not found.")
        breaked = False

    return selected_units


@dataclass
class Unit:
    id: str
    name: str
    category: "Category"
    class_unit: "Class"
    weapon: "Weapon"
    soldiers: int
    cost: int
    seasons_to_train: int
    morale_boost: int = 0
    attack_boost: int = 0
    armor_boost: int = 0
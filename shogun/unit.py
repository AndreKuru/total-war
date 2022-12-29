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

def get_unit(units: list["Unit"], id: str):
    for unit in units:
        if unit.id == id:
            return unit

def get_units(units: list["Unit"], ids: list[str]):
    selected_units = list()

    for unit in units:
        for id in ids:
            if unit.id == id:
                selected_units.append(unit)
                ids.remove(id)
                pass

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
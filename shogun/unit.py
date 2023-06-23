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

@dataclass
class Agent:
    id: str
    name: str
    cost: int
    seasons_to_train: int
    morale_boost: int | None = 0

def list_units(units: list[Unit]):
    for unit in units:
        spaces = ""
        for _ in range(4 - len(unit.id)):
            spaces += " "
        morale = ""
        for _ in range(unit.morale_boost):
            morale += "+"
        print(unit.id + spaces + "- " + unit.name + morale + " $" + str(unit.cost) + " #" + str(unit.seasons_to_train))

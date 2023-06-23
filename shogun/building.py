from dataclasses import dataclass, field
from enum import Enum
from typing import Self
from unit import Unit

class Condition(Enum):
    WATER = 1
    IRON_SAND_DEPOSITS = 2
    NATURAL_MINERAL_DEPOSITS = 3
    LEGENDARY_SWORDMAN_EVENT = 4
    CHRISTIANITY = 5
    SIX_CHURCHES = 6
    DUTCH_ACCEPTANCE = 7
    BUDDHISM = 8

class Boost(Enum):
    ATTACK = 1
    ARMOR = 2
    RALLY = 3

@dataclass
class Building:
    id: str
    name: str
    cost: int
    seasons_to_build: int
    requires: list[Condition | Self | list[Self] | None] = field(default_factory=lambda: [None])  # lambda? # TODO: redo the read_building
    produces: list[tuple[str, Self | None]] = field(default_factory=list)                                 # Talvez não precise de Condition # TODO: redo the read_building
    upgrades: Self | None = None                                                                          # TODO: redo the read_building
    boost: Boost | None = None # Preciso explicitar o None?

def list_buildings(buildings: list[Building]):
    for building in buildings:
        spaces = ""
        for _ in range(4 - len(building.id)):
            spaces += " "
        print(building.id + spaces + "- " + building.name + " $" + str(building.cost) + " #" + str(building.seasons_to_build) + " | requires: " + building.requires)

def remove_buildings_upgraded(buildings: list[Building], building: Building):
    if building.upgrades:
        remove_buildings_upgraded(buildings, building.upgrades)
        buildings.remove(building.upgrades)


def remove_all_buildings_upgraded(buildings: list[Building]):
    for building in buildings:
        remove_buildings_upgraded(buildings, building)
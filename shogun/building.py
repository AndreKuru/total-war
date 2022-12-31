from dataclasses import dataclass, field
from enum import Enum
from unit import Unit

class Condition(Enum):
    NOTHING = 0
    WATER = 1
    IRON_SAND_DEPOSITS = 2
    NATURAL_MINERAL_DEPOSITS = 3
    LEGENDARY_SWORDMAN_EVENT = 4
    CHRISTIANITY = 5
    SIX_CHURCHES = 6
    DUTCH_ACCEPTANCE = 7
    BUDDHISM = 8

def list_buildings(buildings: list["Building"]):
    for building in buildings:
        spaces = ""
        for _ in 4 - len(building.id):
            spaces += " "
        print(building.id + spaces + "- " + building.name + " $" + building.cost + " #" + building.seasons_to_build + " | requires: " + building.requires)

def remove_buildings_upgraded(buildings: list["Building"], building: "Building"):
    if building.upgrades:
        remove_buildings_upgraded(buildings, building.upgrades)
        buildings.remove(building.upgrades)


def remove_all_buildings_upgraded(buildings: list["Building"]):
    for building in buildings:
        remove_buildings_upgraded(buildings, building)

@dataclass
class Building:
    id: str
    name: str
    cost: int
    seasons_to_build: int
    requires: list["Condition" | "Building" | list["Building"] ] = field(default_factory=lambda: [Condition.NOTHING]) # lambda? # TODO: redo the read_building
    produces: list[tuple["Unit", "Building" | "Condition"]] = field(default_factory=list)         # Talvez não precise de Condition # TODO: redo the read_building
    upgrades: "Building" = None                                                                   # TODO: redo the read_building
from dataclasses import dataclass
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

def remove_upgrades(buildings: list["Building"], building: "Building"):
    if building.upgrades:
        remove_upgrades(buildings, building.upgrades)
        buildings.remove(building.upgrades)


def get_only_upgraded_buildings(buildings: list["Building"]):
    selected_buildings = buildings.copy()

    for building in selected_buildings:
        remove_upgrades(selected_buildings, building)

    return selected_buildings

@dataclass
class Building:
    id: str
    name: str
    cost: int
    requires: list["Building" | "Condition"]            # TODO: redo the read_building
    produces: tuple["Unit", "Building" | "Condition"]   # TODO: redo the read_building
    upgrades: "Building"                                # TODO: redo the read_building
    seasons_to_build: int
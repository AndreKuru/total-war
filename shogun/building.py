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



def get_buildings(buildings: list["Building"], ids: list[str]):
    selected_buildings = list()
    breaked = False

    for id in ids:
        for building in buildings:
            if building.id == id:
                if building in selected_buildings:
                    print(building.name  + "duplicate ignored.")
                else:
                    selected_buildings.append(building)
                breaked = True
                break
        if not breaked:
            raise Exception("Building " + id + " not found.")
        breaked = False

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
from dataclasses import dataclass

def get_buildings(buildings: list["Building"], ids: list[str]):
    selected_buildings = list()

    for building in buildings:
        for id in ids:
            if building.id == id:
                selected_buildings.append(building)
                ids.remove(id)
                pass

    return selected_buildings


@dataclass
class Building:
    id: str
    name: str
    cost: int
    requires: str
    produces: str
    upgrades: str
    seasons_to_build: int
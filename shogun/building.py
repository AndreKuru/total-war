from dataclasses import dataclass

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
    requires: str
    produces: str
    upgrades: str
    seasons_to_build: int
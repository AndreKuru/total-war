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
    
    raise Exception("Invalid province.")

def get_provinces(provinces: list["Province"], ids: list[str]):
    selected_provinces = list()
    breaked = False

    for id in ids:
        for province in provinces:
            if province.id == id:
                if province in selected_provinces:
                    print(province.name  + "duplicate ignored.")
                else:
                    selected_provinces.append(province)
                breaked = True
                break
        if not breaked:
            raise Exception("Province " + id + " not found.")
        breaked = False

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

    def insert_upgradeds(self, building: "Building"):
        if building.upgrades:
            self.insert_upgradeds(building.upgrades)
        else:
            if building not in self.buildings:
                self.buildings.append(building)

    def insert(self, buildings: list["Building"]):
        for building in buildings:
            if building in self.buildings:
                raise Exception(building.name + " already exists")
            else:
                self.insert_upgradeds(building)
                self.buildings.append(building)

    def remove_upgradeds(self, building_to_remove: "Building"):
        for building in self.buildings:
            if building.upgrades == building_to_remove.id:
                self.remove_upgradeds(building)
                self.buildings.remove(building)
                break

    def remove(self, buildings: list["Building"]):
        for building in buildings:
            if building not in self.buildings:
                raise Exception(building.name + " not exists")
            else:
                self.remove_upgradeds(building)
                self.buildings.remove(building)
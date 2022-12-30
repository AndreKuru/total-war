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

    buildings_queue: list["Building"] = field(default_factory=list)
    units_queue: list["Unit"] = field(default_factory=list)

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

    def end_season_from_building_queue(self):
        seasons = 0
        for building in self.buildings_queue:
            seasons += building.seasons_to_build
        return seasons

    def purchase_building(self, building: "Building"):
        if building in self.buildings:
            raise Exception(building.name + " already exists.")
        elif building in self.buildings_queue:
            raise Exception(building.name + " already in queue.")
        else:
            debt = (self.end_season_from_building_queue(), building.cost)
            self.buildings_queue.append(building)
            return debt

    def purchase_unit(self, unit: "Unit"):
        pass
from dataclasses import dataclass, field
from enum import Enum
from building import Building, Condition
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

def list_my_provinces(provinces: list["Province"]):
    my_provinces = list()
    for province in provinces:
        if province.owned:
            my_provinces.append(province)
    
    for province in my_provinces:
        spaces = ""
        for _ in 4 - len(province.id):
            spaces += " "
        print(province.id + spaces + "- " + province.name)

def get_purchasable_and_owned_buildings(all_buildings: list["Building"], my_buildings: list["Building"], 
water: bool, iron_sand_deposits: bool, minerium: "Minerium",
legendary_swordman_event: bool, christianity: bool, churches: int, dutch_acceptance: bool):
    
    purchasable_and_owned_buildings = list()
    for building in all_buildings:
        purchasable = True
        for required in building.requires:
            if isinstance(required, Building):
                if required not in my_buildings:
                    purchasable = False
                    break
            else:
                match required:
                    case Condition.NOTHING:
                        pass

                    case Condition.WATER:
                        if not water:
                            purchasable = False
                            break

                    case Condition.IRON_SAND_DEPOSITS:
                        if not iron_sand_deposits:
                            purchasable = False
                            break

                    case Condition.NATURAL_MINERAL_DEPOSITS:
                        if not minerium.value():
                            purchasable = False
                            break

                    case Condition.LEGENDARY_SWORDMAN_EVENT:
                        if not legendary_swordman_event:
                            purchasable = False
                            break

                    case Condition.CHRISTIANITY:
                        if not christianity:
                            purchasable = False
                            break

                    case Condition.SIX_CHURCHES:
                        if churches < 6:
                            purchasable = False
                            break

                    case Condition.DUTCH_ACCEPTANCE:
                        if not dutch_acceptance:
                            purchasable = False
                            break

                    case Condition.BUDDHISM:
                        if christianity:
                            purchasable = False
                            break

        # end for required    
        if purchasable:
            purchasable_and_owned_buildings.append(building)

    # end for building

    return purchasable_and_owned_buildings

def get_purchasable_buildings(all_buildings: list["Building"], my_buildings: list["Building"], 
water: bool, iron_sand_deposits: bool, minerium: "Minerium",
legendary_swordman_event: bool, christianity: bool, churches: int, dutch_acceptance: bool):

    buildings = get_purchasable_and_owned_buildings(all_buildings, my_buildings, water, iron_sand_deposits, minerium, legendary_swordman_event, christianity, churches, dutch_acceptance)
    
    for building in my_buildings:
        buildings.remove(building)

    return buildings


@dataclass
class Province:
    id: str
    name: str
    farm_income: int

    water: bool = False
    sand: bool = False
    minerium: "Minerium" = 0
    bonus: str | "Category" | "Weapon" | None = None
    owned: bool = False

    buildings: list["Building"] = field(default_factory=list)
    units_trainable: list["Unit"] = field(default_factory=list)

    buildings_queue: list["Building"] = field(default_factory=list)
    units_queue: list["Unit"] = field(default_factory=list)

    def get_buildings_with_queue(self):
        buildings = self.buildings.copy()
        buildings += self.buildings_queue
        return buildings

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

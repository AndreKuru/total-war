from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from building import Building, Condition, Boost
from unit import Unit, Category, Weapon

class Minerium(Enum):
    COPPER = 1
    SILVER = 2
    GOLD = 3

@dataclass
class Province:
    id: str
    name: str
    farm_income: int

    water: bool = False
    sand: bool = False
    minerium: Minerium = None
    bonus: str | Category | Weapon | None = None
    owned: bool = False

    buildings: list[Building] = field(default_factory=list) # buildings constructed
    units: list[Unit] = field(default_factory=list)         # units trainable with buildings constructed

    buildings_queue: list[Building] = field(default_factory=list)
    buildings_queue_time: int = 0 # time remaining for the first building in the queue
    units_queue: list[Unit] = field(default_factory=list)
    units_queue_time: int = 0 # time remaining for the first unit in the queue

    def insert_upgradeds(self, building: Building):
        if building.upgrades:
            self.insert_upgradeds(building.upgrades)
        else:
            if building not in self.buildings:
                self.buildings.append(building)

    def insert(self, buildings: list[Building]):
        for building in buildings:
            if building in self.buildings:
                raise Exception(building.name + " already exists")
            else:
                self.insert_upgradeds(building)
                self.buildings.append(building)

    def remove_upgradeds(self, building_to_remove: Building):
        for building in self.buildings:
            if building.upgrades == building_to_remove.id:
                self.remove_upgradeds(building)
                self.buildings.remove(building)
                break

    def remove(self, buildings: list[Building]):
        for building in buildings:
            if building not in self.buildings:
                raise Exception(building.name + " not exists")
            else:
                self.remove_upgradeds(building)
                self.buildings.remove(building)

    def seasons_to_end_buildings_queue(self):
        seasons = 0
        for building in self.buildings_queue:
            seasons += building.seasons_to_build
        return seasons

    def seasons_to_end_units_queue(self):
        seasons = 0
        for unit in self.units_queue:
            seasons += unit.seasons_to_train
        return seasons

    def purchase_building(self, building: Building):
        if building in self.buildings:
            raise Exception(building.name + " already exists.")
        elif building in self.buildings_queue:
            raise Exception(building.name + " already in queue.")
        else:
            debt = (self.seasons_to_end_buildings_queue(), building.cost)
            self.buildings_queue.append(building)
            return debt

    def purchase_unit(self, unit: Unit):
        pass

def get_province(provinces: list[Province], id: str):
    for province in provinces:
        if province.id == id:
            return province
    
    raise Exception("Invalid province.")

def list_my_provinces(provinces: list[Province]):
    my_provinces = list()
    for province in provinces:
        if province.owned:
            my_provinces.append(province)
    
    for province in my_provinces:
        spaces = ""
        for _ in range(4 - len(province.id)):
            spaces += " "
        print(province.id + spaces + " - " + province.name)

def get_purchasable_and_owned_buildings(all_buildings: list[Building], my_buildings: list[Building], 
water: bool, iron_sand_deposits: bool, minerium: Minerium,
legendary_swordman_event: bool, christianity: bool, churches: int, dutch_acceptance: bool):
    
    purchasable_and_owned_buildings = list()
    for building in all_buildings:
        purchasable = True
        for required in building.requires:
            if isinstance(required, Building):
                if required not in my_buildings:
                    purchasable = False
                    break
            elif isinstance(required, list):
                if not set(required) & set(my_buildings): # If none of the buildings required are my
                    purchasable = False
                    break
            elif isinstance(required, Condition):
                match required:
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

def get_purchasable_buildings(all_buildings: list[Building], my_buildings: list[Building], 
water: bool, iron_sand_deposits: bool, minerium: Minerium,
legendary_swordman_event: bool, christianity: bool, churches: int, dutch_acceptance: bool):

    buildings = get_purchasable_and_owned_buildings(all_buildings, my_buildings, water, iron_sand_deposits, minerium, legendary_swordman_event, christianity, churches, dutch_acceptance)
    
    for building in my_buildings:
        buildings.remove(building)

    return buildings

# Remove building if impossible in province and it's building requiremnts
def is_possible_in_province(building: Building,
water: bool, iron_sand_deposits: bool, minerium: Minerium):
    for required in building.requires:
        if isinstance(required, Building):
            if not is_possible_in_province(building, water, iron_sand_deposits, minerium):
                return False
        else:
            match required:
                case Condition.WATER:
                    if not water:
                        return False
            
                case Condition.IRON_SAND_DEPOSITS:
                    if not iron_sand_deposits:
                        return False
            
                case Condition.NATURAL_MINERAL_DEPOSITS:
                    if not minerium:
                        return False
                
                case _:
                    pass
    
    # end for required
    return True
            

def get_not_yet_purchasable_buildings(all_buildings: list[Building], my_buildings: list[Building], 
water: bool, iron_sand_deposits: bool, minerium: Minerium,
legendary_swordman_event: bool, christianity: bool, churches: int, dutch_acceptance: bool):

    purchsable_and_owned_buildings = get_purchasable_and_owned_buildings(all_buildings, my_buildings, water, iron_sand_deposits, minerium, legendary_swordman_event, christianity, churches, dutch_acceptance)

    not_purchasable_buildings = list()
    for building in all_buildings:
        if building not in purchsable_and_owned_buildings:
            not_purchasable_buildings.append(building)
    
    not_yet_purchasable_buildings = list()
    for building in not_purchasable_buildings:
        if is_possible_in_province(building, water, iron_sand_deposits, minerium):
            not_yet_purchasable_buildings.append(building)

    return not_yet_purchasable_buildings

def get_purchasable_units_and_boosts(all_units: list[Unit], my_buildings: list[Building]):
    purchasable_units = list()
    boost_attack = 0
    boost_armor = 0
    boost_rally = False
    for building in my_buildings:
        if building.produces:
            (produced_unit_id, building_required) = building.produces
            if building_required and building_required in my_buildings:
                new_unit = True
                for unit in purchasable_units:
                    if unit.id == produced_unit_id:
                        new_unit = False
                        unit.boost_morale += 1
                        break
                if new_unit:
                    for unit in all_units:
                        if unit.id == produced_unit_id:
                            purchasable_units.append(deepcopy(unit))
        elif building.boost:
            match building.boost:
                case Boost.ATTACK:
                    boost_attack += 1

                case Boost.ARMOR:
                    boost_armor += 1

                case Boost.RALLY:
                    boost_rally = True

    
    return purchasable_units, boost_attack, boost_armor, boost_rally

def get_not_purchasable_units(all_units: list[Unit], my_buildings: list[Building]):
    purchasable_units, _, _, _ = get_purchasable_units_and_boosts(all_units, my_buildings)

    not_purchasable_units_id = list()
    for unit in all_units:
        not_purchasable_units_id.append(unit.id)

    for purchsable_unit in purchasable_units:
        try:
            not_purchasable_units_id.remove(purchsable_unit.id)
        except ValueError:
            pass

    not_purchasable_units = list()
    for id in not_purchasable_units:
        for unit in all_units:
            if unit.id == id:
                not_purchasable_units.append(unit)
            
    return not_purchasable_units

def get_buildings_with_queue(my_buildilngs: list[Building], buildings_queue: list[Building]):
    buildings = my_buildilngs.copy()
    buildings += buildings_queue
    return buildings


def get_buildings_with_queue_until(my_buildilngs: list[Building], buildings_queue: list[Building], seasons_in_advance: int):
    buildings = my_buildilngs.copy()

    seasons_in_advance -= buildings[0]
    if seasons_in_advance == 0:
        buildings.append(building)

    elif seasons_in_advance > 0:
        buildings.append(building)

        for building in buildings_queue[1:]:
            seasons_in_advance -= building.seasons_to_build
            if seasons_in_advance > 0:
                buildings.append(building)
            elif seasons_in_advance == 0:
                buildings.append(building)
                break
            else:
                break

    return buildings

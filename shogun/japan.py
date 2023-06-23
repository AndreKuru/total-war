from dataclasses import dataclass, field
from enum import Enum
from province import Province, get_province, list_my_provinces, get_purchasable_buildings, get_not_yet_purchasable_buildings, get_buildings_with_queue, get_buildings_with_queue_until, get_purchasable_units_and_boosts, get_not_purchasable_units
from building import Building, list_buildings, remove_all_buildings_upgraded
from unit import Unit, Agent, list_units

TITLE_LEN = 15

class Season(Enum):
    SPRING = 0 # new year
    SUMMER = 1 # new game
    AUTUMN = 2 # profit arrives on this turn end
    WINTER = 3 # brace yourselves

def get_instances(collection: list["Unit"] | list["Agent"] | list["Building"] | list["Province"], ids: list[str]):
    selected_instances = list()
    breaked = False

    for id in ids:
        for instance in collection:
            if instance.id == id:
                if instance in selected_instances:
                    print(instance.name  + "duplicate ignored.")
                else:
                    selected_instances.append(instance)
                breaked = True
                break
        if not breaked:
            raise Exception(id + " not found.")
        breaked = False

    return selected_instances

def print_province_and_season_after_queue(current_year: int, seasons: int, province: Province):
    year = current_year + (seasons // 4)
    season = Season(seasons % 4)
    print("Province:" + province.name + " - " + str(year) + " " + season.name)

def print_province_and_season_after_buildings_queue(current_year: int, current_season: Season, province: Province):
    seasons = province.seasons_to_end_buildings_queue() + current_season.value
    print_province_and_season_after_queue(current_year, seasons, province)

def print_province_and_season_after_units_queue(current_year: int, current_season: Season, province: Province,
boost_attack: int, boost_armor: int, boost_rally: bool):
    seasons = province.seasons_to_end_units_queue() + current_season.value
    print_province_and_season_after_queue(current_year, seasons, province)
    print("Boost Attack: " + boost_attack)
    print("Boost Armor: " + boost_armor)
    if boost_rally:
        print("Boost Rally: Yes")
    else:
        print("Boost Rally: No")

def print_queues_by_season(buildings_queue: list["Building"], buildings_queue_time: int, units_queue: list["Unit"], units_queue_time: int, current_year: int, current_season: Season):

    if len(buildings_queue[0].name) > TITLE_LEN:
        max_str = len(buildings_queue[0].name)
    else:
        max_str = TITLE_LEN # len("BUILDINGS QUEUE")
    
    # create buildings list to print
    if len(buildings_queue):
        buildings_queue_by_season = [buildings_queue[0].name]
        for _ in buildings_queue_time - 1:
            buildings_queue_by_season.append("#")

        for building in buildings_queue:
            if len(building.name) > max_str:
                max_str = len(building.name)
            
            buildings_queue_by_season.append(building.name)
            for _ in building.seasons_to_build - 1:
                buildings_queue_by_season.append("#")

        initial_building = buildings_queue_by_season[0]
    else:
        initial_building = ""

    # create units list to print
    if len(units_queue):
        units_queue_by_season = [units_queue[0].name]
        for _ in units_queue_time - 1:
            units_queue_by_season.append("#")

        for unit in units_queue:
            units_queue_by_season.append(unit.name)
            for _ in unit.seasons_to_train - 1:
                units_queue_by_season.append("#")

        initial_unit = units_queue_by_season[0]
    else:
        initial_unit = ""

    spaces += ""
    for _ in max_str - TITLE_LEN:
        spaces += " "

        # "YEAR.SEASON"
    print("           " + " BUILDINGS QUEUE" + spaces + " | UNITS QUEUE")

    for _ in TITLE_LEN:
        spaces += " "

    print(str(current_year) + "." + current_season.name + " " + initial_building + spaces + " | " + initial_unit)
    for i in range(1, max(len(buildings_queue_by_season), len(units_queue_by_season))):

        if current_season == Season.WINTER:
            current_season = Season.SPRING
            current_year += 1
        else:
            current_season = Season(current_season.value + 1)


        # print year and season
        print(str(current_year) + "." + current_season.name, end=" ")

        # print building in season
        if i < len(buildings_queue_by_season):
            print(buildings_queue_by_season[i], end="")
        else:
            print(spaces)

        # print unit in season
        if i < len(units_queue_by_season):
            print(" | " + units_queue_by_season[i])
        else:
            print(" | " )

@dataclass
class Japan:
    id: str
    units: list[Unit]         # For reference
    provinces: list[Province] # Trocado de posição com buildings, mas n entendi o erro
    buildings: list[Building] # For reference
    current_season: Season = Season.SUMMER
    current_year: int = 1530
    current_money: int = 1000
    debts_by_season: list[int] = field(default_factory=list)
    legendary_swordman_event: bool = False
    christianity: bool = False
    churches: int = 0
    dutch_acceptance: bool = False
    current_province: Province | None = None 

        
    def select(self, input):
        try:
            province = get_province(self.provinces, input)
            if province.owned:
                self.current_province = province
            else:
                raise Exception("Province not owned.")
        except Exception as e:
            print(e)

    def insert(self, input):
        if self.current_province == None:
            print("No province selected.")
        elif len(input) == 0:
            print("No building informed.")
        else:
            try:
                buildings = get_instances(self.buildings, input)
                self.current_province.insert(buildings)
            except Exception as e:
                print("Building" + e)

    def remove(self, input):
        if self.current_province == None:
            print("No province selected.")
        elif len(input) == 0:
            print("No building informed.")
        else:
            try:
                buildings = get_instances(input)
                self.current_province.remove(buildings)
            except Exception as e:
                print("Building" + e)

    def list_provinces(self):
        list_my_provinces(self.provinces)

    def purchase(self):
        pass

    def list_all_buildings(self):
        list_buildings(self.buildings)

    def list_buildings(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            list_buildings(self.current_province.buildings)

    def purchasable_buildings(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            my_buildings_with_queue = get_buildings_with_queue(self.current_province.buildings, self.current_province.buildings_queue)
            purchasable_buildings = get_purchasable_buildings(self.buildings, my_buildings_with_queue, self.current_province.water, self.current_province.sand, self.current_province.minerium, self.legendary_swordman_event, self.christianity, self.churches, self.dutch_acceptance)
            remove_all_buildings_upgraded(purchasable_buildings)
            print_province_and_season_after_buildings_queue(self.current_year, self.current_season, self.current_province)
            list_buildings(purchasable_buildings)

    def not_yet_purchasable_buildings(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            my_buildings_with_queue = get_buildings_with_queue(self.current_province.buildings, self.current_province.buildings_queue)
            not_yet_purchasable_buildings = get_not_yet_purchasable_buildings(self.buildings, my_buildings_with_queue, self.current_province.water, self.current_province.sand, self.current_province.minerium, self.legendary_swordman_event, self.christianity, self.churches, self.dutch_acceptance)
            list_buildings(not_yet_purchasable_buildings)

    def list_all_units(self):
        list_units(self.units)

    def purchasable_units(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            seasons = self.current_province.seasons_to_end_units_queue
            my_buildings_with_queue = get_buildings_with_queue_until(self.current_province.buildings, self.current_province.buildings_queue, seasons)
            purchasable_units, boost_attack, boost_armor, boost_rally = get_purchasable_units_and_boosts(self.units, my_buildings_with_queue)
            print_province_and_season_after_units_queue(self.current_year, self.current_season, self.current_province, boost_attack, boost_armor, boost_rally)
            list_units(purchasable_units)

    def not_purchasable_units(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            seasons = self.current_province.seasons_to_end_units_queue
            my_buildings_with_queue = get_buildings_with_queue_until(self.current_province.buildings, self.current_province.buildings_queue, seasons)
            not_purchasable_units = get_not_purchasable_units(self.units, my_buildings_with_queue)
            list_units(not_purchasable_units)

    def show_queues_in_province(self):
        if self.current_province == None:
            print("No province selected.")
        else:
            print_queues_by_season(self.current_province.buildings_queue,
                                    self.current_province.buildings_queue_time,
                                    self.current_province.units_queue,
                                    self.current_province.units_queue_time,
                                    self.current_year,
                                    self.current_season) # Por que current_season n é sobreescrito?

    def show_all_buildings_queues(self):
        pass

    def show_all_units_queues(self):
        pass

    def show_money(self):
        pass

    def update_money(self):
        pass

    def turn_end(self):
        pass
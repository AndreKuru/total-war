from dataclasses import dataclass, field
from enum import Enum
from province import Province, get_province, list_my_provinces, get_purchasable_buildings, get_not_purchasable_buildings_yet, get_buildings_with_queue, get_buildings_with_queue_until, get_purchasable_units_and_boosts, get_not_purchasable_units
from building import Building, list_buildings, remove_all_buildings_upgraded
from unit import Unit, Agent, list_units

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

@dataclass
class Japan:
    id: str
    units: list["Unit"]         # For reference
    buildings: list["Building"] # For reference
    provinces: list["Province"]
    current_season: "Season" = Season.SUMMER
    current_year: int = 1530
    current_money: int = 1000
    debts_by_season: list[int] = field(default_factory=list)
    legendary_swordman_event: bool = False
    christianity: bool = False
    churches: int = 0
    dutch_acceptance: bool = False

        
    def run(self):
        current_province = None 

        while True:
            command = input(id + ":")
            command = command.split(" ")

            match command[0]:
                case "select" | "s":
                    try:
                        province = get_province(self.provinces, command[1])
                        if province.owned:
                            current_province = province
                        else:
                            raise Exception("Province not owned.")
                    except Exception as e:
                        print(e)

                case "insert" | "i":
                    if current_province == None:
                        print("No province selected.")
                    elif len(command[1:]) == 0:
                        print("No building informed.")
                    else:
                        try:
                            buildings = get_instances(self.buildings, command[1:])
                            current_province.insert(buildings)
                        except Exception as e:
                            print("Building" + e)

                case "remove" | "r":
                    if current_province == None:
                        print("No province selected.")
                    elif len(command[1:]) == 0:
                        print("No building informed.")
                    else:
                        try:
                            buildings = get_instances(command[1:])
                            current_province.remove(buildings)
                        except Exception as e:
                            print("Building" + e)

                case "list" | "list_provinces" | "l":
                    list_my_provinces(self.provinces)

                case "purchase" | "p":
                    pass

                case "all_buildings" | "ab":
                    list_buildings(self.buildings)

                case "buildings" | "b":
                    list_buildings(current_province.buildings)

                case "purchsable_buildings" | "pb":
                    my_buildings_with_queue = get_buildings_with_queue(current_province.buildings, current_province.buildings_queue)
                    purchasable_buildings = get_purchasable_buildings(self.buildings, my_buildings_with_queue, current_province.water, current_province.sand, current_province.minerium, self.legendary_swordman_event, self.christianity, self.churches, self.dutch_acceptance)
                    remove_all_buildings_upgraded(purchasable_buildings)
                    print_province_and_season_after_buildings_queue(self.current_year, self.current_season, current_province)
                    list_buildings(purchasable_buildings)

                case "not_purchasable_buildings_yet" | "npb":
                    my_buildings_with_queue = get_buildings_with_queue(current_province.buildings, current_province.buildings_queue)
                    not_purchasable_buildings_yet = get_not_purchasable_buildings_yet(self.buildings, my_buildings_with_queue, current_province.water, current_province.sand, current_province.minerium, self.legendary_swordman_event, self.christianity, self.churches, self.dutch_acceptance)
                    list_buildings(not_purchasable_buildings_yet)

                case "all_units" | "au":
                    list_units(self.units)

                case "units" | "u":
                    list_units(current_province.unit)

                case "purchasable_units" | "pu":
                    seasons = current_province.seasons_to_end_units_queue
                    my_buildings_with_queue = get_buildings_with_queue_until(current_province.buildings, current_province.buildings_queue, seasons)
                    purchasable_units, boost_attack, boost_armor, boost_rally = get_purchasable_units_and_boosts(self.units, my_buildings_with_queue)
                    print_province_and_season_after_units_queue(self.current_year, self.current_season, current_province, boost_attack, boost_armor, boost_rally)
                    list_units(purchasable_units)

                case "not_purchasable_units" | "npu":
                    seasons = current_province.seasons_to_end_units_queue
                    my_buildings_with_queue = get_buildings_with_queue_until(current_province.buildings, current_province.buildings_queue, seasons)
                    not_purchasable_units = get_not_purchasable_units(self.units, my_buildings_with_queue)
                    list_units(not_purchasable_units)
                    pass

                case "show_queue_by_season" | "q":
                    pass

                case "show_queue_by_purchase" | "qp":
                    pass

                case "show_money" | "m":
                    pass

                case "update_money" | "um":
                    pass

                case "turn_end" | "t":
                    pass

                case _:
                    print("Command invalid. Try again.")

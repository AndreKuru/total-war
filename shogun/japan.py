from dataclasses import dataclass, field
from enum import Enum
from province import Province, get_province, get_provinces
from building import Building, get_buildings
from unit import Unit, get_units

class Season(Enum):
    SPRING = 0 # new year
    SUMMER = 1 # new game
    AUTUMN = 2 # profit arrives on this turn end
    WINTER = 3 # brace yourselves

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

    def list_my_provinces(self):
        my_provinces = list()
        for province in self.provinces:
            if province.owned:
                my_provinces.append(province)
        
        for province in my_provinces:
            spaces = ""
            for _ in 4 - len(province.id):
                spaces += " "
            print(province.id + spaces + "- " + province.name)
        
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
                            buildings = get_buildings(self.buildings, command[1:])
                            current_province.insert(buildings)
                        except Exception as e:
                            print(e)

                case "remove" | "r":
                    if current_province == None:
                        print("No province selected.")
                    elif len(command[1:]) == 0:
                        print("No building informed.")
                    else:
                        try:
                            buildings = get_buildings(command[1:])
                            current_province.remove(buildings)
                        except Exception as e:
                            print(e)

                case "list" | "list_provinces" | "l":
                    self.list_my_provinces()

                case "purchase" | "p":
                    pass

                case "all_buildings" | "ab":
                    pass

                case "buildings" | "b":
                    pass

                case "purchsable_buildings" | "pb":
                    pass

                case "not_purchsable_buildings_yet" | "npb":
                    pass

                case "all_units" | "au":
                    pass

                case "units" | "u":
                    pass

                case "purchsable_units" | "pu":
                    pass

                case "not_purchsable_units_yet" | "npu":
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

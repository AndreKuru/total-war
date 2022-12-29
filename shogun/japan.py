from dataclasses import dataclass, field
from enum import Enum
from province import Province, get_province, get_provinces
from building import Building, get_building, get_buildings
from unit import Unit, get_unit, get_units

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
    current_province: "Province" = None

    def run(self):
        while True:
            command = input(id + ":")
            
            command = command.split(" ")

            match command[0]:
                case "select" | "s":
                    current_province = get_province(self.provinces, command[1])

                    '''               
                case "insert" | "i":
                    current_province.insert_building(command[1])

                case "remove" | "r":

                case "list" | "list_provinces" | "l":

                case "purchase" | "p":

                case "all_buildings" | "ab":

                case "buildings" | "b":

                case "purchsable_buildings" | "pb":

                case "not_purchsable_buildings_yet" | "npb":

                case "all_units" | "au":

                case "units" | "u":

                case "purchsable_units" | "pu":

                case "not_purchsable_units_yet" | "npu":

                case "show_queue_by_season" | "q":

                case "show_queue_by_purchase" | "qp":

                case "show_money" | "m"

                case "update_money" | "um"

                case "turn_end" | "t"

                    '''
                case _:
                    print("Command invalid. Try again.")

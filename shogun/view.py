from cmd import Cmd
from japan import Japan

class Prompt(Cmd):
    intro = "Welcome to Shogun - Total War:"

    def __init__(self, controller: Japan) -> None:
        self.prompt = controller.id + ": "
        self.controller = controller
        Cmd.__init__(self)

    def do_exit(self, input) -> None:
        print("Exiting game.")
        return True

    def do_select(self, input: str) -> None:
        self.controller.select(input)

    def do_insert(self, input: str) -> None:
        self.controller.insert(input)

    def do_remove(self, input: str) -> None:
        self.controller.remove()

    def do_list_provinces(self, input: str) -> None:
        self.controller.list_provinces()

    def do_purchase(self, input: str) -> None:
        self.controller.purchase(input)

    def do_list_all_buildings(self, input: str) -> None:
        self.controller.list_all_buildings()

    def do_list_buildings(self, input: str) -> None:
        self.controller.list_buildings()

    def do_purchasable_buildings(self, input: str) -> None:
        self.controller.purchasable_buildings()

    def do_not_purchasable_buildings_yet(self, input: str) -> None:
        self.controller.not_purchasable_buildings_yet()

    def do_list_all_units(self, input: str) -> None:
        self.controller.list_all_units()

    def do_purchasable_units(self, input: str) -> None:
        self.controller.purchasable_units()

    def do_not_purchasable_units(self, input: str) -> None:
        self.controller.not_purchasable_units()

    def do_show_queues_in_province(self, input: str) -> None:
        self.controller.show_queues_in_province()

    def do_show_all_buildings_queues(self, input: str) -> None:
        self.controller.show_all_buildings_queues()

    def do_show_all_units_queues(self, input: str) -> None:
        self.controller.show_all_units_queues()

    def do_show_money(self, input: str) -> None:
        self.controller.show_money()

    def do_update_money(self, input: str) -> None:
        self.controller.update_money(input)

    def do_turn_end(self, input: str) -> None:
        self.controller.turn_end()

    def default(self, input: str) -> None:
        match input:
            case "s":
                return self.do_select(input)
            case "i":
                return self.do_insert(input)
            case "r":
                return self.do_remove(input)
            case "l":
                return self.do_list_provinces(input)
            case "p":
                return self.do_purchase(input)
            case "ab":
                return self.do_list_all_buildings(input)
            case "b":
                return self.do_list_buildings(input)
            case "pb":
                return self.do_purchasable_buildings(input)
            case "npb":
                return self.do_not_purchasable_buildings_yet(input)
            case "au":
                return self.do_list_all_units(input)
            case "pu":
                return self.do_purchasable_units(input)
            case "npu":
                return self.do_not_purchasable_units(input)
            case "q":
                return self.do_show_queues_in_province(input)
            case "qb":
                return self.do_show_all_buildings_queues(input)
            case "qu":
                return self.do_show_all_units_queues(input)
            case "m":
                return self.do_show_money(input)
            case "um":
                return self.do_update_money(input)
            case "t":
                return self.do_turn_end(input)
            case _:
                return super().default(input)
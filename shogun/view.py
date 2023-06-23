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
        self.controller.remove(input)

    def do_list_provinces(self) -> None:
        self.controller.list_provinces()

    def do_purchase(self, input: str) -> None:
        self.controller.purchase(input)

    def do_list_all_buildings(self, input: str) -> None:
        self.controller.list_all_buildings()

    def do_list_buildings(self, input: str) -> None:
        self.controller.list_buildings()

    def do_purchasable_buildings(self, input: str) -> None:
        self.controller.purchasable_buildings()

    def do_not_yet_purchasable_buildings(self, input: str) -> None:
        self.controller.not_yet_purchasable_buildings()

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
            case _:
                return super().default(input)

    def do_help(self, *args):
        Cmd.do_help(self, *args)
        print("Shortcuts: ")
        print("EOF = Ctrl + D = exit")
        print("s   = select")
        print("i   = insert")
        print("r   = remove")
        print("l   = list_provinces")
        print("p   = purchase")
        print("ab  = list_all_buildings")
        print("b   = list_buildings")
        print("pb  = purchasable_buildings")
        print("npb = not_yet_purchasable_buildings")
        print("au  = list_all_units")
        print("pu  = purchasable_units")
        print("npu = not_purchasable_units")
        print("q   = show_queues_in_province")
        print("qb  = show_all_buildings_queues")
        print("qu  = show_all_units_queues")
        print("m   = show_money")
        print("um  = update_money")
        print("t   = turn_end")

    def help_help(self) -> None:
        print("Print all available commands.")

    def help_exit(self) -> None:
        print("Exit the session.")
    
    def help_select(self) -> None:
        print("Select the informed province as long as the province is owned.")
        
    def help_insert(self) -> None:
        print("Insert informed building in the current selected province.")
        
    def help_remove(self) -> None:
        print("Remove informed building from the current selected province.")
        
    def help_list_provinces(self) -> None:
        print("List all provinces owned.")
        
    def help_purchase(self) -> None:
        print("Purchase ...")
        
    def help_list_all_buildings(self) -> None:
        print("List all existing buildings in the game.")
        
    def help_list_buildings(self) -> None:
        print("List all existing buildings in the current selected province.")
        
    def help_purchasable_buildings(self) -> None:
        print("List all purchasable buildings in the current selected province.")
        
    def help_not_yet_purchasable_buildings(self) -> None:
        print("List all not yet purchasable buildings in the current selected province.")
        
    def help_list_all_units(self) -> None:
        print("List all existing units in the game.")
        
    def help_purchasable_units(self) -> None:
        print("List all purchasable units in the current selected province.")
        
    def help_not_purchasable_units(self) -> None:
        print("List all not purchasable units in the current selected province.")
        
    # def help_show_queues_in_province(self) -> None:
    #     print("")
    #     
    # def help_show_all_buildings_queues(self) -> None:
    #     print("")
    #     
    # def help_show_all_units_queues(self) -> None:
    #     print("")
    #     
    # def help_show_money(self) -> None:
    #     print("")
    #     
    # def help_update_money(self) -> None:
    #     print("")
    #     
    # def help_turn_end(self) -> None:
    #     print("")

    do_EOF = do_exit
    do_s = do_select
    do_i = do_insert
    do_r = do_remove
    do_l = do_list_provinces
    do_p = do_purchase
    do_ab = do_list_all_buildings
    do_b = do_list_buildings
    do_pb = do_purchasable_buildings
    do_npb = do_not_yet_purchasable_buildings
    do_au = do_list_all_units
    do_pu = do_purchasable_units
    do_npu = do_not_purchasable_units
    do_q = do_show_queues_in_province
    do_qb = do_show_all_buildings_queues
    do_qu = do_show_all_units_queues
    do_m = do_show_money
    do_um = do_update_money
    do_t = do_turn_end

    help_EOF = help_exit
    help_s = help_select
    help_i = help_insert
    help_r = help_remove
    help_l = help_list_provinces
    help_p = help_purchase
    help_ab = help_list_all_buildings
    help_b = help_list_buildings
    help_pb = help_purchasable_buildings
    help_npb = help_not_yet_purchasable_buildings
    help_au = help_list_all_units
    help_pu = help_purchasable_units
    help_npu = help_not_purchasable_units
    # help_q = help_show_queues_in_province
    # help_qb = help_show_all_buildings_queues
    # help_qu = help_show_all_units_queues
    # help_m = help_show_money
    # help_um = help_update_money
    # help_t = help_turn_end
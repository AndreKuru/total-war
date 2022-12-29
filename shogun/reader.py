from japan import Japan
from province import Province
from building import Building
from unit import Unit, Category, Class, Weapon

def read_units(file_path):
    file = open(file_path, "r")
    file_lines = file.readlines()
    file_lines = [line.rstrip("\n") for line in file_lines]
    units = list()
    for line in file_lines:
        data = line.split(";")
        if len(data) > 7:
            id = data[0]
            name = data[1]
            category = Category(int(data[2]))
            class_unit = Class(int(data[3]))
            weapon = Weapon(int(data[4]))
            soldiers = int(data[5])
            cost = int(data[6])
            seasons_to_train = int(data[7])

            if len(data) > 8:
                morale_boost = int(data[8])
                if len(data) > 9:
                    attack_boost = int(data[9])
                    if len(data) > 10:
                        armor_boost = int(data[10])
                        if len(data) > 11:
                            raise Exception("Too many data to unit.")

                        unit = Unit(id, name, category, class_unit, weapon, soldiers, cost, seasons_to_train, morale_boost, attack_boost, armor_boost)
                    else:
                        unit = Unit(id, name, category, class_unit, weapon, soldiers, cost, seasons_to_train, morale_boost, attack_boost)
                else:
                    unit = Unit(id, name, category, class_unit, weapon, soldiers, cost, seasons_to_train, morale_boost)
            else:
                unit = Unit(id, name, category, class_unit, weapon, soldiers, cost, seasons_to_train)
        else:
            raise Exception("Unit data insufficient.")
        
        units.append(unit)

    return units
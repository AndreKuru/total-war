from pathlib import Path
from province import Province, Minerium
from building import Building
from unit import Unit, Category, Class, Weapon

def read_units(file_path: Path):
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

def read_buildings(file_path: Path):
    file = open(file_path, "r")
    file_lines = file.readlines()
    file_lines = [line.rstrip("\n") for line in file_lines]

    buildings = list()
    for line in file_lines:
        data = line.split(";")
        if len(data) == 7:
            id = data[0]
            name = data[1]
            cost = int(data[2])
            seasons_to_build = int(data[3])
            requires = data[4]
            produces = data[5]
            upgrades = data[6]
            building = Building(id, name, cost, seasons_to_build, requires, produces, upgrades)
            buildings.append(building)
        else:
            raise Exception("Building input has incorrect format.")
        
    return buildings

def read_provinces(file_path: Path, initial: bool = False):
    file = open(file_path, "r")
    file_lines = file.readlines()
    file_lines = [line.rstrip("\n") for line in file_lines]

    provinces = list()
    for line in file_lines:
        data = line.split(";")
        if len(data) > 2:
            id = data[0]
            name = data[1]
            farm_income = int(data[2])

            if len(data) > 3:
                water = bool(data[3])

                if len(data) > 4:
                    minerium = Minerium(int(data[4]))

                    if len(data) > 5:
                        bonus = data[5]
                        match bonus[0]:
                            case 'c':
                                bonus = Class(int(bonus[1:]))
                            case 'w':
                                bonus = Weapon(int(bonus[1:]))
                            case 'i':
                                bonus = bonus[1:]
                            case _:
                                raise Exception("Invalid building bonus.")
                        
                        if len(data) > 6:
                            if not initial:
                                raise Exception("Too many data to initial province.")

                            owned = bool(data[6])

                            if len(data) > 7:
                                buildings = data[7].split(",")
                                
                                if len(data) > 8:
                                    units_trainable = data[8].split(",")

                                    if len(data) > 9:
                                        raise Exception("Too many data to province.")
                                    
                                    province = Province(id, name, farm_income, water, minerium, bonus, owned, buildings, units_trainable)

                                else:
                                    province = Province(id, name, farm_income, water, minerium, bonus, owned, buildings)

                            else:
                                province = Province(id, name, farm_income, water, minerium, bonus, owned)

                        else:
                            province = Province(id, name, farm_income, water, minerium, bonus)

                    else:
                        province = Province(id, name, farm_income, water, minerium)

                else:
                    province = Province(id, name, farm_income, water)

            else:
                province = Province(id, name, farm_income)
        
        else:
            raise Exception("Insuficient data to province.")

        provinces.append(province)
    
    return provinces
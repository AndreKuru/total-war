from pathlib import Path
from province import Province, Minerium
from building import Building, Condition, Boost
from unit import Unit, Category, Class, Weapon, Agent
from typing import Self
from copy import deepcopy

import re


def insert_new_unit(
    all_units: dict[Unit], 
    id: str,
    name: str,
    category: str,
    class_unit: str,
    weapon: str,
    soldiers: str,
    cost: str,
    seasons_to_train: str | int = 1,
) -> None:
    category = Category(int(category))
    class_unit = Class(int(class_unit))
    weapon = Weapon(int(weapon))
    soldiers = int(soldiers)
    cost = int(cost)
    seasons_to_train = int(seasons_to_train)
    new_unit = Unit(id, name, category, class_unit, weapon, soldiers, cost, seasons_to_train)
    all_units[id] = new_unit

def read_units(lines: list[str]):
    units = dict()
    for line in lines:
        if re.match(' *#', line) or re.match(' *$', line):
            continue
        data = line.split(";")
        if len(data) >= 7 and len(data) <= 8:
            insert_new_unit(units, *data)
        else:
            raise Exception("Invalid unit input: ", line)
        
    return units

def read_agents(lines: list[str]):
    agents = dict()
    for line in lines:
        if re.match(' *#', line) or re.match(' *$', line):
            continue
        data = line.split(";")
        if len(data) >= 4:
            id = data[0]
            name = data[1]
            cost = int(data[2])
            seasons_to_train = int(data[3])
            if re.match("None$", data[4]):
                morale_boost = None
            else:
                morale_boost = int(data[4])

            new_agent = Agent(id, name, cost, seasons_to_train, morale_boost)
            agents[id] = new_agent
        else:
            raise Exception("Invalid agent input: ", line)
        
    return agents

def get_unit_by_id(unit_id: str, all_units: dict[Unit]):
    morale_boost = len(re.findall('\+', unit_id))
    unit_id = unit_id.strip('+')
    unit: Unit = deepcopy(all_units[unit_id])
    unit.morale_boost = morale_boost
    return unit

def insert_new_building(
    all_buildings:  dict[Building],
    all_units:  dict[Unit],
    all_upgrades: list[tuple[str,str]],
    id: str,
    name: str,
    cost: str,
    seasons_to_build: str,
    upgrades_to: str | None = None,
    requires: str | None = None,
    produces: str | None = None,
    boost: str | None = None,
) -> Building:
    cost = int(cost)
    seasons_to_build = int(seasons_to_build)

    if upgrades_to == "None":
        upgrades_to = None

    if requires == "None":
        requires = None

    if produces == "None":
        produces = None

    if boost == "None":
        boost = None

    if upgrades_to is not None:
        if not re.match("None$", upgrades_to):
            all_upgrades.append((id, upgrades_to))

    if requires is not None:
        all_required = list()
        for required in requires.split(','):
            if required.isnumeric():
                required = Condition(int(required))
            else:
                if re.search('\|', required):
                    required = required.split('|')
                    required = [all_buildings[required_option] for required_option in required]
                else:
                    required = all_buildings[required]

            all_required.append(required)
        requires = all_required

    if produces is not None:
        all_produced = list()
        for produced in produces.split(','):
            if re.search(':', produced):
                unit_id, building_required_id = produced.split(':')
                unit = get_unit_by_id(unit_id, all_units)
                building_required = all_buildings[building_required_id]
                all_produced.append((unit, building_required))
            else:
                unit = get_unit_by_id(produced, all_units)
                all_produced.append(unit)
        
        produces = all_produced

    if boost is not None:
        boost = Boost(int(boost))

    new_building = Building(id, name, cost, seasons_to_build, None, requires, produces, boost)
    all_buildings[id] = new_building

def read_buildings(lines: list[str], units: list[Unit]):
    buildings = dict()
    upgrades = list()
    for line in lines:
        if re.match(' *#', line) or re.match(' *$', line):
            continue
        data = line.split(";")
        if len(data) >= 4 and len(data) <= 8:
            insert_new_building(buildings, units, upgrades, *data)
        else:
            raise Exception("Invalid building input.")
        
    return buildings

def insert_new_province(
    all_provinces: list[Province],
    id: str,
    name: str,
    farm_income: str,
    water: str | bool = False,
    sand: str | bool = False,
    minerium: str | None = None,
    bonus: str | Category | Weapon | None = None,
) -> None:
    farm_income = int(farm_income)

    if isinstance(water, str):
        water = bool(int(water))

    if isinstance(sand, str):
        sand = bool(int(sand))

    if minerium == "None":
        minerium = None

    if minerium is not None:
        minerium = Minerium(int(minerium))
    
    if bonus is not None:
        match bonus[0]:
            case 'c':
                bonus = Class(int(bonus[1:]))
            case 'w':
                bonus = Weapon(int(bonus[1:]))
            case 'i':
                bonus = bonus[1:]
            case _:
                raise Exception("Invalid building bonus input.")
    
    province = Province(id, name, farm_income, water, sand, minerium, bonus)
    all_provinces.append(province)

def read_provinces(file_path: Path, initial: bool = False):
    file = open(file_path, "r")
    file_lines = file.readlines()
    file_lines = [line.rstrip("\n") for line in file_lines]

    provinces = list()
    for line in file_lines:
        if re.match(' *#', line) or re.match(' *$', line):
            continue
        data = line.split(";")
        if len(data) >= 3 and len(data) <= 7:
            insert_new_province(provinces, *data)
        else:
            raise Exception("Invalid province input.")

    return provinces

def read_purchasables(file_path: Path):
    file = open(file_path, "r")
    file_lines = file.readlines()
    file_lines = [line.rstrip("\n") for line in file_lines]

    for i in range(len(file_lines)):
        line = file_lines[i]

        if re.match(' *#', line) and re.search('Unit', line):
            units_begin = i
            continue
        
        if re.match(' *#', line) and re.search('Agent', line):
            agents_begin = i
            continue

        if re.match(' *#', line) and re.search('Building', line):
            buildings_begin = i
            break
    
    units = read_units(file_lines[units_begin + 1: agents_begin])
    agents = read_agents(file_lines[agents_begin + 1: buildings_begin])
    buildings = read_buildings(file_lines[buildings_begin + 1:], units | agents)

    return units, agents, buildings
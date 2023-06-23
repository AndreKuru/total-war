from pathlib import Path
from reader import read_units, read_buildings, read_provinces
from view import Prompt
from japan import Japan

def main():
    id = "Uesugi"
    units = read_units(Path.cwd() / "data" / "shogun-units.txt")
    buildings = read_buildings(Path.cwd() / "data" / "shogun-buildings.txt")
    provinces = read_provinces(Path.cwd() / "data" / "shogun-provinces.txt")
    japan = Japan(id, units, buildings=buildings, provinces=provinces)
    prompt = Prompt(japan)
    prompt.cmdloop()
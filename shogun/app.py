from pathlib import Path
from reader import read_purchasables, read_provinces
from view import Prompt
from japan import Japan

def main():
    id = "Uesugi"
    units, agents, buildings = read_purchasables(Path.cwd() / "data" / "shogun-purchasables.txt")
    provinces = read_provinces(Path.cwd() / "data" / "shogun-provinces.txt")
    japan = Japan(id, units, buildings=buildings, provinces=provinces)
    prompt = Prompt(japan)
    prompt.cmdloop()
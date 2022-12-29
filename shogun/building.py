from dataclasses import dataclass


@dataclass
class Building:
    id: str
    name: str
    cost: int
    requires: str
    produces: str
    upgrades: str
    seasons_to_build: int
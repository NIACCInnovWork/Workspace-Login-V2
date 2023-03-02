from typing import List, Dict

all_stats = {}

def stat(stat_class):
    all_stats[stat_class.__name__] = stat_class

    return stat_class


class Scaler:
    def __init__(self, demention: str, value: any):
        self.demention = demention
        self.value = value


class Point:
    def __init__(self, coordinates: List[Scaler]):
        self.coordinates = coordinates

    def to_dict(self) -> Dict:
        return { c.demention: c.value for c in self.coordinates }

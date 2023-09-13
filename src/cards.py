import json
import re
from dataclasses import dataclass
from enum import Enum
from typing import Set

import requests


class Color(Enum):
    WHITE = 'W'
    BLUE = 'U'
    BLACK = 'B'
    RED = 'R'
    GREEN = 'G'
    COLORLESS = 'C'


class Rarity(Enum):
    COMMON = 'C'
    UNCOMMON = 'U'
    RARE = 'R'
    MYTHIC = 'M'


@dataclass
class Card:
    name: str
    colors: Set[Color]
    rarity: Rarity
    rating: float

    def __hash__(self):
        return hash(self.name)


def get_cards() -> Set[Card]:
    response = requests.get('https://draftsim.com/generated/LTR.js')
    raw = response.text.split('=', 1)[-1].replace(';', '').strip()
    return {
        Card(
            name=x['name'].replace('_', ' '),
            colors=__convert_colors(x['castingcost1']),
            rarity=Rarity(x['rarity']),
            rating=float(x['myrating'])
        )
        for x in json.loads(re.sub(r'(\w+)(\s*:\s*)', r'"\1"\2', raw).replace(',]', ']'))
    }


def __convert_colors(casting_cost: str) -> Set[Color]:
    converted = set([Color(x) for x in re.sub(r'(X|[0-9])', '', casting_cost)])
    return converted or {Color.COLORLESS}

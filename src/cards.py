import json
import re
from dataclasses import dataclass
from typing import List

import requests


@dataclass
class Card:
    name: str
    colors: List[str]
    rarity: str
    rating: float


def get_cards():
    response = requests.get('https://draftsim.com/generated/LTR.js')
    raw = response.text.split('=', 1)[-1].replace(';', '').strip()
    return [
        Card(
            name=x['name'].replace('_', ' '),
            colors=list(set(re.sub(r'(X|[0-9])', '', x['castingcost1']))),
            rarity=x['rarity'],
            rating=float(x['myrating'])
        )
        for x in json.loads(re.sub(r'(\w+)(\s*:\s*)', r'"\1"\2', raw).replace(',]', ']'))
    ]

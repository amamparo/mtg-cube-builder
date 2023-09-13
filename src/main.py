from dataclasses import dataclass
from typing import Set, Dict, List, Collection, Optional

from prettytable import PrettyTable

from src.cards import get_cards, Card, Rarity, Color


@dataclass
class Settings:
    players: int = 8
    n_of_each_rare_up: int = 1
    n_of_each_uncommon: int = 2
    n_of_each_common: int = 3


settings = Settings()

cards: Set[Card] = get_cards()


def main():
    total_packs = settings.players * 3
    cube = Cube() \
        .merge(__get_subcube({Rarity.RARE, Rarity.MYTHIC}, total_packs, 1)) \
        .merge(__get_subcube({Rarity.UNCOMMON}, total_packs * 4, 2)) \
        .merge(__get_subcube({Rarity.COMMON}, total_packs * 10, 3))
    print(cube)


class Cube:
    def __init__(self, cards: Optional[Collection[Card]] = None):
        self.__cards = list(cards or [])

    def add(self, card: Card) -> None:
        self.__cards.append(card)

    def merge(self, other: 'Cube') -> 'Cube':
        self.__cards.extend(other.__cards)
        return self

    @property
    def cards(self) -> List[Card]:
        return self.__cards

    def __len__(self) -> int:
        return len(self.__cards)

    def __str__(self) -> str:
        as_str = ''
        for color in {item for sublist in [x.colors for x in cards] for item in sublist}:
            color_cards = sorted([x for x in self.__cards if color in x.colors], key=lambda x: x.rating, reverse=True)
            as_str += f'\n{color} ({len(color_cards)})\n---------'
            for card in color_cards:
                as_str += f'\n{card.name} ({card.rating})'
        return as_str


def __get_subcube(rarities: Collection[Rarity], n_cards: int, n_of_each: int) -> Cube:
    available_cards: Set[Card] = {x for x in cards if x.rarity in rarities}
    optimal_distribution = __distribution(available_cards)

    subcube = Cube()

    while len(subcube) < n_cards:
        current_distribution = __distribution(subcube.cards)
        distribution_distances = {c: v - current_distribution.get(c, 0) for c, v in optimal_distribution.items()}
        high_distribution_distance = max(distribution_distances.values())
        candidate_colors = {c for c, v in distribution_distances.items() if v == high_distribution_distance}
        candidate_cards = filter(lambda x: candidate_colors.intersection(x.colors), available_cards)
        next_card = sorted(candidate_cards, key=lambda x: x.rating).pop()
        for _ in range(n_of_each):
            subcube.add(next_card)
        available_cards.remove(next_card)

    return subcube


def __distribution(_cards: Collection[Card]) -> Dict[Color, float]:
    colors = {}
    for card in _cards:
        for color in card.colors:
            colors[color] = colors.get(color, 0) + 1
    total = sum(colors.values())
    return {c: v / total for c, v in colors.items()}


if __name__ == '__main__':
    main()

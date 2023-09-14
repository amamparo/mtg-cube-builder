from os import getcwd, path
from typing import Set, Dict, List, Collection, Optional

from src.cards import get_cards, Card, Rarity, Color

n_players = 8


def main():
    cards = {x for x in get_cards() if len(x.colors) <= 2}
    total_packs = n_players * 3
    cube = Cube() \
        .merge(__get_subcube(cards, {Rarity.MYTHIC, Rarity.RARE}, total_packs, 1)) \
        .merge(__get_subcube(cards, {Rarity.UNCOMMON}, total_packs * 4, 2)) \
        .merge(__get_subcube(cards, {Rarity.COMMON}, total_packs * 10, 4))
    with open(path.join(getcwd(), 'cube.txt'), 'w') as f:
        f.write('\n'.join(x.name for x in cube.cards))


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


def __get_subcube(cards: Set[Card], rarities: Collection[Rarity], n_cards: int, n_of_each: int) -> Cube:
    available_cards: Set[Card] = {x for x in cards if x.rarity in rarities and len(x.colors) <= 2}
    optimal_distribution = __distribution(available_cards)
    subcube = Cube()

    while len(subcube) < n_cards:
        current_distribution = __distribution(subcube.cards)
        distribution_distances = {c: v - current_distribution.get(c, 0) for c, v in optimal_distribution.items()}
        high_distribution_distance = max(distribution_distances.values())
        candidate_colors = {c for c, v in distribution_distances.items() if v == high_distribution_distance}
        candidate_cards = filter(lambda x: candidate_colors.intersection(x.colors), available_cards)
        next_card = sorted(candidate_cards, key=lambda x: x.rating, reverse=True)[0]
        for _ in range(n_of_each):
            subcube.add(next_card)
        available_cards.remove(next_card)

    return subcube


def __distribution(cards: Collection[Card]) -> Dict[Color, float]:
    distribution = {c: 0 for c in Color}
    for card in cards:
        for color in card.colors:
            distribution[color] += 1
    total = sum(distribution.values()) or 1
    return {c: v / total for c, v in distribution.items()}


if __name__ == '__main__':
    main()

from typing import Set, Dict

from src.cards import get_cards, Card, Rarity, Color

N = 48

cards: Set[Card] = {x for x in get_cards() if len(x.colors) <= 2}


def get_subcube(rarities: Set[Rarity], n: int) -> Set[Card]:
    available_cards: Set[Card] = {x for x in cards if x.rarity in rarities}
    optimal_distribution = __distribution(available_cards)

    subcube: Set[Card] = set()

    while len(subcube) < n:
        current_distribution = __distribution(subcube)
        distribution_distances = {c: v - current_distribution.get(c, 0) for c, v in optimal_distribution.items()}
        high_distribution_distance = max(distribution_distances.values())
        candidate_colors = {c for c, v in distribution_distances.items() if v == high_distribution_distance}
        next_card = sorted(
            [x for x in available_cards if candidate_colors.intersection(x.colors)],
            key=lambda x: x.rating, reverse=True
        )[0]
        subcube.add(next_card)
        available_cards.remove(next_card)

    return subcube


def main():
    cube: Set[Card] = set()
    cube.update(get_subcube({Rarity.RARE, Rarity.MYTHIC}, 24))
    cube.update(get_subcube({Rarity.UNCOMMON}, 48))
    cube.update(get_subcube({Rarity.COMMON}, 80))

    for color in {item for sublist in [x.colors for x in cards] for item in sublist}:
        color_cards = sorted([x for x in cube if color in x.colors], key=lambda x: x.rating, reverse=True)
        print(f'\n{color} ({len(color_cards)})\n---------')
        for card in color_cards:
            print(f'{card.name} ({card.rating})')


def __distribution(_cards: Set[Card]) -> Dict[Color, float]:
    colors = {}
    for card in _cards:
        for color in card.colors:
            colors[color] = colors.get(color, 0) + 1
    total = sum(colors.values())
    return {c: v / total for c, v in colors.items()}


if __name__ == '__main__':
    main()

import random
from copy import deepcopy
from statistics import mean

from simanneal import Annealer

from src.cards import get_cards

required_card_names = ['The One Ring']

N = 48
ANNEAL_STEPS = 25_000

cards = [x for x in get_cards() if x.rarity in set('RM') and len(x.colors) <= 2]
max_rating = max(x.rating for x in cards)
colors = set([item for sublist in [x.colors for x in cards] for item in sublist])


class Problem(Annealer):
    def __init__(self):
        self.steps = ANNEAL_STEPS
        required_cards = [x for x in cards if x.name in required_card_names]
        super().__init__(required_cards + random.sample([x for x in cards if x.name not in required_card_names], N - len(required_cards)))

    def move(self) -> None:
        new_state = deepcopy(self.state)
        removed = random.choice([x for x in new_state if x.name not in required_card_names])
        new_state.remove(removed)
        new_state.append(random.choice([x for x in cards if x not in self.state]))
        self.state = new_state

    def energy(self) -> float:
        rating_score = mean(x.rating for x in self.state) / max_rating

        color_counts = {x: 0 for x in colors}
        for card in self.state:
            for color in card.colors:
                color_counts[color] += 1
        low_color_count = min(color_counts.values())
        high_color_count = max(color_counts.values())
        color_score = low_color_count / high_color_count

        return -(rating_score * color_score)


def main():
    optimal_cards, foo = Problem().anneal()
    optimal_cards = sorted(optimal_cards, key=lambda x: x.rating, reverse=True)
    for color in colors:
        color_cards = [x for x in optimal_cards if color in x.colors]
        print(f'\n{color} ({len(color_cards)})\n---------')
        for card in color_cards:
            print(f'{card.name} ({card.rating})')

    color_cards = [x for x in optimal_cards if not x.colors]
    print(f'\nColorless ({len(color_cards)})\n---------')
    for card in color_cards:
        print(f'{card.name} ({card.rating})')


if __name__ == '__main__':
    main()

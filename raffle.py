from argparse import ArgumentParser
from dataclasses import dataclass
from itertools import islice
import json
from pathlib import Path
from random import seed, shuffle
from time import sleep


def colored(text, *a, **kw):
    return text

try:
    import colorama
except ImportError: 
    pass
else:
    colorama.init()
    try:
        from termcolor import colored
    except ImportError:
        pass


def cprint(*args, sep=' ', end='\n', color=None, on_color=None, attrs=None, **kwargs) -> None:
    print(ctext(*args, sep=sep, end=end, color=color, on_color=on_color, attrs=attrs), end='', **kwargs)


def ctext(*args, sep=' ', end='', color=None, on_color=None, attrs=None) -> str:
    text = sep.join(map(str, args)) + end
    return colored(text, color=color, on_color=on_color, attrs=attrs)


@dataclass
class Data:
    scores: dict[str, int]
    prizes: list[str] | None = None

    @property
    def winner_count(self):
        return len(self.prizes)


def load_data(path):
    with path.open() as f:
        data = json.load(f)

    # for backwards compatibility
    if isinstance(data, dict) and all(isinstance(key, str) and isinstance(value, int) for key, value in data.items()):
        data = {"scores": data}

    return Data(**data)


def main():
    parser = ArgumentParser()

    parser.add_argument('data_source', type=Path)
    parser.add_argument('-w', '--winners', type=int, default=None)
    parser.add_argument('-d', '--duplicates-allowed', action='store_true')
    parser.add_argument('-p', '--pause', type=float, default=1)
    parser.add_argument('-btw', '--best-to-worst', action='store_true')

    args = parser.parse_args()

    data = load_data(args.data_source)

    if args.winners is not None:
        data.prizes = [None] * args.winners
    elif data.prizes is None:
        data.prizes = [None] * 3


    total_tickets = sum(data.scores.values())
    print(f"The total number of tickets is {total_tickets}.")
    print(f"There will be {data.winner_count} winner(s).")
    seed(total_tickets)

    assert data.prizes is not None

    if not args.duplicates_allowed and len(data.scores) < data.winner_count:
        raise RuntimeError("fewer candidates than winners")

    if total_tickets < data.winner_count:
        raise RuntimeError("fewer tickets than winners")

    def candidates():
        candidates = sorted(
            name for name, score in data.scores.items() for it in range(score)
        )
        shuffle(candidates)
        return candidates

    def winners():
        found = set()
        for candidate in candidates():
            if args.duplicates_allowed or candidate not in found:
                found.add(candidate)
                yield candidate

    winners = [*zip(winners(), reversed(data.prizes))]

    if args.best_to_worst:
        print('The ordering of winners is from best prize to worst prize.')
    else:
        print('The ordering of winners is from worst prize to best prize.')
        winners = [*reversed(winners)]

    print()

    for candidate, prize in winners:
        if prize is not None:
            print(end="The next prize is... ", flush=True)
            input()
            cprint(f"{prize}", color='blue')

        print(end="And the winner is..", flush=True)

        for it in range(3):
            sleep(args.pause)
            print(end='.', flush=True)
        input()
        cprint(f"{candidate}!", flush=True, color='green')
        input()

    print()
    print("Congratulations!")
    print()

if __name__ == '__main__':
    main()

from argparse import ArgumentParser
from itertools import islice
import json
from pathlib import Path
from random import seed, shuffle
from time import sleep

parser = ArgumentParser()

parser.add_argument('data_source', type=Path)
parser.add_argument('-w', '--winners', type=int, default=3)
parser.add_argument('-d', '--duplicates-allowed', action='store_true')
parser.add_argument('-btw', '--best-to-worst', action='store_true')

args = parser.parse_args()

with args.data_source.open() as f:
    data = json.load(f)

total_tickets = sum(data.values())
print(f"The total number of tickets is {total_tickets}.")
print(f"There will be {args.winners} winners.")
seed(total_tickets)

if not args.duplicates_allowed and len(data) < args.winners:
    raise RuntimeError("fewer candidates than winners")

if total_tickets < args.winners:
    raise RuntimeError("fewer tickets than winners")

def candidates():
    candidates = sorted(
        name for name, score in data.items() for it in range(score)
    )
    shuffle(candidates)
    return candidates

def winners():
    found = set()
    for candidate in candidates():
        if args.duplicates_allowed or candidate not in found:
            found.add(candidate)
            yield candidate

winners = [*islice(winners(), args.winners)]

if args.best_to_worst:
    print('The ordering is from best to worst.\n')
else:
    print('The ordering is from worst to best.\n')
    winners = [*reversed(winners)]

for candidate in winners:
    print(end="And the winner is..", flush=True)
    for it in range(3):
        sleep(1)
        print(end='.', flush=True)
    input()
    print(f"{candidate}!", flush=True)
    input()


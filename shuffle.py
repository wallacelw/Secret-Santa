from copy import deepcopy
from random import Random
from pprint import pprint

with open("list.txt", 'r') as f:
    members = [s.strip() for s in f.readlines()]

def generate(seed = None):
    if (seed == None):
        seed = Random().randint(1, 1_000)

    selected = deepcopy(members)
    Random(seed).shuffle(selected)

    bad = False
    for i, j in zip(members, selected):
        if (i == j):
            bad = True
            break

    if (bad):
        return generate()
    
    mapped = {}
    for i, j in zip(members, selected):
        mapped[i] = j

    return seed, mapped

seed, mapped = generate()
print(seed)
pprint(mapped)
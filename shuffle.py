from copy import deepcopy
from random import Random
from pprint import pprint

with open("list.txt", 'r') as f:
    members = [s.strip() for s in f.readlines()]

selected = deepcopy(members)

with open("seed.txt", 'r') as f:
    seed = f.read().strip()
    print(seed)

done = False

while(not done):
    tmp = Random().randint(1, 1_000)

    Random(tmp).shuffle(selected)

    done = True

    for i, j in zip(members, selected):
        if (i == j):
            done = False
            break
    
    if done:
        with open("good.txt", 'w') as f:
            f.write(str(tmp))

mapped = {}

for i, j in zip(members, selected):
    mapped[i] = j

pprint(mapped)
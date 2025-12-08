from functools import reduce
import math
import sys

distance = {}
nets = []
connected = set()

def get_distance(tup1, tup2):
    key = tup1 + tup2
    if key in distance:
        return distance[key]
    dist = sum([(tup1[i] - tup2[i]) ** 2 for i in range(3)])
    distance[key] = dist
    distance[tup2 + tup1] = dist

    return dist

def already_connected(tup1, tup2):
    return tup1 + tup2 in connected

def add_connection(tup1, tup2):
    print("adding connection", tup1, tup2)
    tup1net = [net for net in nets if tup1 in net]
    tup2net = [net for net in nets if tup2 in net]
    print(tup1net, tup2net)
    connected.add(tup1 + tup2)
    connected.add(tup2 + tup1)

    if tup1net:
        if tup2net:
            if tup1net == tup2net:
                print("Same net. Skipping")
                return
            # Combine
            print("COMBINING nets")
            nets.remove(tup1net[0])
            for x in tup1net[0]:
                tup2net[0].add(x)
        else:
            tup1net[0].add(tup2)
    elif tup2net:
        tup2net[0].add(tup1)
    else:
        nets.append({tup1, tup2})
    print('new nets')
    print(nets)


if __name__ == '__main__':
    print('running')

    lines = sys.stdin.readlines()
    tups = [ tuple(int(x) for x in l.split(",")) for l in lines]
    print(tups)

    for i in range(1000):
        closest = None

        for out_i, tup1 in enumerate(tups):
            for tup2 in (tups[out_i+1:]):
                if ((not closest or get_distance(tup1, tup2) < get_distance(*closest))) and not already_connected(tup1, tup2):
                    closest = [tup1, tup2]

        add_connection(*closest)

    sizes = sorted([len(x) for x in nets])
    print(sizes)
    print(sizes[-3:])

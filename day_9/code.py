from functools import reduce
import math
import sys

if __name__ == '__main__':
    print('running')

    coords = [tuple(int(x) for x in line.split(",")) for line in sys.stdin.readlines()]
    print(coords)

    largest = 0
    for i, x in enumerate(coords):
        for y in coords[i+1:]:
            area = (1+x[0]-y[0])*(1+x[1]-y[1])
            largest = max(area, largest)
    print(largest)

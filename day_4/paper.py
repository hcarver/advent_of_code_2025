import math
import sys

ADJACENCIES = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        ]

def num_adjacent_paper(grid, x, y):
    count = 0

    for (dx, dy) in ADJACENCIES:
        new_x = x + dx
        new_y = y + dy

        if new_x >= 0 and new_x < len(grid) and new_y >= 0 and new_y < len(grid[0]):
            if grid[new_x][new_y]:
                count += 1

    return count

def process(grid):
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y]:
                print('paper at ', x, y)
                adj = num_adjacent_paper(grid, x, y)
                print('adjacencies: ', adj)

                if adj < 4:
                    count += 1
    return count

def process_2(grid):
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y]:
                print('paper at ', x, y)
                adj = num_adjacent_paper(grid, x, y)
                print('adjacencies: ', adj)

                if adj < 4:
                    count += 1
                    grid[x][y] = False
    return count

if __name__ == '__main__':
    print('running')

    total = 0

    grid = [[y == '@' for y in x.strip()] for x in sys.stdin.readlines()]

    #result = process(grid)
    #print(result)

    count = 0

    while True:
        new_count = process_2(grid)
        print('found ', new_count)
        if new_count == 0:
            break
        count += new_count

    print(count)

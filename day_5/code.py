import math
import sys

range_list = []

def add_to_range_list(low, high):
    for r in range_list:
        if low > r[1] or high < r[0]:
            continue
        else:
            range_list.remove(r)
            add_to_range_list(min(low, r[0]), max(high, r[1]))
            return

    range_list.append((low, high))

if __name__ == '__main__':
    print('running')

    ranges = []
    found = False
    count = 0
    for x in sys.stdin.readlines():
        x = x.strip()

        if x == "":
            found = True
            continue
        if not found:
            new_range = [int(y) for y in x.split("-")]
            ranges.append(new_range)
            add_to_range_list(new_range[0], new_range[1])
        else:
            num = int(x)

            if any([num >= x and num <= y for (x,y) in ranges]):
                count += 1
    print(range_list)
    print(count)

    count2 = 0
    for r in range_list:
        count2 += 1 + r[1] - r[0]

    print(count2)

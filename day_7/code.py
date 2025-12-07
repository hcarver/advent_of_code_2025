from functools import reduce
import math
import sys

if __name__ == '__main__':
    print('running')

    lines = sys.stdin.readlines()
    current = [val == 'S' for val in lines[0].strip()]
    path_count = [int(val) for val in current]

    splits = 0
    for line in lines[1:]:
        new_current = [False for _ in range(len(line))]
        new_path_count = [0 for _ in range(len(line))]
        for i, val in enumerate(line):
            if val == 'S':
                new_current[i] = True
                new_path_count[i] = 1
            if val == '.' and current[i]:
                new_current[i] = True
                new_path_count[i] += path_count[i]
            if val == '^' and current[i]:
                splits += 1
                new_current[i-1] = True
                new_current[i+1] = True

                new_path_count[i-1] += path_count[i]
                new_path_count[i+1] += path_count[i]

        print(new_current)
        print(new_path_count)
        current = new_current
        path_count = new_path_count

    print(splits)
    print(sum(path_count))

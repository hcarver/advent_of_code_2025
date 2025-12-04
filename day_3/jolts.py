import math
import sys

def process(line):
    nums = [int(x) for x in line.strip()]

    print(nums, line)

    best = 0
    for i in range(len(nums) - 1):
        for j in range(i+1, len(nums)):
            val = 10*nums[i] + nums[j]
            best = max(best, val)

    print(best)

    return best

def argmax(some):
    best = 0
    for i, val in enumerate(some):
        if val > some[best]:
            best = i

    return best

def process_2(line):
    nums = [int(x) for x in line.strip()]

    last_i_taken = -1
    taken = []

    for digit in range(12):
        first_allowed = last_i_taken + 1
        last_allowed = len(nums) - (12 - digit)
        last_i_taken = first_allowed + argmax(nums[first_allowed : last_allowed + 1])

        taken.append(nums[last_i_taken])
        print(first_allowed, last_allowed, last_i_taken, taken)

    return int("".join(map(str,taken)))

if __name__ == '__main__':
    print('running')

    process_2('987654321111111')
    process_2('811111111111119')
    process_2('234234234234278')
    process_2('818181911112111')

    total = 0

    for l in sys.stdin.readlines():
        for r in l.split(','):
            total += process_2(r)

    print(total)

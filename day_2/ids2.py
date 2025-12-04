import math
import sys

def process_line(line):
    total = 0
    (low, high) = map(int, line.split('-'))

    print(line, low, high)

    for trial in range(low, high):
        as_str = str(trial)
        invalid = False

        for sublen in range(1, len(as_str) // 2 + 1):
            parts = [as_str[i:i + sublen] for i in range(0, len(as_str), sublen)]
            print('split into', parts)
            if(len(set(parts)) == 1):
                print('all parts the same, invalid')
                invalid = True
                break

        if invalid:
            total += trial
    print('line total', total)
    return total

if __name__ == '__main__':
    process_line('11-22')
    process_line('95-115')
    process_line('998-1012')
    process_line('1188511880-1188511890')
    process_line('222220-222224')
    process_line('1698522-1698528')
    process_line('446443-446449')
    process_line('38593856-38593862')
    process_line('565653-565659')
    process_line('824824821-824824827')
    process_line('2121212118-2121212124')

    print('running')

    total = 0

    for l in sys.stdin.readlines():
        for r in l.split(','):
            total += process_line(r)

    print(total)

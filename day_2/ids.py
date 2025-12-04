import math
import sys

if __name__ == '__main__':
    print('running')

    total = 0

    for l in sys.stdin.readlines():
        for r in l.split(','):
            (low, high) = map(int, r.split('-'))

            print(r, low, high)

            # First even power of 10 above the number
            power = math.ceil(math.log10(low))
            if power % 2 == 1:
                power += 1
            if power == 0:
                power = 2

            print('power', power)

            # Seek numbers of form 11, 101,
            factor = 10 ** (power // 2) + 1
            print('factor', factor)

            min_multiple = math.ceil(low / factor) * factor
            print('mm', min_multiple)

            while min_multiple >= low and min_multiple <= high:
                if math.floor(math.log10(min_multiple)) % 2 == 0:
                    print('ignoring for odd length', min_multiple)
                else:
                    print('happy with', min_multiple)
                    total += min_multiple
                min_multiple += factor

    print(total)

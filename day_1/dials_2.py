import sys

if __name__ == '__main__':
    print('running')

    dial = 50
    count = 0

    for l in sys.stdin.readlines():
        print(l.strip())
        number = int(l[1:])

        if l[0] == 'L':
            count += (((100 - dial) % 100) + number) // 100
            dial = (dial - number) % 100
        else:
            count += (dial + number) // 100
            dial = (dial + number) % 100


        print(dial)
        print(count)
        if dial < 0 or dial > 99:
            raise ValueError()

    print(count)

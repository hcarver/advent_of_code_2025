import sys

if __name__ == '__main__':
    print('running')

    dial = 50
    count = 0

    for l in sys.stdin.readlines():
        print(l)
        number = int(l[1:])

        if l[0] == 'L':
            dial = (100000 + dial - number) % 100
        else:
            dial = (dial + number) % 100


        print(dial)
        if dial == 0:
            count += 1

    print(count)

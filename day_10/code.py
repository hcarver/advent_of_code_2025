from functools import reduce
import math
import sys

def apply(state, button):
    return tuple(x ^ y for x,y in zip(state, button))

def handle(target, buttons):
    states = {tuple(False for x in target)}
    for i in range(1, 1000):
        new_states = {
                apply(state, button)
                for state in states
                for button in buttons
                }
        print(target)
        print(i, new_states)
        if target in new_states:
            return i
        states = new_states

if __name__ == '__main__':
    print('running')

    total = 0
    for line in sys.stdin.readlines():
        target = None
        buttons = []
        joltage = None
        for cpt in line.split():
            if cpt[0] == '[':
                target = tuple(char == '#' for char in cpt[1:-1])
            if cpt[0] == '(':
                changed = {int(x) for x in cpt[1:-1].split(",")}
                buttons.append(tuple(i in changed for i in range(len(target))))
        presses = handle(target, buttons)
        total += presses

        print(total)

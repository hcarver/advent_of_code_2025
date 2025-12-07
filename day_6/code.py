from functools import reduce
import math
import sys

def process_args(args):
    print("SECOND")
    print(args)
    total = 0
    is_last = False
    while not is_last:
        try:
            col_length = max([row.index(" ") for row in args])

            this_col = [row[0:col_length] for row in args]
            args = [row[col_length + 1:] for row in args]
        except ValueError:
            col_length = len(args[0]) - 1
            this_col = [row for row in args]
            is_last = True
        print(col_length)
        print(this_col)
        print(args)

        # read down columns
        arguments = []
        for i in range(col_length):
            argument = [rowlet[i] for rowlet in this_col[:-1]]
            argument = "".join(argument)
            argument = int(argument)
            arguments.append(argument)
        print(arguments)

        reducer = (lambda x,y: x*y) if "*" in this_col[-1] else lambda x,y: x+y
        result = reduce(reducer, arguments)
        print(result)
        total += result

    return total

if __name__ == '__main__':
    print('running')

    lines = []
    for x in sys.stdin.readlines():
        lines.append(x)

    total = 0
    total_2 = 0

    for i, op in enumerate(lines[-1].split()):
        print(i,op)

        reducer = (lambda x,y: x*y) if op == "*" else lambda x,y: x+y
        args_1 = [int(x.split()[i]) for x in lines[:-1]]
        print(args_1)
        result = reduce(reducer, args_1)
        print(result)
        total += result

    total_2 = process_args(lines)

    print(total)
    print(total_2)


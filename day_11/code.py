import sys

if __name__ == '__main__':
    print('running')

    lines = sys.stdin.readlines()
    fromtos = {}
    for line in lines:
        if not line.strip():
            continue
        print(line)
        source, nodes = line.split(":")
        fromtos[source.strip()] = nodes.strip().split()
    print(fromtos)

    paths_to_process = {('you',)}
    found_paths = set(('you',))

    while paths_to_process:
        current_stem = paths_to_process.pop()
        last = current_stem[-1]
        continuations = fromtos.get(last, [])

        for cont in continuations:
            full = current_stem + (cont,)
            if full in found_paths:
                continue

            paths_to_process.add(full)
            found_paths.add(full)
    print(found_paths)

    print(len([x for x in found_paths if x[-1] == 'out']))

from collections import defaultdict
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

    # From node -> {to node -> count}
    path_counts = defaultdict(lambda: defaultdict(lambda: 0))
    def add_path(frm, to):
        print("adding path", frm, "->", to)
        print("before ", path_counts)
        # New direct path
        path_counts[frm][to] += 1

        # Everywhere that goes to frm has new routes to reach everywhere that's reached by to
        new_adds = []
        for initial_source, destinations in path_counts.items():
            if frm not in destinations:
                continue
            for eventual_destination, route_count in path_counts.get(to, {}).items():
                new_adds.append((initial_source, eventual_destination, destinations[frm] * route_count))

            # Everywhere that can reach frm has new routes to to
            new_adds.append((initial_source, to, destinations[frm]))
        # Everywhere that can be reached from to has new routes from frm
        for ultimate, count in path_counts[to].items():
            new_adds.append((frm, ultimate, count))

        for (x,y,z) in new_adds:
            path_counts[x][y] += z
        print("after", path_counts)

    for frm, tos in fromtos.items():
        for to in tos:
            add_path(frm, to)

    # svr dac fft out
    order1 = path_counts['svr']['dac'] * path_counts['dac']['fft'] * path_counts['fft']['out']
    # svr fft dac out
    order2 = path_counts['svr']['fft'] * path_counts['fft']['dac'] * path_counts['dac']['out']
    print(order1, order2, order1 + order2)

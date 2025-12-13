from functools import reduce
import math
import sys

if __name__ == '__main__':
    print('running')

    # corner, corner, area
    possibles = []

    coords = [tuple(int(x) for x in line.split(",")) for line in sys.stdin.readlines()]

    for i, x in enumerate(coords):
        for y in coords[i+1:]:
            area = (1+abs(x[0]-y[0]))*(1+abs(x[1]-y[1]))
            possibles.append((x, y, area))

    # largest first
    possibles = sorted(possibles, key=lambda x: -x[2])
    print(possibles)
    line_segments = list(zip(coords, coords[1:] + [coords[0]]))
    print(line_segments)
    # horizontals and verticals
    h_segments = [x for x in line_segments if x[0][1] == x[1][1]]
    v_segments = [x for x in line_segments if x[0][0] == x[1][0]]

    # Check that we've got them all
    for x in line_segments:
        if x not in h_segments and x not in v_segments:
            raise ValueError(x)

    # Merge connected vertical segments at the same x-coordinate
    def merge_v_segments(segments):
        if not segments:
            return []

        # Group by x-coordinate
        by_x = {}
        for seg1, seg2 in segments:
            x = seg1[0]
            if x not in by_x:
                by_x[x] = []
            by_x[x].append((min(seg1[1], seg2[1]), max(seg1[1], seg2[1])))

        # Merge overlapping or adjacent ranges for each x
        merged = []
        for x, ranges in by_x.items():
            ranges = sorted(ranges)
            current_ranges = []
            for start, end in ranges:
                if current_ranges and start <= current_ranges[-1][1] + 1:
                    print("merging ", x, current_ranges[-1], (start, end))
                    # Merge with previous range
                    current_ranges[-1] = (current_ranges[-1][0], max(current_ranges[-1][1], end))
                else:
                    current_ranges.append((start, end))

            # Convert back to segment format
            for start, end in current_ranges:
                merged.append(((x, start), (x, end)))

        return merged

    v_segments = merge_v_segments(v_segments)

    # A dictionary of y co-ordinates to a list of tuple pairs.
    # The values in the pairs are ranges across that line where the (x1,x2) is all inside the shape.
    # Ranges are inclusive. Both end points are inside.
    inside_points_by_line = {}

    # Rely on v_segments remaining sorted by x to build that dictionary line-by-line
    v_segments = sorted(v_segments)
    def add_line_to_dictionary(y):
        xs = []
        inside = False
        on_hseg = None
        previous = None
        for seg1, seg2 in v_segments:
            if max(seg1[1], seg2[1]) == y:
                # Starting an h segment
                if on_hseg == None:
                    print("Starting hseg from bottom", seg1[0], inside)
                    on_hseg = "FROM BOTTOM"
                    if not inside:
                        xs.append(seg1[0])
                    previous = inside
                    inside = True
                # Otherwise we're finishing an h segment from the bottom.
                else:
                    # If we started from the bottom, our new inside-ness is the same as before
                    # If we started from the top, our new inside-ness should flip
                    new_inside = (on_hseg != "FROM BOTTOM") ^ previous
                    on_hseg = None
                    print("exiting hseg from bottom", seg1[0], new_inside)

                    if not new_inside:
                        xs.append(seg1[0])

                    inside = new_inside
            if min(seg1[1], seg2[1]) == y:
                # Starting an h segment
                if on_hseg == None:
                    print("Starting hseg from top", seg1[0], inside)
                    on_hseg = "FROM TOP"
                    if not inside:
                        xs.append(seg1[0])
                    previous = inside
                    inside = True
                # Otherwise we're finishing an h segment from the top.
                else:
                    # If we started from the top, our new inside-ness is the same as before
                    # If we started from the bottom, our new inside-ness should flip
                    new_inside = (on_hseg != "FROM TOP") ^ previous
                    on_hseg = None
                    print("exiting hseg from top", seg1[0], new_inside)

                    if not new_inside:
                        xs.append(seg1[0])

                    inside = new_inside
            elif min(seg1[1], seg2[1]) < y < max(seg1[1], seg2[1]):
                print("Crossing found", seg1, seg2)
                x = seg1[0]
                xs.append(x)
                inside = not inside
        xs = sorted(xs)

        if len(xs) % 2 != 0:
            raise ValueError("Expected even number of xs at ", y, xs)

        inside_ranges = list(zip(xs, xs[1:]))[::2]

        # split into adjacent pairs
        inside_points_by_line[y] = inside_ranges

    for y in range(max([x[1] for x in coords]) + 1):
        print("adding line ", y)
        add_line_to_dictionary(y)
        print(inside_points_by_line[y])

    def test_line(y, minX, maxX):
        for (rangeStart, rangeEnd) in inside_points_by_line[y]:
            if rangeStart <= minX and maxX <= rangeEnd:
                return True
        return False

    for (c1x, c1y), (c2x, c2y), area in possibles:
        print("trying shape", c1x, c1y, c2x, c2y, area)
        ok = True

        miny = min(c1y, c2y)
        maxy = max(c1y, c2y)
        minx = min(c1x, c2x)
        maxx = max(c1x, c2x)

        for y in range(miny, maxy + 1):
            if not test_line(y, minx, maxx):
                print("failed on line ", y)
                ok = False
                break
        if ok:
            print(c1x, c1y, c2x, c2y)
            print(area)
            break


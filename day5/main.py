from __future__ import annotations
from functools import reduce


INPUT_FILENAME = 'input.txt'


class Node:
    def __init__(
            self, 
            x_mid: int,
            intervals: list[tuple[int, int]],
            left: Node | None, 
            right: Node | None
        ):
        self.x_mid = x_mid
        self.intervals_by_start = sorted(intervals, key=lambda r: r[0])
        self.intervals_by_end = sorted(intervals, key=lambda r: -r[1])
        self.left = left
        self.right = right

    def __repr__(self):
        result = f'x_mid={self.x_mid}\nintervals={self.intervals_by_start}'
        result += '\nleft='
        if self.left:
            for line in str(self.left).split('\n'):
                result += '\n  ' + line
        else:
            result += 'None'
        result += '\nright='
        if self.right:
            for line in str(self.right).split('\n'):
                result += '\n  ' + line
        else:
            result += 'None'
        return result


def read_from_input() -> tuple[list[tuple[int, int]], list[int]]:
    input_file = open(INPUT_FILENAME, 'r')
    ranges = []
    queries = []

    is_reading_queries = False
    for line in input_file:
        row = line.strip()
        if row == '':
            is_reading_queries = True
            continue
        if is_reading_queries:
            queries.append(int(row))
        else:
            start, end = row.split('-')
            ranges.append((int(start), int(end)))
    return ranges, queries


def build_interval_tree(ranges: list[tuple[int, int]]) -> Node:
    if len(ranges) == 0:
        return None
    
    sorted_endpoints = sorted(reduce(lambda a, b: list(a) + list(b), ranges))
    x_mid = sorted_endpoints[(len(sorted_endpoints) - 1) // 2]

    # split ranges into three disjoint sets
    left_intervals = []
    right_intervals = []
    overlap = []
    for r in ranges:
        start, end = r
        if start <= x_mid <= end:
            overlap.append(r)
        elif x_mid < start:
            right_intervals.append(r)
        else:
            left_intervals.append(r)
    
    left_node = build_interval_tree(left_intervals)
    right_node = build_interval_tree(right_intervals)
    return Node(x_mid, overlap, left_node, right_node)


def search_interval_tree(tree: Node | None, query: int) -> list[tuple[int, int]]:
    if not tree:
        return []
    
    res = []
    if query == tree.x_mid:
        return tree.intervals_by_start  
    elif query < tree.x_mid:
        # all intervals in left must end after query,
        # so find intervals that start before query
        for r in tree.intervals_by_start:
            if r[0] <= query:
                res.append(r)
            else:
                break
        res += search_interval_tree(tree.left, query)
    else: # query > tree.x_mid
        # all intervals in right must start before query,
        # so find intervals that end after query
        for r in tree.intervals_by_end:
            if r[1] >= query:
                res.append(r)
            else:
                break
        res += search_interval_tree(tree.right, query)

    return res
        

def part_1(ranges: list[tuple[int, int]], queries: list[int]) -> int:
    interval_tree = build_interval_tree(ranges)
    count = 0
    for query in queries:
        if len(search_interval_tree(interval_tree, query)) > 0:
            count += 1
    return count


def merge_intervals(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    # merge all intervals
    # sort by start
    sorted_ranges = sorted(ranges)
    merged = []

    for curr_range in sorted_ranges:
        if not merged:
            merged.append(list(curr_range))
        last_range = merged[-1]
        # check for overlap
        if last_range[1] >= curr_range[0]:
            last_range[1] = max(last_range[1], curr_range[1])
        else:
            merged.append(list(curr_range))

    return merged


def part_2(ranges: list[tuple[int, int]]) -> int:
    merged = merge_intervals(ranges)
    # add up the lengths (inclusive)
    res = 0
    for start, end in merged:
        res += (end - start + 1)
    return res


def main():
    ranges, queries = read_from_input()
    print(f'part 1 result: {part_1(ranges, queries)}')
    print(f'part 2 result: {part_2(ranges)}')


if __name__ == "__main__":
    main()

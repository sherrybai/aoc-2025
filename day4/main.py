import collections


INPUT_FILENAME = 'input.txt'
ROLL = '@'
EMPTY = '.'

OFFSETS = [-1, 0, 1]

MAX_SURROUNDING_ROLLS = 4


def read_from_input() -> list[tuple[int, int]]:
    input_file = open(INPUT_FILENAME, 'r')
    result = []
    for line in input_file:
        row = list(line.strip())
        result.append(row)
    return result


def get_neighbors(pos: tuple[int, int], grid: list[list[str]], n: int, m: int):
    result = []
    x, y = pos
    for dx in OFFSETS:
        if not 0 <= (x + dx) < n:
            continue
        for dy in OFFSETS:
            if not 0 <= (y + dy) < m:
                continue

            neighbor = (x + dx, y + dy)
            if neighbor == pos:
                continue
            if grid[x + dx][y + dy] != ROLL:
                continue

            result.append(neighbor)
    return result


def can_be_removed(pos: tuple[int, int], grid: list[list[str]], n: int, m: int) -> bool:
    x, y = pos
    neighbors = get_neighbors((x, y), grid, n, m)
    num_surrounding_rolls = len(neighbors)
    return num_surrounding_rolls < MAX_SURROUNDING_ROLLS    


def find_removable_rolls(grid: list[list[str]], n: int, m: int) -> list[tuple[int, int]]:
    result = []
    for x in range(n):
        for y in range(m):
            if grid[x][y] != ROLL:
                continue

            if can_be_removed((x, y), grid, n, m):
                result.append((x, y))

    return result


def part_2(grid: list[list[str]], n: int, m: int) -> list[tuple[int, int]]:
    queue = collections.deque(find_removable_rolls(grid, n, m))
    visited = set()
    result = []
    while queue:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        result.append((x, y))

        # remove the roll
        grid[x][y] = EMPTY

        # check all the neighboring rolls and add to the queue
        for neighbor in get_neighbors((x, y), grid, n, m):
            if neighbor not in visited and can_be_removed(neighbor, grid, n, m):
                queue.append(neighbor)
        

    return result


def main():
    grid = read_from_input()
    n = len(grid)  # num rows
    m = len(grid[0]) if n > 0 else 0  # num columns

    print(f'part 1 result: {len(find_removable_rolls(grid, n, m))}')
    print(f'part 2 result: {len(part_2(grid, n, m))}')


if __name__ == "__main__":
    main()

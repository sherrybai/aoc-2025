import re
from typing import Generator

import numpy as np
import numpy.typing as npt


INPUT_FILENAME = 'input.txt'


def read_from_input_part_1() -> Generator[npt.NDArray[np.integer] | npt.NDArray[np.bool]]:
    # yield vector of numbers OR mask array
    input_file = open(INPUT_FILENAME, 'r')

    for line in input_file:
        row = line.strip().split()
        if row[0] == '*' or row[0] == '+':
            yield np.array(row) == '*'
        else:
            yield np.array([int(n) for n in row])


def read_from_input_part_2() -> tuple[npt.NDArray[np.str_], list[str]]:
    # yield character 2D matrix and list of operations
    input_file = open(INPUT_FILENAME, 'r')
    res = [list(line.strip('\n')) for line in input_file]
    return np.array(res[:-1]),  [c for c in res[-1] if c != ' ']


def part_1():
    multiply_vector = None
    add_vector = None
    mask = None
    for row in read_from_input_part_1():
        if row.dtype == np.bool:
            mask = row
            break
        if multiply_vector is None:  # first row
            multiply_vector = np.ones_like(row)
            add_vector = np.zeros_like(row)
        multiply_vector *= row
        add_vector += row
    
    return np.sum(multiply_vector[mask]) + np.sum(add_vector[~mask])


def part_2():
    matrix, ops = read_from_input_part_2()
    transposed = np.transpose(matrix)
    joined = [''.join(row).strip() for row in transposed.tolist()]

    op_idx = 0
    res = 1 if ops[op_idx] == '*' else 0
    total = 0
    for s in joined:
        if s == '':
            # add result to total
            total += res
            op_idx += 1
            res = 1 if ops[op_idx] == '*' else 0
            continue
        if ops[op_idx] == '*':
            res *= int(s)
        else:
            res += int(s)
    total += res
    return total


def main():
    print(f'part 1 result: {part_1()}')
    print(f'part 2 result: {part_2()}')


if __name__ == "__main__":
    main()

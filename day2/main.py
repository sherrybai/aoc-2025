import math


INPUT_FILENAME = 'input.txt'


def read_from_input() -> list[tuple[int, int]]:
    input_file = open(INPUT_FILENAME, 'r')
    input_string = input_file.readline().strip()
    range_strings = input_string.split(',')
    result = []
    for range_str in range_strings:
        range_as_list = range_str.split('-')
        range_as_tuple = (int(range_as_list[0]), int(range_as_list[1]))
        result.append(range_as_tuple)
    return result


def log_10(num: int) -> int:
    return int(math.log(num) // math.log(10))


def range_sum(start: int, end: int) -> int:
    return int((end - start + 1) * (start + end) / 2)


def prime_factors(num: int) -> list[int]:
    result = []
    factor = 2
    while factor ** 2 <= num:
        while num % factor == 0:
            if factor not in result:
                result.append(factor)
            num //= factor
        factor += 1
    if num > 1 and num not in result:
        result.append(num)
    return result


# sum all ids in range that satisfy number of digits and number of repeats
def add_ids_in_range_helper(
    start: int, 
    end: int, 
    start_digits: int,
    end_digits: int,
    num_digits: int, 
    num_repeats: int
) -> int:
    multiplicand_digits = num_digits // num_repeats
    multiplier = sum([10 ** (multiplicand_digits * i) for i in range(num_repeats)])

    if num_digits == start_digits:
        multiplicand_start = math.ceil(start / multiplier)
    else:
        multiplicand_start = 10 ** (multiplicand_digits - 1)
    
    if num_digits == end_digits:
        multiplicand_end = end // multiplier
    else:
        multiplicand_end = 10 ** multiplicand_digits - 1
    
    if multiplicand_start > multiplicand_end:
        return 0
    
    multiplicand = range_sum(multiplicand_start, multiplicand_end)
    return multiplicand * multiplier


def add_ids_in_range_part_1(start: int, end: int) -> int:
    start_digits = log_10(start) + 1
    end_digits = log_10(end) + 1

    result = 0
    for num_digits in range(start_digits, end_digits + 1):
        if num_digits % 2:
            # only consider even digits
            continue
        
        result += add_ids_in_range_helper(
            start=start,
            end=end,
            start_digits=start_digits,
            end_digits=end_digits,
            num_digits=num_digits,
            num_repeats=2,
        )
    
    return result


def add_ids_in_range_part_2(start: int, end: int) -> int:
    start_digits = log_10(start) + 1
    end_digits = log_10(end) + 1

    result = 0
    for num_digits in range(start_digits, end_digits + 1):
        if num_digits < 2:
            continue
        # get the prime factorization of num_digits
        factors = prime_factors(num_digits)
        for factor in factors:
            result += add_ids_in_range_helper(
                start=start,
                end=end,
                start_digits=start_digits,
                end_digits=end_digits,
                num_digits=num_digits,
                num_repeats=factor,
            )
        # could have double-counted
        # check any product of 2 prime factors < num_digits
        # (technically we should probably check any product of n prime factors, 
        # but no input value has 2 * 3 * 5 = 30 digits or more)
        for i in range(len(factors)):
            for j in range(i+1, len(factors)):
                if factors[i] * factors[j] > num_digits:
                    break
                factor = factors[i] * factors[j]
                result -= add_ids_in_range_helper(
                    start=start,
                    end=end,
                    start_digits=start_digits,
                    end_digits=end_digits,
                    num_digits=num_digits,
                    num_repeats=factor,
                )
    
    return result


def main():
    ranges = read_from_input()

    # this approach assumes all ranges are non-overlapping
    part_1_result = 0
    part_2_result = 0
    for start, end in ranges:
        part_1_result += add_ids_in_range_part_1(start, end)
        part_2_result += add_ids_in_range_part_2(start, end)
    print(f'part 1 result: {part_1_result}')
    print(f'part 2 result: {part_2_result}')


if __name__ == "__main__":
    main()

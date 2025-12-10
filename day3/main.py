INPUT_FILENAME = 'input.txt'


def read_from_input() -> list[str]:
    input_file = open(INPUT_FILENAME, 'r')
    return [line.strip() for line in input_file]


def get_largest_joltage(bank: str, num_batteries: int):
    selected_batteries = ''
    last_battery_idx = -1
    batteries_left = num_batteries
    while batteries_left > 0:
        batteries_left -= 1        
        start_index = last_battery_idx + 1
        # leave enough room for remaining batteries
        batteries_to_consider = bank[start_index : -batteries_left] if batteries_left else bank[start_index :]
        battery = max(batteries_to_consider)
        last_battery_idx = batteries_to_consider.index(battery) + start_index
        selected_batteries += battery

    return int(selected_batteries)


def part_1(banks: list[str]) -> int:
    result = 0
    for bank in banks:
        result += get_largest_joltage(bank, 2)
    return result


def part_2(banks: list[str]) -> int:
    result = 0
    for bank in banks:
        result += get_largest_joltage(bank, 12)
    return result


def main():
    banks = read_from_input()
    print(f'part 1 result: {part_1(banks)}')
    print(f'part 2 result: {part_2(banks)}')


if __name__ == "__main__":
    main()

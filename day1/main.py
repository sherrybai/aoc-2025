INPUT_FILENAME = 'input.txt'

LEFT = 'L'
RIGHT = 'R'

DIAL_SIZE = 100  # values 0 to 99

START_VALUE = 50

# rotation format: (direction, count)
def read_from_input() -> list[tuple[str, int]]:
    input_file = open(INPUT_FILENAME, 'r')
    rotation_list = []
    for line in input_file:
        rotation_str = line.strip()
        rotation = (rotation_str[0], int(rotation_str[1:]))
        rotation_list.append(rotation)
    return rotation_list


# return value: (dial_value, zero_count)
def turn_dial(curr_value: int, rotation: tuple[str, int]) -> tuple[int, int]:
    direction, count = rotation
    if direction == LEFT:
        # in python, modulo is guaranteed to be positive
        dial_value = (curr_value - count) % DIAL_SIZE

        # treat left rotations starting from 0 as starting from 100
        if curr_value == 0: curr_value = 100

        if (curr_value > count):
            zero_count = 0
        else:
            # already crossed boundary once from curr_value -> 0
            # remaining clicks from 0: count - curr_value
            # divide DIAL_SIZE for number of full rotations
            zero_count = 1 + (count - curr_value) // DIAL_SIZE

        return (dial_value, zero_count)
    
    if direction == RIGHT:
        dial_value = (curr_value + count) % DIAL_SIZE

        zero_count = (curr_value + count) // DIAL_SIZE

        return (dial_value, zero_count)
    
    raise TypeError('bad direction value: ${direction}')
        

def main():
    rotation_list = read_from_input()

    part_1_result = 0
    part_2_result = 0

    curr_value = START_VALUE
    for rotation in rotation_list:
        curr_value, zero_count = turn_dial(curr_value, rotation)

        assert(0 <= curr_value < DIAL_SIZE)
        
        if curr_value == 0:
            part_1_result += 1
        
        part_2_result += zero_count
    
    # print out final results
    print(f'part 1 password: {part_1_result}')
    print(f'part 2 password: {part_2_result}')


if __name__ == "__main__":
    main()

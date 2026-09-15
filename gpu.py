import cpu
import memory_bus

screen_width = 0x40
screen_height = 0x20
screen_matrix = [[0x00 for _ in range(screen_width)] for _ in range(screen_height)]

def screen_clear():
    for x in range(screen_height):
        for y in range(screen_width):
            screen_matrix[x][y] = 0x00

def draw(vx, vy, n):
    bit_switched = False

    for l in range(n):
        curr_i = cpu.cpu_I_register + l
        pixel = int.from_bytes(memory_bus.memory_read(curr_i), byteorder='big')
        for w in range(8):
            # if screen_matrix[vy + l][vx + w] != curr_i: bit_switched = True
            if (pixel & (0x80 >> w)) != 0: bit_switched = True
            if (curr_i > 0):
                screen_matrix[vy + l][vx + w] ^= 1
    cpu.cpu_data_registers[0x0f] =  1 if bit_switched else 0

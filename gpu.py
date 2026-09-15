import cpu

screen_width = 0x40
screen_height = 0x20
screen_matrix = [[0x00 for _ in range(screen_width)] for _ in range(screen_height)]

def screen_clear():
    for x in range(screen_height):
        for y in range(screen_width):
            screen_matrix[x][y] = 0x00

def draw(x, y, n):
    bit_switched = False
    vx = cpu.cpu_data_registers[x]
    vy = cpu.cpu_data_registers[y]

    for l in range(n):
        curr_i = cpu.cpu_I_register + l
        for w in range(8):
            if screen_matrix[vy + l][vx + w] != curr_i: bit_switched = True
            if (curr_i > 0):
                screen_matrix[vx + w][vy + l] = 1
    cpu.cpu_data_registers[0x0f] =  1 if bit_switched else 0

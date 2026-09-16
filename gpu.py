import pygame
import cpu
import memory_bus

screen_width = 0x40
screen_height = 0x20
screen_matrix = [[0x00 for _ in range(screen_width)] for _ in range(screen_height)]
screen_scale = 10
screen_pixel_rgb = (0, 125, 250)
screen = pygame.Surface

def initialize_gpu():
    global screen, screen_width, screen_height, screen_scale
    pygame.init()
    screen = pygame.display.set_mode((screen_width * screen_scale, screen_height * screen_scale))
    pygame.display.set_caption("Chippy")
    screen.fill((0, 0, 0))

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
            if (pixel & (0x80 >> w)) != 0: 
                screen_x = (vx + w) % screen_width
                screen_y = (vy + l) % screen_height
                bit_switched = True if screen_matrix[screen_y][screen_x] == 1 else 0
                screen_matrix[screen_y][screen_x] ^= 1

    cpu.cpu_data_registers[0x0f] =  1 if bit_switched else 0

    render_frame()

def screen_heartbeart():
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    except:
        exit()

def render_frame():
    global screen_matrix, screen_height, screen_width, screen, screen_scale
    for y in range(screen_height):
        for x in range(screen_width):
            if screen_matrix[y][x] >= 1:
                scale_tuple = (x * screen_scale, y * screen_scale, screen_scale, screen_scale)
                pygame.draw.rect(screen, screen_pixel_rgb, scale_tuple)
    pygame.display.flip()

import pygame
import cpu

keypad_input_matrix = [0x00 for _ in range(16)]

keypad_input_map = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}

keypad_input_target_vx = None

def capture_input():
    global keypad_input_target_vx
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in keypad_input_map:
                c8k = keypad_input_map[event.key]
                if keypad_input_matrix[c8k] == 0x01: continue
                keypad_input_matrix[c8k] = 0x01

                if cpu.cpu_await_keypress and keypad_input_target_vx != None:
                    cpu.cpu_data_registers[keypad_input_target_vx] = c8k
                    cpu.cpu_await_keypress = False   
                    keypad_input_target_vx = None

        elif event.type == pygame.KEYUP:
            if event.key in keypad_input_map:
                c8k = keypad_input_map[event.key]
                if keypad_input_matrix[c8k] == 0x00: continue
                keypad_input_matrix[c8k] = 0x00

        elif event.type == pygame.QUIT:
            exit()

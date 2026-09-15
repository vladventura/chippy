import time
import cpu
import memory_bus
import gpu

memory_bus.load_into_memory('./test_opcode.ch8')

# print(gpu.screen_matrix)

cpu.cpu_stack_pointer = 0x00
cpu.cpu_prog_counter = 0x200

ins_counter = 0

while cpu.run():
    print('Executed instruction {0}: {1} {2}'.format(
        ins_counter,
        cpu.cpu_ins_packet[1],
        cpu.cpu_ins_packet[0]
    ))
    ins_counter += 1
    if (ins_counter > 200): break

for x in range(gpu.screen_height):
    for y in range (gpu.screen_width):
        print(gpu.screen_matrix[x][y], end="")
    print()

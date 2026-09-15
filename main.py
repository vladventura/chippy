import cpu
import memory_bus
import gpu

memory_bus.load_into_memory('./test_opcode.ch8')

# print(gpu.screen_matrix)

cpu.cpu_stack_pointer = 0x00
cpu.cpu_prog_counter = 0x200

while cpu.run():
    print('Executed instruction')

# for x in range(gpu.screen_height):
#     for y in range (gpu.screen_width):
#         print(gpu.screen_matrix[x][y], end="")
#     print()

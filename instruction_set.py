import gpu
import cpu
import memory_bus

instructions_param = 0x000

def _00e0(): 
    gpu.screen_clear()

def _1nnn():
    cpu.cpu_prog_counter = instructions_param

def _2nnn():
    cpu.cpu_stack[cpu.cpu_stack_pointer] = cpu.cpu_prog_counter
    cpu.cpu_stack_pointer += 1
    cpu.cpu_prog_counter = instructions_param

def _3xnn():
    vx = (instructions_param & 0xf00) >> 8
    nn = (instructions_param & 0x0ff)
    if cpu.cpu_data_registers[vx] == nn:
        cpu.cpu_prog_counter += 2

def _4xnn():
    vx = (instructions_param & 0xf00) >> 8
    nn = instructions_param & 0x0ff
    if cpu.cpu_data_registers[vx] != nn:
        cpu.cpu_prog_counter += 2

def _5xy0():
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    if cpu.cpu_data_registers[vx] == cpu.cpu_data_registers[vy]:
        cpu.cpu_prog_counter += 2

def _6xnn():
    global instructions_param
    cpu.cpu_data_registers[(instructions_param & 0xf00) >> 2] = instructions_param & 0x0ff

def _7xnn():
    vx = (instructions_param & 0xf00) >> 8
    nn = instructions_param & 0x0ff
    cpu.cpu_data_registers[vx] += nn

def _9xy0():
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    if cpu.cpu_data_registers[vx] != cpu.cpu_data_registers[vy]:
        cpu.cpu_prog_counter += 2

def _annn():
    global instructions_param
    cpu.cpu_I_register = instructions_param

def _dxyn():
    global instructions_param
    x = (instructions_param & 0xf00) >> 8
    y = (instructions_param & 0x0f0) >> 4
    n = instructions_param & 0x00f
    gpu.draw(cpu.cpu_data_registers[x], cpu.cpu_data_registers[y], n)

"""
(Description, Opcode, Callback)
"""
instructions = {
    0x0: ('Execute Subroutine', '0NNN', None),
    0x00E0: ('Clear Screen', '00E0', _00e0),
    0x00EE: ('Return from Subroutine', '00EE', None),
    0x1000: ('Jump to Address', '1NNN', _1nnn),
    0x2000: ('Call subroutine at NNN', '2NNN', _2nnn),
    0x3000: ('Skip next if VX == NN', '3XNN', _3xnn),
    0x4000: ('Skip next if VX != NN', '4XNN', _4xnn),
    0x5000: ('Skip if VX == VY', '5XY0', _5xy0),
    0x6000: ('Set VX to NN', '6XNN', _6xnn),
    0x7000: ('Add NN to VX (no carry)', '7XNN', _7xnn),
    0x9000: ('Skip if VX != VY', '9XY0', _9xy0),
    0xA000: ('Set I register', 'ANNN', _annn),
    0xD000: ('Draw N-height at VXVY', 'DXYN', _dxyn)
}

def get_instruction(ins: bytes):
    global instructions_param
    opcode = int.from_bytes(ins, byteorder='big')
    instructions_param = 0x000
    if opcode & 0xf000 == 0x0000:
        if opcode == 0x00E0:
            return instructions[0x00E0]
        if opcode == 0x00EE:
            return instructions[0x00EE]
        return instructions[0x0000]
    
    if opcode & 0xf000 in instructions:
        instructions_param = (opcode & 0x0fff)
        return instructions[opcode & 0xf000]

    return ('Opcode not found', ins.hex(), None)

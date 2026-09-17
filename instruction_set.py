import helpers
import gpu
import cpu
import memory_bus
import keypad_input
import timer

instructions_param = 0x000

def _00e0(): 
    gpu.screen_clear()

def _00ee():
    cpu.cpu_stack_pointer -= 1
    cpu.cpu_prog_counter = cpu.cpu_stack[cpu.cpu_stack_pointer]
    cpu.cpu_stack[cpu.cpu_stack_pointer] = 0x000

def _1nnn():
    global instructions_param
    # print("InsParam on 1nnn ", hex(instructions_param))
    cpu.cpu_prog_counter = instructions_param
    cpu.cpu_flow_flag = True

def _2nnn():
    global instructions_param
    cpu.cpu_stack[cpu.cpu_stack_pointer] = cpu.cpu_prog_counter
    cpu.cpu_stack_pointer += 1
    cpu.cpu_stack_pointer &= 0xff
    cpu.cpu_prog_counter = instructions_param
    cpu.cpu_flow_flag = True

def _3xnn():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    nn = (instructions_param & 0x0ff)
    if cpu.cpu_data_registers[vx] == nn:
        cpu.cpu_prog_counter += 2

def _4xnn():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    nn = instructions_param & 0x0ff
    if cpu.cpu_data_registers[vx] != nn:
        cpu.cpu_prog_counter += 2

def _5xy0():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    if cpu.cpu_data_registers[vx] == cpu.cpu_data_registers[vy]:
        cpu.cpu_prog_counter += 2
        cpu.cpu_prog_counter &= 0xfff

def _6xnn():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    nn = instructions_param & 0x0ff
    cpu.cpu_data_registers[vx] = nn 
    cpu.cpu_data_registers[vx] &= 0xff

def _7xnn():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    nn = instructions_param & 0x0ff
    cpu.cpu_data_registers[vx] = (cpu.cpu_data_registers[vx] + nn)
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy0():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] = cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy1():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] |= cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy2():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] &= cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy3():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] ^= cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy4():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    has_carry = vx + vy > 0xff 
    cpu.cpu_data_registers[0x0F] = 1 if has_carry else 0

    cpu.cpu_data_registers[vx] += cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy5():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    has_borrow = cpu.cpu_data_registers[vx] < cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[0x0F] = 0 if has_borrow else 1
    cpu.cpu_data_registers[vx] -= cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy6():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] = cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] >>= 1
    cpu.cpu_data_registers[vx] &= 0xff

def _8xy7():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    has_borrow = cpu.cpu_data_registers[vy] < cpu.cpu_data_registers[vx]
    cpu.cpu_data_registers[0x0F] = 0 if has_borrow else 1
    cpu.cpu_data_registers[vx] = cpu.cpu_data_registers[vy] - cpu.cpu_data_registers[vx]
    cpu.cpu_data_registers[vx] &= 0xff

def _8xye():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    cpu.cpu_data_registers[vx] = cpu.cpu_data_registers[vy]
    cpu.cpu_data_registers[vx] <<= 1
    cpu.cpu_data_registers[vx] &= 0xff

def _9xy0():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    vy = (instructions_param & 0x0f0) >> 4
    if cpu.cpu_data_registers[vx] != cpu.cpu_data_registers[vy]:
        cpu.cpu_prog_counter += 2
        cpu.cpu_prog_counter &= 0xfff

def _annn():
    global instructions_param
    cpu.cpu_I_register = instructions_param
    cpu.cpu_I_register &= 0xffff

def _dxyn():
    global instructions_param
    x = (instructions_param & 0xf00) >> 8
    y = (instructions_param & 0x0f0) >> 4
    n = instructions_param & 0x00f
    gpu.draw(cpu.cpu_data_registers[x], cpu.cpu_data_registers[y], n)

def _fx07():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    cpu.cpu_data_registers[vx] = timer.timer_delay

def _fx0a():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    keypad_input.keypad_input_target_vx = vx
    cpu.cpu_await_keypress = True

def _fx15():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    timer.timer_delay = cpu.cpu_data_registers[vx]

def _fx29():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    cpu.cpu_I_register = cpu.cpu_data_registers[vx] * 5 # ?
    cpu.cpu_I_register &= 0xffff

def _fx33():
    global instructions_param
    vx = (instructions_param & 0xf00) >> 8
    bcd = helpers.to_bcd(cpu.cpu_data_registers[vx])
    for offset in range(3):
        addr = cpu.cpu_I_register + offset
        val = (bcd >> (8 - (4 * offset))) & 0x00f
        memory_bus.memory_write(addr, val)

def _fx55():
    global instructions_param
    vx_max = ((instructions_param & 0xf00) >> 8) + 1
    for vx in range(vx_max):
        offset = cpu.cpu_I_register + vx
        memory_bus.memory_write(offset, cpu.cpu_data_registers[vx])
    cpu.cpu_I_register += vx_max

def _fx65():
    global instructions_param
    vx_max = ((instructions_param & 0xf00) >> 8) + 1
    for vx in range(vx_max):
        offset = cpu.cpu_I_register + vx
        cpu.cpu_data_registers[vx] = memory_bus.memory_read(offset)
    cpu.cpu_I_register += vx_max & 0xffff

"""
(Description, Opcode, Callback)
"""
instructions = {
    0x0000: ('Execute Subroutine',                              '0NNN', _1nnn),
    0x00E0: ('Clear Screen',                                    '00E0', _00e0),
    0x00EE: ('Return from Subroutine',                          '00EE', _00ee),
    0x1000: ('Jump to Address',                                 '1NNN', _1nnn),
    0x2000: ('Call subroutine at NNN',                          '2NNN', _2nnn),
    0x3000: ('Skip next if VX == NN',                           '3XNN', _3xnn),
    0x4000: ('Skip next if VX != NN',                           '4XNN', _4xnn),
    0x5000: ('Skip if VX == VY',                                '5XY0', _5xy0),
    0x6000: ('Set VX to NN',                                    '6XNN', _6xnn),
    0x7000: ('Add NN to VX (no carry)',                         '7XNN', _7xnn),
    0x8000: ('Set VX = VY',                                     '8XY0', _8xy0),
    0x8001: ('Set VX |= VY',                                    '8XY1', _8xy1),
    0x8002: ('Set VX &= VY',                                    '8XY2', _8xy2),
    0x8003: ('Set VX ^= VY',                                    '8XY3', _8xy3),
    0x8004: ('Set VX += VY',                                    '8XY4', _8xy4),
    0x8005: ('Set VX -= VY',                                    '8XY5', _8xy5),
    0x8006: ('Set VX = VY >> 1',                                '8XY6', _8xy6),
    0x8007: ('Set VX = VY - VX',                                '8XY7', _8xy7),
    0x800E: ('Set VX = VY << 1',                                '8XYE', _8xye),
    0x9000: ('Skip if VX != VY',                                '9XY0', _9xy0),
    0xA000: ('Set I register',                                  'ANNN', _annn),
    0xB000: ('Jump to NNN + V0',                                'BNNN', None),
    0xC000: ('Set VX = rand() & NN',                            'CXNN', None),
    0xD000: ('Draw N-height at VXVY',                           'DXYN', _dxyn),
    0xE09E: ('Skip next if hex key value in VX is pressed',     'EX9E', None),
    0xE0A1: ('Skip next if hex key value in VX is not pressed', 'EXA1', None),
    0xF007: ('Set VX = delay timer',                            'FX07', _fx07),
    0xF00A: ('Wait for a keypress, store on VX',                'FX0A', _fx0a),
    0xF015: ('Set delay timer = VX',                            'FX15', _fx15),
    0xF018: ('Set sound timer = VX',                            'FX18', None),
    0xF01E: ('Set I += VX',                                     'FX1E', None),
    0xF029: ('Set I to sprite on hex value in VX',              'FX29', _fx29),
    0xF033: ('Set BCD of VX into addresses I, I + 1, I + 2',    'FX33', _fx33),
    0xF055: ('Set [V0, VX] into addresses [I, I + X]',          'FX55', _fx55),
    0xF065: ('Set addresses [I, I + X] into [V0, VX]',          'FX65', _fx65),
}

def get_instruction(ins: int):
    global instructions_param
    opcode = ins
    instructions_param = 0x000
    if opcode & 0xf000 == 0x0000:
        if opcode == 0x00E0:
            return instructions[0x00E0]
        if opcode == 0x00EE:
            return instructions[0x00EE]
        return instructions[0x0000]
    
    if opcode & 0xf000 in instructions:
        if opcode & 0xf00f in instructions:
            instructions_param = (opcode & 0x0ff0)
            return instructions[opcode & 0xf00f]

        instructions_param = (opcode & 0x0fff)
        return instructions[opcode & 0xf000]
    
    if opcode & 0xf0ff in instructions:
        instructions_param = (opcode & 0x0f00)
        return instructions[opcode & 0xf0ff]

    return ('Opcode not found', ins.hex(), None)

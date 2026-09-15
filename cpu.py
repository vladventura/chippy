import memory_bus
import instruction_set

cpu_data_registers = {
    0x00: 0x00,
    0x01: 0x00,
    0x02: 0x00,
    0x03: 0x00,
    0x04: 0x00,
    0x05: 0x00,
    0x06: 0x00,
    0x07: 0x00,
    0x08: 0x00,
    0x09: 0x00,
    0x0a: 0x00,
    0x0b: 0x00,
    0x0c: 0x00,
    0x0d: 0x00,
    0x0e: 0x00,
    0x0f: 0x00,
}

cpu_I_register = 0x0000
cpu_prog_counter = 0x000
cpu_stack = [0x000 for _ in range(0x10)]
cpu_stack_pointer = 0
cpu_current_ins = None
cpu_ins_packet = None
cpu_flow_flag = False

def fetch():
    global cpu_ins_packet, cpu_prog_counter, cpu_current_ins
    ins_hi = memory_bus.memory_read(cpu_prog_counter)
    ins_lo = memory_bus.memory_read(cpu_prog_counter + 1)
    res = ins_hi + ins_lo
    cpu_ins_packet = instruction_set.get_instruction(res)
    cpu_current_ins = cpu_ins_packet[2]

def execute() -> bool:
    global cpu_flow_flag, cpu_prog_counter,  cpu_current_ins
    if cpu_current_ins == None:
        print('Not implemented yet (0x{0}): {1}'.format(cpu_ins_packet[1], cpu_ins_packet[0]))
        return False
    print("PC ", cpu_prog_counter)
    cpu_current_ins()
    if not cpu_flow_flag:
        cpu_prog_counter += 2
    else:
        cpu_flow_flag = False
    return True

def run() -> bool:
    fetch()
    return execute()

memory = [0x00 for _ in range(4096)]

def load_into_memory(prog):
    chunks = []
    with open(prog, 'rb') as binf:
        while True:
            chunk = binf.read(1)
            if not chunk: break
            if len(chunk) == 1:
                chunks.append(chunk)
    counter = 0x200
    for chunk in chunks:
        memory[counter] = chunk
        counter += 1

def memory_read(addr) -> bytes:
    return memory[addr]

def memory_write(addr, val):
    memory[addr] = val

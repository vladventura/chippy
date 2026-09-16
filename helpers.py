def to_bcd(n):
    acc = 0x000
    if (n > 0): acc = int(str(n), base=16)
    return acc

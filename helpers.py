"""
Int to BCD: Adjusted code from divyeshrabadiya07
https://www.geeksforgeeks.org/dsa/convert-a-given-decimal-number-to-its-bcd-representation/
"""
def to_bcd(n) : 
    acc = 0x000
    if (n > 0): 
        rev = 0
        while (n > 0) : 
            rev = rev * 10 + (n % 10)
            n = n // 10
        offset = 0
        while (rev > 0) : 
            b = rev % 10
            acc |= (b << (4 * offset))
            rev = rev // 10
    return acc
    
# mini_aes.py

SBOX = [
    0x9, 0x4, 0xA, 0xB,
    0xD, 0x1, 0x8, 0x5,
    0x6, 0x2, 0x0, 0x3,
    0xC, 0xE, 0xF, 0x7
]

INV_SBOX = [SBOX.index(x) for x in range(16)]

def gf_mult(a, b):
    p = 0
    for i in range(4):
        if b & 1:
            p ^= a
        carry = a & 0x8
        a <<= 1
        if carry:
            a ^= 0b10011  # irreducible polynomial x^4 + x + 1
        a &= 0xF
        b >>= 1
    return p

def sub_nibbles(block):
    return ((SBOX[(block >> 12) & 0xF] << 12) |
            (SBOX[(block >> 8) & 0xF] << 8) |
            (SBOX[(block >> 4) & 0xF] << 4) |
            (SBOX[block & 0xF]))

def inv_sub_nibbles(block):
    return ((INV_SBOX[(block >> 12) & 0xF] << 12) |
            (INV_SBOX[(block >> 8) & 0xF] << 8) |
            (INV_SBOX[(block >> 4) & 0xF] << 4) |
            (INV_SBOX[block & 0xF]))

def shift_rows(block):
    n0 = (block >> 12) & 0xF
    n1 = (block >> 8) & 0xF
    n2 = (block >> 4) & 0xF
    n3 = block & 0xF
    return (n0 << 12) | (n1 << 8) | (n3 << 4) | n2  # Corrected shift

def inv_shift_rows(block):
    n0 = (block >> 12) & 0xF
    n1 = (block >> 8) & 0xF
    n2 = (block >> 4) & 0xF
    n3 = block & 0xF
    return (n0 << 12) | (n1 << 8) | (n3 << 4) | n2  # Corrected inverse shift

def mix_columns(block):
    n0 = (block >> 12) & 0xF
    n1 = (block >> 8) & 0xF
    n2 = (block >> 4) & 0xF
    n3 = block & 0xF

    m0 = gf_mult(n0, 1) ^ gf_mult(n2, 4)
    m1 = gf_mult(n0, 4) ^ gf_mult(n2, 1)
    m2 = gf_mult(n1, 1) ^ gf_mult(n3, 4)
    m3 = gf_mult(n1, 4) ^ gf_mult(n3, 1)

    return (m0 << 12) | (m1 << 8) | (m2 << 4) | m3

def inv_mix_columns(block):
    n0 = (block >> 12) & 0xF
    n1 = (block >> 8) & 0xF
    n2 = (block >> 4) & 0xF
    n3 = block & 0xF

    m0 = gf_mult(n0, 9) ^ gf_mult(n1, 2)
    m1 = gf_mult(n0, 2) ^ gf_mult(n1, 9)
    m2 = gf_mult(n2, 9) ^ gf_mult(n3, 2)
    m3 = gf_mult(n2, 2) ^ gf_mult(n3, 9)

    return (m0 << 12) | (m1 << 8) | (m2 << 4) | m3

def add_round_key(block, key):
    return block ^ key

def key_expansion(key):
    w = [0] * 6
    w[0] = (key >> 8) & 0xFF
    w[1] = key & 0xFF
    w[2] = w[0] ^ 0b10000000 ^ ((SBOX[w[1] >> 4] << 4) | SBOX[w[1] & 0x0F])
    w[3] = w[2] ^ w[1]
    w[4] = w[2] ^ 0b00110000 ^ ((SBOX[w[3] >> 4] << 4) | SBOX[w[3] & 0x0F])
    w[5] = w[4] ^ w[3]

    round_keys = [
        (w[0] << 8) | w[1],
        (w[2] << 8) | w[3],
        (w[4] << 8) | w[5],
    ]
    return round_keys

def mini_aes_encrypt(plaintext, key):
    round_keys = key_expansion(key)

    state = add_round_key(plaintext, round_keys[0])
    print(f"Round 0: {state:04x}")
    state = sub_nibbles(state)
    print(f"Round 1: SubNibbles: {state:04x}")
    state = shift_rows(state)
    print(f"Round 2: ShiftRows: {state:04x}")
    state = mix_columns(state)
    print(f"Round 3: MixColumns: {state:04x}")
    state = add_round_key(state, round_keys[1])
    print(f"Round 4: AddRoundKey: {state:04x}")
    state = sub_nibbles(state)
    print(f"Round 5: SubNibbles: {state:04x}")
    state = shift_rows(state)
    print(f"Round 6: ShiftRows: {state:04x}")
    state = add_round_key(state, round_keys[2])
    print(f"Round 7: AddRoundKey: {state:04x}")

    return state

def mini_aes_decrypt(ciphertext, key):
    round_keys = key_expansion(key)

    state = add_round_key(ciphertext, round_keys[2])
    print(f"Round 0: {state:04x}")
    state = inv_shift_rows(state)
    print(f"Round 1: InvShiftRows: {state:04x}")
    state = inv_sub_nibbles(state)
    print(f"Round 2: InvSubNibbles: {state:04x}")
    state = add_round_key(state, round_keys[1])
    print(f"Round 3: AddRoundKey: {state:04x}")
    state = inv_mix_columns(state)
    print(f"Round 4: InvMixColumns: {state:04x}")
    state = inv_shift_rows(state)
    print(f"Round 5: InvShiftRows: {state:04x}")
    state = inv_sub_nibbles(state)
    print(f"Round 6: InvSubNibbles: {state:04x}")
    state = add_round_key(state, round_keys[0])
    print(f"Round 7: AddRoundKey: {state:04x}")

    return state

def encrypt_ecb(plaintext_blocks, key):
    return [mini_aes_encrypt(block, key) for block in plaintext_blocks]

def decrypt_ecb(ciphertext_blocks, key):
    return [mini_aes_decrypt(block, key) for block in ciphertext_blocks]

def encrypt_cbc(plaintext_blocks, key, iv):
    ciphertext_blocks = []
    prev = iv
    for block in plaintext_blocks:
        enc = mini_aes_encrypt(block ^ prev, key)
        ciphertext_blocks.append(enc)
        prev = enc
    return ciphertext_blocks

def decrypt_cbc(ciphertext_blocks, key, iv):
    plaintext_blocks = []
    prev = iv
    for block in ciphertext_blocks:
        dec = mini_aes_decrypt(block, key) ^ prev
        plaintext_blocks.append(dec)
        prev = block
    return plaintext_blocks

def avalanche_effect(plaintext, key):
    cipher1 = mini_aes_encrypt(plaintext, key)
    cipher2 = mini_aes_encrypt(plaintext ^ (1 << 0), key)  # flip 1 bit
    diff = cipher1 ^ cipher2
    return bin(diff).count('1')

def save_to_file(filename, blocks):
    with open(filename, 'w') as f:
        for block in blocks:
            f.write(f"{block:04x}\n")

def load_from_file(filename):
    blocks = []
    with open(filename, 'r') as f:
        for line in f:
            blocks.append(int(line.strip(), 16))
    return blocks

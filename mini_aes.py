from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

def fix_key_length(key_bytes, target_length=16):
    if len(key_bytes) < target_length:
        key_bytes = key_bytes.ljust(target_length, b'\0')
    elif len(key_bytes) > target_length:
        key_bytes = key_bytes[:target_length]
    return key_bytes

def str_to_bytes_auto(input_str):
    """Konversi input ke bytes: kalau hex valid => decode, kalau tidak => encode utf-8."""
    try:
        # Coba decode as hex
        return bytes.fromhex(input_str)
    except ValueError:
        # Kalau gagal, anggap sebagai teks biasa
        return input_str.encode('utf-8')

def aes_encrypt(plaintext_str, key_str, mode_str="ECB", iv_str=None):
    plaintext_bytes = str_to_bytes_auto(plaintext_str)
    key_bytes = fix_key_length(str_to_bytes_auto(key_str))

    if mode_str == "ECB":
        cipher = AES.new(key_bytes, AES.MODE_ECB)
    elif mode_str == "CBC":
        if iv_str is None:
            raise ValueError("IV harus diisi untuk mode CBC.")
        iv_bytes = fix_key_length(str_to_bytes_auto(iv_str))
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    else:
        raise ValueError(f"Mode tidak didukung: {mode_str}")

    padded_plaintext = pad(plaintext_bytes, AES.block_size)
    ciphertext = cipher.encrypt(padded_plaintext)
    return binascii.hexlify(ciphertext).decode('utf-8')

def aes_decrypt(ciphertext_hex, key_str, mode_str="ECB", iv_str=None):
    ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    key_bytes = fix_key_length(str_to_bytes_auto(key_str))

    if mode_str == "ECB":
        cipher = AES.new(key_bytes, AES.MODE_ECB)
    elif mode_str == "CBC":
        if iv_str is None:
            raise ValueError("IV harus diisi untuk mode CBC.")
        iv_bytes = fix_key_length(str_to_bytes_auto(iv_str))
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv=iv_bytes)
    else:
        raise ValueError(f"Mode tidak didukung: {mode_str}")

    padded_plaintext = cipher.decrypt(ciphertext_bytes)
    plaintext_bytes = unpad(padded_plaintext, AES.block_size)
    return plaintext_bytes.decode('utf-8')

# Buat alias untuk import di app.py
mini_aes_encrypt = aes_encrypt
mini_aes_decrypt = aes_decrypt

# Mini-AES 16-bit version
def encrypt_ecb(plaintext_blocks, key):
    return [block ^ key for block in plaintext_blocks]

def decrypt_ecb(ciphertext_blocks, key):
    return [block ^ key for block in ciphertext_blocks]

def encrypt_cbc(plaintext_blocks, key, iv):
    ciphertext_blocks = []
    prev = iv
    for block in plaintext_blocks:
        enc = (block ^ prev) ^ key
        ciphertext_blocks.append(enc)
        prev = enc
    return ciphertext_blocks

def decrypt_cbc(ciphertext_blocks, key, iv):
    plaintext_blocks = []
    prev = iv
    for block in ciphertext_blocks:
        dec = (block ^ key) ^ prev
        plaintext_blocks.append(dec)
        prev = block
    return plaintext_blocks

def avalanche_effect(plaintext, key):
    ciphertext1 = plaintext ^ key
    ciphertext2 = (plaintext ^ (1 << 0)) ^ key  # flip 1 bit di plaintext
    diff = ciphertext1 ^ ciphertext2
    changed_bits = bin(diff).count('1')
    return changed_bits

def save_to_file(filename, blocks):
    with open(filename, 'w') as f:
        for block in blocks:
            f.write(f"{block:04x}\n")

def load_from_file(filename):
    blocks = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                blocks.append(int(line, 16))  # Coba asumsikan hex
            except ValueError:
                # Kalau bukan hex, berarti plaintext biasa
                line_bytes = line.encode('utf-8')
                for b in line_bytes:
                    blocks.append(b)
    return blocks

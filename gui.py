import streamlit as st
from mini_aes import (
    mini_aes_encrypt, mini_aes_decrypt,
    encrypt_ecb, decrypt_ecb,
    encrypt_cbc, decrypt_cbc,
    avalanche_effect, save_to_file, load_from_file
)

def to_hex_if_needed(s):
    try:
        int(s, 16)
        return s.lower()
    except ValueError:
        return s.encode('utf-8').hex()

def hex_to_text_safe(hex_str):
    """Coba konversi hex ke teks utf-8, kalau gagal return None."""
    try:
        return bytes.fromhex(hex_str).decode('utf-8')
    except Exception:
        return None

st.title("Mini-AES 16-bit Encryption Tool 🔒")

menu = st.sidebar.selectbox("Menu", ["Encrypt/Decrypt", "Avalanche Effect Test", "File Operations"])

if menu == "Encrypt/Decrypt":
    st.header("Mini AES Encrypt / Decrypt")

    plaintext_input = st.text_input("Plaintext (Teks biasa atau Hex)").strip()
    key_input = st.text_input("Key (Teks biasa atau Hex)").strip()
    mode = st.selectbox("Mode Operasi", ["ECB", "CBC"])
    iv_input = st.text_input("Initialization Vector (IV) untuk CBC", value="0000").strip()

    if st.button("Encrypt"):
        try:
            plaintext_hex = to_hex_if_needed(plaintext_input)
            key_hex = to_hex_if_needed(key_input)
            iv_hex = to_hex_if_needed(iv_input)

            key = int(key_hex, 16)
            iv = int(iv_hex, 16)
            plaintext_blocks = [int(plaintext_hex[i:i+4], 16) for i in range(0, len(plaintext_hex), 4)]

            if mode == "ECB":
                ciphertext_blocks = encrypt_ecb(plaintext_blocks, key)
            else:
                ciphertext_blocks = encrypt_cbc(plaintext_blocks, key, iv)

            result = ''.join(hex(block)[2:].zfill(4) for block in ciphertext_blocks)
            st.success(f"Ciphertext (hex): {result}")

            st.session_state['ciphertext_blocks'] = ciphertext_blocks
            st.session_state['key'] = key
            st.session_state['iv'] = iv
            st.session_state['mode'] = mode

        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Decrypt"):
        try:
            if 'ciphertext_blocks' not in st.session_state:
                st.warning("Lakukan enkripsi dulu.")
            else:
                if st.session_state['mode'] == "ECB":
                    decrypted_blocks = decrypt_ecb(st.session_state['ciphertext_blocks'], st.session_state['key'])
                else:
                    decrypted_blocks = decrypt_cbc(st.session_state['ciphertext_blocks'], st.session_state['key'], st.session_state['iv'])

                decrypted_hex = ''.join(hex(block)[2:].zfill(4) for block in decrypted_blocks)
                st.success(f"Decrypted (hex): {decrypted_hex}")

                decrypted_text = hex_to_text_safe(decrypted_hex)
                if decrypted_text is not None:
                    st.info(f"Decrypted (text): {decrypted_text}")
                else:
                    st.warning("Hasil dekripsi tidak bisa dikonversi ke teks utf-8 yang valid.")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "Avalanche Effect Test":
    st.header("Avalanche Effect Test")

    plaintext_input = st.text_input("Plaintext (Teks biasa atau Hex)", key="plaintext_avalanche").strip()
    key_input = st.text_input("Key (Teks biasa atau Hex)", key="key_avalanche").strip()

    if st.button("Test Avalanche"):
        try:
            plaintext_hex = to_hex_if_needed(plaintext_input)
            key_hex = to_hex_if_needed(key_input)

            plaintext = int(plaintext_hex, 16)
            key = int(key_hex, 16)

            changed_bits = avalanche_effect(plaintext, key)
            st.success(f"Perubahan bit: {changed_bits} dari 16 bit")
        except Exception as e:
            st.error(f"Error: {e}")

elif menu == "File Operations":
    st.header("File Operations")

    uploaded_file = st.file_uploader("Upload file (format txt)", type=['txt'])

    if uploaded_file:
        with open("uploaded.txt", "wb") as f:
            f.write(uploaded_file.read())

        plaintext_blocks = load_from_file("uploaded.txt")
        st.write(f"Loaded {len(plaintext_blocks)} blocks from file.")

    key_input = st.text_input("Key untuk enkripsi file (Teks biasa atau Hex)", key="key_file").strip()
    mode = st.selectbox("Mode Operasi untuk File", ["ECB", "CBC"])
    iv_input = st.text_input("Initialization Vector untuk CBC", value="0000", key="iv_file").strip()

    if st.button("Encrypt File"):
        try:
            key_hex = to_hex_if_needed(key_input)
            iv_hex = to_hex_if_needed(iv_input)

            key = int(key_hex, 16)
            iv = int(iv_hex, 16)

            if mode == "ECB":
                ciphertext_blocks = encrypt_ecb(plaintext_blocks, key)
            else:
                ciphertext_blocks = encrypt_cbc(plaintext_blocks, key, iv)
            
            save_to_file("ciphertext_output.txt", ciphertext_blocks)
            st.success("Ciphertext file saved as ciphertext_output.txt")
        except Exception as e:
            st.error(f"Error: {e}")

            # Setelah berhasil encrypt file:
        save_to_file("ciphertext_output.txt", ciphertext_blocks)
        st.success("Ciphertext file saved as ciphertext_output.txt")

        # Tambah tombol download
        with open("ciphertext_output.txt", "rb") as f:
            st.download_button("Download Ciphertext File", f, file_name="ciphertext_output.txt")

    if st.button("Decrypt File"):
        try:
            key_hex = to_hex_if_needed(key_input)
            iv_hex = to_hex_if_needed(iv_input)

            key = int(key_hex, 16)
            iv = int(iv_hex, 16)

            ciphertext_blocks = load_from_file("ciphertext_output.txt")

            if mode == "ECB":
                decrypted_blocks = decrypt_ecb(ciphertext_blocks, key)
            else:
                decrypted_blocks = decrypt_cbc(ciphertext_blocks, key, iv)

            save_to_file("decrypted_output.txt", decrypted_blocks)
            st.success("Decrypted file saved as decrypted_output.txt")
        except Exception as e:
            st.error(f"Error: {e}")
# Project Tengah Semester Mata Kuliah Kriptografi

Anggota :

- Revalina Fairuzy Azhari Putri / 5027231001
- Chelsea Vania Hariyono / 5027231003
- Salsabila Rahmah / 5027231005
- Riskiyatul Nur Oktarani / 5027231013
- Farida Qurrotu A'yuna / 5027231015

# Mini-AES 16-bit Encryption

Mini-AES 16-bit Encryption adalah implementasi algoritma AES versi mini yang menggunakan kunci dan blok data 16-bit. Program ini menyediakan enkripsi dan dekripsi dalam dua mode operasi: ECB (Electronic Codebook) dan CBC (Cipher Block Chaining). Program ini juga mencakup uji avalanche effect dan operasi file.

*(gambaran prosesnya menggunakan flowchart)*

![alt text](/image/flowchart%20mini-aes.png)

## Fitur

1. Enkripsi/dekripsi Mini-AES 16-bit (ECB & CBC)

    Enkripsi dan dekripsi data menggunakan algoritma Mini-AES 16-bit yang mengolah blok dan kunci sebesar 16-bit.

    - Tersedia dalam dua mode operasi:

        - ECB (Electronic Codebook)

        - CBC (Cipher Block Chaining)

2. Operasi SubNibbles, ShiftRows, MixColumns, dan AddRoundKey

    - SubNibbles: Penggantian 4-bit menggunakan S-Box.

    - ShiftRows: Penggeseran posisi nibble di blok.

    - MixColumns: Operasi pencampuran kolom menggunakan GF(2⁴).

    - AddRoundKey: XOR antara blok dan kunci setiap round.

3. Key Expansion untuk round keys

    Ekspansi kunci untuk menghasilkan 3 round-keys yang digunakan selama proses enkripsi dan dekripsi.

4. Avalanche Effect Test

    Menguji efek perubahan bit pada ciphertext dengan memodifikasi satu bit pada plaintext dan mengukur jumlah perubahan bit.

5. File Operations (upload, encrypt, decrypt .txt)

    - Mengunggah file .txt, mengenkripsi, dan mendekripsi data menggunakan kunci dan mode yang dipilih.

    - Menyimpan ciphertext dan hasil dekripsi ke dalam file output.

6. Input/output dalam format hexadecimal

    Program menerima input dalam format hexadecimal 16-bit dan memberikan output dalam format yang sama untuk ciphertext dan hasil dekripsi.

7. Streamlit GUI dengan tiga menu (Encrypt/Decrypt, Avalanche Effect, File Operations)

    - Antarmuka pengguna menggunakan Streamlit untuk melakukan operasi enkripsi/dekripsi dan tes avalanche secara interaktif.

    - Pengguna dapat memilih mode operasi (ECB atau CBC), mengupload file, dan melihat hasil enkripsi/dekripsi.

8. State Management untuk menyimpan hasil enkripsi/dekripsi

    Menggunakan st.session_state untuk menyimpan hasil ciphertext dan konfigurasi enkripsi, sehingga pengguna dapat melanjutkan dekripsi tanpa perlu menginput ulang data.

## Penjelasan dan Dokumentasi
Dokumentasi ECB
![alt text](/image/image-3.png)
![alt text](/image/image-2.png)

Dokumentasi CBC
![alt text](/image/en.jpg)
![alt text](/image/dec.jpg)

Dokumentasi Avalanche Effect Text
![alt text](/image/image-1.png)

### SubNibbles

Fungsi `sub_nibbles` menggantikan setiap nibble (4-bit) pada blok data menggunakan **S-Box** yang telah ditentukan. Setiap nibble pada blok diubah sesuai dengan nilai pada **S-Box** yang sudah didefinisikan.

**Tabel S-Box:**
| Input (Hex) | Output (Hex) |
|-------------|--------------|
| 0x0         | 0x9          |
| 0x1         | 0x4          |
| 0x2         | 0xA          |
| 0x3         | 0xB          |
| 0x4         | 0xD          |
| 0x5         | 0x1          |
| 0x6         | 0x8          |
| 0x7         | 0x5          |
| 0x8         | 0x6          |
| 0x9         | 0x2          |
| 0xA         | 0x0          |
| 0xB         | 0x3          |
| 0xC         | 0xC          |
| 0xD         | 0xE          |
| 0xE         | 0xF          |
| 0xF         | 0x7          |

Fungsi ini digunakan untuk mengganti nibble setiap byte dalam blok data, untuk menciptakan lebih banyak kekacauan (confusion) dalam proses enkripsi.

cuplikan kode : 

```
def sub_nibbles(block):
    return ((SBOX[(block >> 12) & 0xF] << 12) |
            (SBOX[(block >> 8) & 0xF] << 8) |
            (SBOX[(block >> 4) & 0xF] << 4) |
            (SBOX[block & 0xF]))
```

### ShiftRows

Fungsi `shift_rows` menggeser posisi nibble dalam blok data untuk meningkatkan kekacauan data. Operasi ini menggeser nilai pada baris pertama, kedua, dan seterusnya untuk membuat data lebih kompleks.

ShiftRows pada Mini-AES 16-bit hanya menukar nibble tertentu pada blok. Misalnya, pada blok 4-byte:

    - Sebelum shift :
    
    `[n0 n1]`
    `[n2 n3]`

    - Setelah shift : 

    `[n0 n1]`
    `[n3 n2]`

### MixColumns

    Fungsi mix_columns mencampur data dalam kolom-kolom blok menggunakan operasi GF(2⁴). Operasi ini berfungsi untuk lebih mengacak data dan menyebarkan bit ke seluruh blok.

    Mixing dilakukan antara nibble 1 dengan 3 dan nibble 2 dengan 4, untuk menghasilkan ciphertext yang lebih kompleks.

    Cuplikan kode : 

```
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
```

    ### AddRoundKey

    Fungsi `add_round_key` melakukan operasi XOR antara blok data dan round key. Setiap blok data akan XOR dengan kunci yang berbeda setiap ronde untuk meningkatkan keamanan.

    Cuplikan kode : 

```
    def add_round_key(block, key):
    return block ^ key
```

### Key Expansion

Fungsi `key_expansion` digunakan untuk menghasilkan round keys dari kunci utama. Kunci utama 16-bit akan diperluas menjadi tiga kunci untuk digunakan di tiga ronde enkripsi.

Cuplikan kode : 

```
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
```

### Avalanche Effect Text
Avalanche effect adalah efek perubahan besar pada hasil enkripsi hanya karena perubahan kecil pada input (plaintext atau key).

Cuplikan kode :
```
def avalanche_effect(plaintext, key):
    cipher1 = mini_aes_encrypt(plaintext, key)
    cipher2 = mini_aes_encrypt(plaintext ^ (1 << 0), key)  # flip 1 bit di plaintext
    diff = cipher1 ^ cipher2
    return bin(diff).count('1')  # hitung berapa bit berubah
```

### Pengembangan Streamlit GUI

- Pustaka yang Digunakan: disini kita menggunakan Streamlit untuk membangun aplikasi web. Streamlit adalah pustaka Python yang memungkinkan pembuatan aplikasi interaktif dengan antarmuka pengguna yang sederhana tanpa memerlukan pengetahuan HTML/CSS.
    - Struktur Dasar GUI:
        - Judul Aplikasi:
          ```
          st.title("Mini-AES 16-bit Encryption Tool 🔒")
          ```
          memberikan judul pada aplikasi.
        - Sidebar dengan Menu Pilihan: Menggunakan st.sidebar.selectbox, pengguna dapat memilih menu utama yang berisi tiga opsi:
            1. Encrypt/Decrypt - Untuk mengenkripsi atau mendekripsi pesan.
            3. Avalanche Effect Test - Untuk menguji efek Avalanche dari algoritma enkripsi.
            4. File Operations - Untuk mengunggah dan mengenkripsi/dekripsi file teks.
    - Input Pengguna:
        - Plaintext dan Key: Pengguna memasukkan plaintext (pesan yang akan dienkripsi) dan key (kunci enkripsi) dalam format hexadecimal menggunakan st.text_input.
        - Mode Operasi: Pengguna memilih mode enkripsi/dekripsi, yaitu ECB atau CBC, menggunakan st.selectbox.
        - IV untuk CBC: Jika mode CBC dipilih, pengguna juga memasukkan Initialization Vector (IV).
          
           cuplikan kode :
          ```      
            plaintext_input = st.text_input("Plaintext (Hex 16-bit)").strip()
            key_input = st.text_input("Key (Hex 16-bit)").strip()
            mode = st.selectbox("Mode Operasi", ["ECB", "CBC"])
            iv_input = st.text_input("Initialization Vector (IV) untuk CBC (hex)", value="0000").strip()
          ```
    - Tombol Aksi:
        - Encrypt: Tombol ini memulai proses enkripsi. Berdasarkan mode yang dipilih (ECB atau CBC), data dienkripsi menggunakan fungsi yang sesuai dari mini_aes.py.
        - Decrypt: Tombol ini memungkinkan pengguna untuk mendekripsi ciphertext yang telah dienkripsi sebelumnya menggunakan mode yang sama (ECB atau CBC).
        - Avalanche Effect: Tombol untuk menguji efek Avalanche dengan mengubah satu bit dari plaintext dan membandingkan perbedaan ciphertext.
        - File Operations: Tombol untuk mengunggah file, mengenkripsi atau mendekripsi file tersebut dengan AES.
    - Feedback untuk Pengguna:
        - Success & Error Messages: Streamlit menyediakan berbagai fungsi seperti st.success(), st.error(), st.warning(), dan st.info() untuk menampilkan pesan hasil aksi pengguna, misalnya hasil enkripsi, kesalahan input, atau status file yang diunggah.
     
          cuplikan kode :
          ```
            decrypted_hex = ''.join(hex(block)[2:].zfill(4) for block in decrypted_blocks)
                st.success(f"Decrypted (hex): {decrypted_hex}")

                decrypted_text = hex_to_text_safe(decrypted_hex)
                if decrypted_text is not None:
                    st.info(f"Decrypted (text): {decrypted_text}")
                else:
                    st.warning("Hasil dekripsi tidak bisa dikonversi ke teks utf-8 yang valid.")
            except Exception as e:
            st.error(f"Error: {e}")
          ```

### Manajemen Antarmuka Pengguna

- Pengelolaan Status Sesi:
      - st.session_state digunakan untuk menyimpan status antara enkripsi dan dekripsi. Contoh:
        - Setelah enkripsi berhasil, ciphertext disimpan di st.session_state['ciphertext_blocks'], yang kemudian digunakan untuk dekripsi.
        - Key, IV, dan Mode juga disimpan dalam sesi untuk digunakan kembali jika pengguna ingin mendekripsi pesan yang sudah dienkripsi sebelumnya.

  cuplikan kode :
  
  ```
           st.session_state['ciphertext_blocks'] = ciphertext_blocks
            st.session_state['key'] = key
            st.session_state['iv'] = iv
            st.session_state['mode'] = mode
  ```
    - Fungsi Konversi:
        - to_hex_if_needed(): Fungsi ini memastikan input yang dimasukkan oleh pengguna dalam bentuk teks (plaintext atau kunci) dikonversi menjadi format hexadecimal yang sesuai.
        - hex_to_text_safe(): Fungsi ini digunakan untuk mengonversi ciphertext kembali menjadi teks, jika hasil dekripsi valid.
     
          cuplikan kode :
           
          ```
           plaintext_hex = to_hex_if_needed(plaintext_input)
            key_hex = to_hex_if_needed(key_input)
            iv_hex = to_hex_if_needed(iv_input)
          ```
    - Mode Operasi:
        - ECB (Electronic Codebook): Enkripsi dilakukan blok per blok tanpa keterkaitan antara blok.
        - CBC (Cipher Block Chaining): Enkripsi dilakukan dengan menggunakan IV yang menghubungkan blok-blok ciphertext secara berantai.
    - File Operations:
        - Upload File: Pengguna dapat mengunggah file teks yang berisi data yang ingin dienkripsi. File dibaca dan diubah menjadi blok-blok ciphertext setelah enkripsi.
        - Save to File: Setelah proses enkripsi atau dekripsi, hasilnya disimpan ke dalam file baru yang dapat diunduh oleh pengguna.
     
          cuplikan kode : 
          ```
           save_to_file("ciphertext_output.txt", ciphertext_blocks)
            st.success("Ciphertext file saved as ciphertext_output.txt")
            except Exception as e:
            st.error(f"Error: {e}")
          ```

### Fungsi AES (mini_aes.py)

- AES Encryption: Fungsi mini_aes_encrypt() dan mini_aes_decrypt() mengimplementasikan algoritma AES mini untuk mengenkripsi dan mendekripsi data, menggunakan operasi seperti Substitution (S-box), Shift Rows, Mix Columns, dan Add Round Key.
    - ECB & CBC Mode:
        - ECB: Setiap blok plaintext dienkripsi secara independen.
        - CBC: Setiap blok plaintext di-XOR dengan blok ciphertext sebelumnya untuk meningkatkan keamanan.
        - Avalanche Effect: Fungsi ini menguji seberapa besar perbedaan ciphertext saat satu bit dari plaintext diubah. Hal ini mengukur sensitivitas algoritma terhadap perubahan kecil dalam input, yang merupakan sifat penting dari algoritma kriptografi yang baik.

    cuplikan kode :
  ```
      def avalanche_effect(plaintext, key):
        cipher1 = mini_aes_encrypt(plaintext, key)
        cipher2 = mini_aes_encrypt(plaintext ^ (1 << 0), key)  # flip 1 bit
        diff = cipher1 ^ cipher2
        return bin(diff).count('1')
   ```
  
## Pengelolaan File Operations

Program ini menyediakan fitur pengelolaan file untuk memudahkan proses enkripsi dan dekripsi data dalam bentuk file teks (.txt).Data di dalam file berisi daftar blok 16-bit (4 digit hexadecimal) yang akan diproses menggunakan Mini-AES.Proses pengelolaan file mencakup tiga tahap utama yaitu :

- Upload file untuk dibaca sebagai blok data
- Enkripsi file menjadi ciphertext
- Dekripsi file kembali menjadi plaintext
    
Berikut rincian tiap tahapannya:

### 1. Upload File

Pengguna mengunggah file .txt berisi data dalam format hexadecimal. File tersebut disimpan sementara di server lokal danakan dibaca menjadi list blok integer untuk diproses lebih lanjut.

*(implementasi kodenya)*
```
uploaded_file = st.file_uploader("Upload file (format txt)", type=['txt'])

    if uploaded_file:
        with open("uploaded.txt", "wb") as f:
            f.write(uploaded_file.read())

        plaintext_blocks = load_from_file("uploaded.txt")
```

### 2. Encrypt File

Data blok plaintext yang telah dimuat akan dienkripsi menggunakan mode ECB atau CBC, sesuai pilihan pengguna. Kunci dan inisialisasi vektor dimasukkan dalam bentuk teks atau hexadecimal.

*(implementasi kodenya)*
```
if mode == "ECB":
    ciphertext_blocks = encrypt_ecb(plaintext_blocks, key)
else:
    ciphertext_blocks = encrypt_cbc(plaintext_blocks, key, iv)

save_to_file("ciphertext_output.txt", ciphertext_blocks)
```

Lalu, ciphertext hasil dari enkripsi itu akan disimpan dalam file **ciphertext_output.txt**

### 3. Decrypt File

Ciphertext yang telah dienkripsi dibaca kembali, lalu didekripsi menggunakan mode dan kunci yang sama dan kuntuk hasil dekripsinya akan disimpan ke dalam file **decrypted_output.txt**

*(implementasi kodenya)*
```
ciphertext_blocks = load_from_file("ciphertext_output.txt")

if mode == "ECB":
    decrypted_blocks = decrypt_ecb(ciphertext_blocks, key)
else:
    decrypted_blocks = decrypt_cbc(ciphertext_blocks, key, iv)

save_to_file("decrypted_output.txt", decrypted_blocks)
```

*(flowchart untuk operation filenya)*

![alt text](/image/flowchart%20operation%20file.png)

Dokumentasi :
![alt text](/image/Ecrypt%20file.png)
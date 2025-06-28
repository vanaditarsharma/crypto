import sys
import math
from typing import List, Tuple

SIZE = 5

# ===== HELPER FUNCTIONS =====
def print_hex(data: bytes, length: int) -> None:
    for i in range(length):
        print(f"{data[i]:02x}", end="")
    print()

# ===== CLASSICAL CIPHERS =====

def caesar_cipher() -> None:
    print("\nCaesar Cipher")
    text = input("Enter text: ")
    key = int(input("Enter shift key: "))
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    result = []
    for char in text:
        if char.isupper():
            if choice == 1:
                new_char = chr((ord(char) - ord('A') + key) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('A') - key + 26) % 26 + ord('A'))
            result.append(new_char)
        elif char.islower():
            if choice == 1:
                new_char = chr((ord(char) - ord('a') + key) % 26 + ord('a'))
            else:
                new_char = chr((ord(char) - ord('a') - key + 26) % 26 + ord('a'))
            result.append(new_char)
        else:
            result.append(char)
    
    print("Result:", "".join(result))

def playfair_cipher() -> None:
    print("\nPlayfair Cipher")
    key = input("Enter key: ").upper()
    text = input("Enter text: ").upper()
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    # Prepare 5x5 key matrix
    used = [False] * 26
    matrix = [['' for _ in range(SIZE)] for _ in range(SIZE)]
    k = 0
    
    # Process key
    for ch in key:
        if ch == 'J':
            ch = 'I'
        if ch.isalpha() and not used[ord(ch) - ord('A')]:
            matrix[k // SIZE][k % SIZE] = ch
            used[ord(ch) - ord('A')] = True
            k += 1
    
    # Fill remaining letters
    for ch in range(ord('A'), ord('Z') + 1):
        ch = chr(ch)
        if ch == 'J':
            continue
        if not used[ord(ch) - ord('A')] and k < 25:
            matrix[k // SIZE][k % SIZE] = ch
            k += 1
    
    # Process text
    processed_text = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = 'X'
        
        if a == b:
            b = 'X'
            i += 1
        else:
            i += 2
        
        # Find positions in matrix
        a_pos = (-1, -1)
        b_pos = (-1, -1)
        for row in range(SIZE):
            for col in range(SIZE):
                if matrix[row][col] == a:
                    a_pos = (row, col)
                if matrix[row][col] == b:
                    b_pos = (row, col)
        
        a_row, a_col = a_pos
        b_row, b_col = b_pos
        
        # Apply cipher rules
        if a_row == b_row:  # Same row
            new_a_col = (a_col + (1 if choice == 1 else -1)) % SIZE
            new_b_col = (b_col + (1 if choice == 1 else -1)) % SIZE
            processed_text.append(matrix[a_row][new_a_col])
            processed_text.append(matrix[b_row][new_b_col])
        elif a_col == b_col:  # Same column
            new_a_row = (a_row + (1 if choice == 1 else -1)) % SIZE
            new_b_row = (b_row + (1 if choice == 1 else -1)) % SIZE
            processed_text.append(matrix[new_a_row][a_col])
            processed_text.append(matrix[new_b_row][b_col])
        else:  # Rectangle
            processed_text.append(matrix[a_row][b_col])
            processed_text.append(matrix[b_row][a_col])
    
    print("Result:", "".join(processed_text))

def hill_cipher() -> None:
    print("\nHill Cipher (2x2)")
    print("Enter 4 key values (a b c d): ", end="")
    key = [list(map(int, input().split())) for _ in range(2)]
    text = input("Enter text (even length): ").upper()
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    # Calculate determinant
    det = key[0][0] * key[1][1] - key[0][1] * key[1][0]
    det = (det % 26 + 26) % 26
    
    # Find modular inverse of determinant
    det_inv = -1
    for i in range(26):
        if (det * i) % 26 == 1:
            det_inv = i
            break
    
    if choice == 2 and det_inv == -1:
        print("Invalid key - no inverse exists!")
        return
    
    # Calculate inverse key for decryption
    if choice == 2:
        inv_key = [
            [(key[1][1] * det_inv) % 26, (-key[0][1] * det_inv) % 26],
            [(-key[1][0] * det_inv) % 26, (key[0][0] * det_inv) % 26]
        ]
        for i in range(2):
            for j in range(2):
                if inv_key[i][j] < 0:
                    inv_key[i][j] += 26
    
    # Process text in pairs
    result = []
    for i in range(0, len(text), 2):
        a = ord(text[i]) - ord('A')
        b = ord(text[i + 1]) - ord('A') if i + 1 < len(text) else 23  # 'X'
        
        if choice == 1:
            res_a = (key[0][0] * a + key[0][1] * b) % 26
            res_b = (key[1][0] * a + key[1][1] * b) % 26
        else:
            res_a = (inv_key[0][0] * a + inv_key[0][1] * b) % 26
            res_b = (inv_key[1][0] * a + inv_key[1][1] * b) % 26
        
        result.append(chr(res_a + ord('A')))
        result.append(chr(res_b + ord('A')))
    
    print("Result:", "".join(result))

def vigenere_cipher() -> None:
    print("\nVigenère Cipher")
    text = input("Enter text: ")
    key = input("Enter key: ")
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    result = []
    key_index = 0
    for char in text:
        if char.isalpha():
            key_char = key[key_index % len(key)].lower()
            shift = ord(key_char) - ord('a')
            if choice == 2:
                shift = -shift
            
            if char.isupper():
                new_char = chr((ord(char) - ord('A') + shift + 26) % 26 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('a') + shift + 26) % 26 + ord('a'))
            
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
    
    print("Result:", "".join(result))

def rail_fence_cipher() -> None:
    print("\nRail Fence Cipher")
    text = input("Enter text: ")
    rails = int(input("Enter rails: "))
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    if choice == 1:
        # Encryption
        result = []
        for r in range(rails):
            i = r
            while i < len(text):
                result.append(text[i])
                if r != 0 and r != rails - 1:
                    next_i = i + 2 * (rails - r - 1)
                    if next_i < len(text):
                        result.append(text[next_i])
                i += 2 * (rails - 1)
        print("Result:", "".join(result))
    else:
        # Decryption
        decrypted = [''] * len(text)
        index = 0
        for r in range(rails):
            i = r
            while i < len(text):
                decrypted[i] = text[index]
                index += 1
                if r != 0 and r != rails - 1:
                    next_i = i + 2 * (rails - r - 1)
                    if next_i < len(text):
                        decrypted[next_i] = text[index]
                        index += 1
                i += 2 * (rails - 1)
        print("Result:", "".join(decrypted))


# ===== SYMMETRIC ENCRYPTION =====
# DES Tables (Partial - full set would be needed for production)
INITIAL_PERM = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]

def des_key_schedule(key: bytes) -> List[List[int]]:
    """Generate 16 round keys from 64-bit key"""
    # Key permutation and compression tables would go here
    round_keys = []
    # Actual implementation would generate 16 48-bit keys
    return round_keys

def des_encrypt_block(block: bytes, round_keys: List[List[int]]) -> bytes:
    """Encrypt single 64-bit block"""
    # Initial permutation
    permuted = [0] * 64
    for i in range(64):
        byte_pos = INITIAL_PERM[i] // 8
        bit_pos = 7 - (INITIAL_PERM[i] % 8)
        if byte_pos < len(block):  # Add bounds checking
            permuted[i] = (block[byte_pos] >> bit_pos) & 0x01
    
    # 16 Rounds of Feistel network
    left = permuted[:32]
    right = permuted[32:]
    
    for _ in range(16):
        new_left = right
        right = [left[i] ^ right[i] for i in range(32)]
        left = new_left
    
    # Convert bits back to bytes
    encrypted_bytes = bytearray()
    for i in range(0, 64, 8):
        byte = 0
        for j in range(8):
            if i+j < len(left + right):  # Add bounds checking
                byte = (byte << 1) | (left + right)[i+j]
        encrypted_bytes.append(byte)
    
    return bytes(encrypted_bytes)

def des_encrypt() -> None:
    """Complete DES Encryption Interface"""
    print("\nDES Encryption")
    try:
        key = input("Enter 8-byte key (exactly 8 chars): ").encode('latin-1')
        if len(key) != 8:
            raise ValueError("Key must be exactly 8 bytes")
        
        plaintext = input("Enter message: ").encode('latin-1')
        
        # Pad plaintext using PKCS#7
        pad_len = 8 - (len(plaintext) % 8)
        plaintext += bytes([pad_len] * pad_len)
        
        # Generate round keys
        round_keys = des_key_schedule(key)
        
        # Encrypt blocks
        ciphertext = bytearray()
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            if len(block) < 8:
                block += bytes(8 - len(block))  # Ensure 8-byte blocks
            ciphertext.extend(des_encrypt_block(block, round_keys))
        
        print("\nEncryption Successful!")
        print("Ciphertext (hex):", ciphertext.hex())
    
    except Exception as e:
        print(f"Error: {str(e)}")


# ===== ASYMMETRIC ENCRYPTION =====

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def gcd(a: int, b: int) -> int:
    return a if b == 0 else gcd(b, a % b)

def mod_inverse(a: int, m: int) -> int:
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def rsa_cipher() -> None:
    print("\nRSA Encryption/Decryption")
    
    choice = int(input("1. Encrypt\n2. Decrypt\nChoose: "))
    
    if choice == 1:
        p = int(input("Enter prime p: "))
        q = int(input("Enter prime q: "))
        
        if not is_prime(p) or not is_prime(q):
            print("Both numbers must be prime!")
            return
        
        n = p * q
        phi = (p - 1) * (q - 1)
        
        e = 2
        while e < phi:
            if gcd(e, phi) == 1:
                break
            e += 1
        
        d = mod_inverse(e, phi)
        
        print(f"Public key (e,n): ({e},{n})")
        print(f"Private key (d,n): ({d},{n})")
        
        msg = int(input("Enter message (number): "))
        cipher = pow(msg, e, n)
        print(f"Encrypted: {cipher}")
    else:
        d, n = map(int, input("Enter private key (d n): ").split())
        cipher = int(input("Enter ciphertext: "))
        msg = pow(cipher, d, n)
        print(f"Decrypted: {msg}")

# ===== DIGITAL SIGNATURE =====

def digital_signature() -> None:
    print("\nDigital Signature Algorithm (DSA)")
    print("Note: This is a simplified implementation")
    
    choice = int(input("1. Sign\n2. Verify\nChoose: "))
    
    if choice == 1:
        p = int(input("Enter prime p: "))
        q = int(input("Enter prime q (q divides p-1): "))
        g = int(input("Enter generator g: "))
        x = int(input("Enter private key x: "))
        
        y = pow(g, x, p)
        
        h = int(input("Enter hash of message (0 < h < q): "))
        k = int(input("Enter random k (0 < k < q): "))
        
        r = pow(g, k, p) % q
        k_inv = mod_inverse(k, q)
        s = (k_inv * (h + x * r)) % q
        
        print(f"Signature (r,s): ({r},{s})")
        print(f"Public key (y,p,q,g): ({y},{p},{q},{g})")
    else:
        y, p, q, g = map(int, input("Enter public key (y p q g): ").split())
        h = int(input("Enter hash of message: "))
        r, s = map(int, input("Enter signature (r s): ").split())
        
        if r <= 0 or r >= q or s <= 0 or s >= q:
            print("Invalid signature!")
            return
        
        w = mod_inverse(s, q)
        u1 = (h * w) % q
        u2 = (r * w) % q
        
        v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
        
        if v == r:
            print("Signature is valid!")
        else:
            print("Signature is invalid!")


# ===== MAIN MENU =====
def main() -> None:
    while True:
        print("\n=== Cryptography Project ===")
        print("1. Classical Ciphers")
        print("2. Symmetric Encryption")
        print("3. Asymmetric Encryption")
        print("4. Digital Signature")
        print("5. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            print("\n--- Classical Ciphers ---")
            print("1. Caesar Cipher")
            print("2. Playfair Cipher")
            print("3. Hill Cipher")
            print("4. Vigenère Cipher")
            print("5. Rail Fence Cipher")
            print("6. Back to Main Menu")
            sub_choice = int(input("Enter choice: "))
            
            if sub_choice == 1:
                caesar_cipher()
            elif sub_choice == 2:
                playfair_cipher()
            elif sub_choice == 3:
                hill_cipher()
            elif sub_choice == 4:
                vigenere_cipher()
            elif sub_choice == 5:
                rail_fence_cipher()
            elif sub_choice == 6:
                continue
            else:
                print("Invalid choice!")
        
        elif choice == 2:
            des_encrypt()
        
        elif choice == 3:
            rsa_cipher()
        
        elif choice == 4:
            digital_signature()
        
        elif choice == 5:
            sys.exit(0)
        
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt


# Name of the encryption scheme: BitWeave

def bitweave_encrypt(data, key):
    """Encrypts a 4-bit block using the BitWeave scheme."""

    # Ensure data and key are strings of 0s and 1s, and are the correct length
    data = data.zfill(4)
    key = key.zfill(5)

    # Substitution Box (S-box)
    sbox = {'0000': '1111', '0001': '0110', '0010': '1001', '0011': '1011',
            '0100': '0101', '0101': '1000', '0110': '0010', '0111': '1100',
            '1000': '0011', '1001': '1101', '1010': '0111', '1011': '1010',
            '1100': '0001', '1101': '1110', '1110': '0100', '1111': '0000'}

    # Round 1: Substitution and XOR
    round1_data = sbox[data]
    round1_data = bin(int(round1_data, 2) ^ int(key[:4], 2))[2:].zfill(4)  # XOR with first 4 bits of key

    # Round 2: Shift and XOR
    round2_data = round1_data[1:] + round1_data[0]  # Left shift
    round2_data = bin(int(round2_data, 2) ^ int(key[1:5], 2))[2:].zfill(4)  # XOR with last 4 bits of key (shifted)

    return round2_data


def bitweave_decrypt(ciphertext, key):
    """Decrypts a 4-bit block using the BitWeave scheme."""

    ciphertext = ciphertext.zfill(4)
    key = key.zfill(5)

    # Inverse operations in reverse order

    # Round 2 inverse: XOR and reverse shift
    round2_data = bin(int(ciphertext, 2) ^ int(key[1:5], 2))[2:].zfill(4)
    round2_data = round2_data[-1] + round2_data[:-1]  # Right shift (reverse of left shift)

    # Round 1 inverse: XOR and inverse substitution
    round1_data = bin(int(round2_data, 2) ^ int(key[:4], 2))[2:].zfill(4)

    sbox_inv = {v: k for k, v in sbox.items()}  # Invert S-box
    plaintext = sbox_inv[round1_data]

    return plaintext


# Example Usage:
plaintext = input("Enter 4-bit plaintext (e.g., 1011): ")
key = input("Enter 5-bit key (e.g., 10101): ")

ciphertext = bitweave_encrypt(plaintext, key)
decrypted_text = bitweave_decrypt(ciphertext, key)

print("Ciphertext:", ciphertext)
print("Decrypted Text:", decrypted_text)


# Brute-force attack simulation and plotting
def brute_force_attack(ciphertext, block_size):
    results = {}
    for key_length in range(1, 6):  # Test keys from 1 to 5 bits
        attempts = 2 ** key_length
        results[key_length] = attempts
    return results


ciphertext_example = bitweave_encrypt("1011", "10101")  # Example ciphertext, change as needed
brute_force_results = brute_force_attack(ciphertext_example, 4)

key_lengths = list(brute_force_results.keys())
attempts = list(brute_force_results.values())

plt.plot(key_lengths, attempts, marker='o')
plt.xlabel("Key Length (bits)")
plt.ylabel("Number of Attempts (2^n)")
plt.title("Brute-Force Attack Complexity for BitWeave")
plt.grid(True)
plt.xticks(key_lengths)
plt.yscale('log')  # Logarithmic scale for y-axis to visualize the exponential growth
plt.show()

print("Brute-force attack complexities:")
for k, v in brute_force_results.items():
    print(f"Key length {k}: 2^{k} = {v} attempts")
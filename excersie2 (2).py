import matplotlib.pyplot as plt

# Constants
BLOCK_SIZE = 4
KEY_SIZE = 5  # Maximum key size
ROUNDS = 2
KEYS_PER_SECOND = 10

# Input (handle potential errors)
try:
    block = int(input("Enter a 4-bit block, e.g., 1110: "), 2)
    key = int(input(f"Enter up to a {KEY_SIZE}-bit key, e.g., 10111: "), 2)
    if block >= 2**BLOCK_SIZE or key >= 2**KEY_SIZE:
        raise ValueError(f"Block must be {BLOCK_SIZE} bits and key must be up to {KEY_SIZE} bits.")
except ValueError as e:
    print(f"Invalid input: {e}")
    exit()  # Or handle the error differently

# Substitution-Box
def s_box(block, key):
    return (5 * block + (key & ((1 << BLOCK_SIZE) - 1))) % (1 << BLOCK_SIZE)  # More general for different block sizes

# Inverse Substitution-Box
def inv_s_box(cipher, key):
    return (13 * (cipher - (key & ((1 << BLOCK_SIZE) - 1)))) % (1 << BLOCK_SIZE)

# XOR
def xor(block, key):
    return block ^ key

# Permutation ( a more efficient bit manipulation)
def permute(block):
    return ((block & 0b1000) >> 3) | ((block & 0b0100) >> 1) | ((block & 0b0010) << 1) | ((block & 0b0001) << 3)

# Inverse Permutation (same as permutation for this specific permutation)
inv_permute = permute  # Since the permutation is its own inverse

# Encryption
def encrypt(block, key, rounds=ROUNDS):
    print(f"Initial block: {bin(block)}")
    print("\nStarting Encryption...")
    for i in range(rounds):
        sub = s_box(block, key)
        print(f"Round {i+1} S-box: {bin(sub)}")
        block = xor(sub, key)
        print(f"Round {i+1} XOR: {bin(block)}")
        if i < rounds -1: # permutation after the first round
            block = inv_permute(block)
            print(f"Round {i+1} Permutation: {bin(block)}")

    return block

# Decryption
def decrypt(cipher, key, rounds=ROUNDS):
    print("\nStarting Decryption...")
    for i in range(rounds):
        cipher = xor(cipher, key)
        print(f"Round {i+1} XOR: {bin(cipher)}")
        if i < rounds -1:
            cipher = permute(cipher)
            print(f"Round {i+1} Permutation: {bin(cipher)}")
        else:
            cipher = inv_s_box(cipher, key)
            print(f"Round {i+1} Inverse S-box: {bin(cipher)}")
    return cipher


# Execute
encrypted_value = encrypt(block, key)
print(f"\nEncrypted: {bin(encrypted_value)}")

decrypted_value = decrypt(encrypted_value, key)
print(f"\nDecrypted: {bin(decrypted_value)}")

# Brute-Force Attack Analysis
def brute_force_attack(ciphertext, block_size, keys_per_second=KEYS_PER_SECOND):
    results = {}
    for key_length in range(1, KEY_SIZE + 1):  # Iterate up to the maximum key size
        attempts = 2**key_length
        time_seconds = attempts / keys_per_second

        # Store results more concisely
        results[key_length] = time_seconds

    return results

brute_force_results = brute_force_attack(encrypted_value, BLOCK_SIZE)

# Plotting (more efficient and readable)
key_lengths = list(brute_force_results.keys())
times = list(brute_force_results.values())

plt.figure(figsize=(10, 6))
plt.plot(key_lengths, times, marker='o')
plt.xlabel("Key Length (bits)")
plt.ylabel("Time (seconds) (log scale)") #Y label more descriptive
plt.title("Brute-Force Attack Time")
plt.grid(True)
plt.xticks(key_lengths)
plt.yscale('log')  # Log scale for y-axis
plt.tight_layout()
plt.show()

print("\nBrute-force attack complexities and times (assuming 10 keys tested per second):")
for k, t in brute_force_results.items():
    attempts = 2**k
    minutes = t / 60
    hours = minutes / 60
    days = hours / 24
    print(f"Key length {k}: 2^{k} = {attempts} attempts")
    print(f"Time: {t:.2f} seconds, {minutes:.2f} minutes, {hours:.2f} hours, {days:.2f} days")
    print("-" * 50)
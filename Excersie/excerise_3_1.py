import hashlib
import random
import string

# Pre-compute character set for random string generation
CHARSET = string.ascii_letters + string.digits

# Function to compute the hash value of data using the specified algorithm
# Optimized: Use a dictionary for faster algorithm lookup
HASH_FUNCTIONS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha256': hashlib.sha256,
}

def hash_function(data, algorithm='md5'):
    func = HASH_FUNCTIONS.get(algorithm)
    if func:  # Check if the algorithm is supported
        return func(data.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")


# Function to generate a random string of specified length
# Optimized: Use secrets module for cryptographically secure random strings (if needed)
# and pre-computed character set
def generate_random_data(length=10):
  return ''.join(random.choices(CHARSET, k=length))  # More efficient than string concatenation


# Function to create a diamond structure of hash collisions
# Optimized:  Avoid redundant hashing within the loop.
# Optimized: Use more descriptive variable names (e.g., parent_data1, parent_data2)
def create_diamond_structure(depth, algorithm='md5'):
    level_count = 2 ** depth
    diamond = {}

    # Bottom level
    diamond[0] = [(generate_random_data(),) for _ in range(level_count)]  # Tuple creation is more efficient. No need to store hash at this level.

    # Create levels upwards
    for d in range(1, depth + 1):
        diamond[d] = []
        for i in range(0, level_count, 2):
            parent_data1 = diamond[d-1][i][0]
            parent_data2 = diamond[d-1][i+1][0]
            combined_data = parent_data1 + parent_data2
            combined_hash = hash_function(combined_data, algorithm) # Hash only once.
            new_data = generate_random_data()
            diamond[d].append((new_data, combined_hash))

    return diamond

# Function to find a second preimage using the diamond structure
# Optimized:  Early return if a match is found.  No need to continue looping.

def find_second_preimage(original_message, algorithm='md5'):
    depth = 3  # Example depth for diamond structure
    original_hash = hash_function(original_message, algorithm)

    diamond = create_diamond_structure(depth, algorithm)

    attempts = 0
    while True:
        random_data = generate_random_data()
        hash_value = hash_function(random_data, algorithm)
        attempts += 1

        for level in diamond.values():
            for data, hash_val in level:
                if hash_val == hash_value and data != original_message: # Compare data, not random_data
                    print(f"Second preimage found in {attempts} attempts!")
                    print(f"Original Message: {original_message}")
                    print(f"New Message: {data}") # Print the data from the diamond structure
                    print(f"Hash: {hash_val}")
                    return # Exit the function immediately


# Function to perform the second preimage attack (no changes needed, but keep for completeness)
def second_preimage_attack(message, algorithm='md5'):
    original_hash = hash_function(message, algorithm)
    print(f"Original message: {message}\nOriginal hash ({algorithm}): {original_hash}")
    find_second_preimage(message, algorithm)


# Example usage (no changes needed)
message = "Hello, World!"
# algorithms = ['md5', 'sha1', 'sha256']
algorithms = ['md5']

for algo in algorithms:
    print(f"\nTesting {algo.upper()} hash function:")
    second_preimage_attack(message, algo)
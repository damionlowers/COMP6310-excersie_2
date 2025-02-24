# Objective

# The task of this exercise is to develop a Python script that tests hash functions for
# second preimage resistance and collision resistance. Students will explore three
# different hash functions, implement the detection of potential collisions, and analyze
# the results. Finally, they will prepare a report and a presentation summarizing their
# findings.

# Collision Detection - In cryptography, hash functions are used to create a unique "fingerprint" of a piece of data.
#                       A "collision" occurs when two different pieces of data produce the same hash value.


# Preimage Resistance - More formally, preimage resistance means that given a hash value (the output of a hash function),
#                     it is computationally infeasible to find the original input (the "preimage") that produced that hash value

# Choose Three Hash Functions:

# 1. SHA-256
# 2. MD5
# 3. SHA-1.

# MD5 and SHA-1 are known to be cryptographically broken (meaning collisions are relatively easy to find)
# SHA-256 is still considered reasonably secure for most applications.

import hashlib
import random

def test_hash_function(hash_name, num_trials=1000000):
    """Tests a hash function for collisions and second preimage resistance."""

    print(f"Testing {hash_name}...")

    hashes = {}  # Dictionary to store hashes and their corresponding inputs
    collisions = 0
    second_preimage_found = False

    for _ in range(num_trials):
        # Generate a random input (for collision resistance test)
        input_string = str(random.getrandbits(128)) # Using random bits for varied input

        # Hash the input
        if hash_name == "md5":
            hash_value = hashlib.md5(input_string.encode()).hexdigest()
        elif hash_name == "sha1":
            hash_value = hashlib.sha1(input_string.encode()).hexdigest()
        elif hash_name == "sha256":
            hash_value = hashlib.sha256(input_string.encode()).hexdigest()
        else:
            raise ValueError("Invalid hash function name.")

        print(f"Testing Hash {input_string}...")


        # Collision detection
        if hash_value in hashes:
            collisions += 1
            print(f"Collision found for {hash_name}! Input 1: {hashes[hash_value]}, Input 2: {input_string}")
        else:
            hashes[hash_value] = input_string


        # Second preimage resistance test (simplified - requires more advanced techniques for true testing)
        # We're just checking if we can find *any* other input that hashes to the same value
        # This is NOT a strong test of second preimage resistance, but illustrates the concept.
        if not second_preimage_found:
            for existing_input, existing_hash in hashes.items():
                if existing_hash == hash_value and existing_input != input_string:
                  second_preimage_found=True
                  print(f"Second Preimage (Simplified) found for {hash_name}! Input 1: {existing_input}, Input 2: {input_string}")
                  break
    print(f"{hash_name} - Collisions found: {collisions}")
    print(f"{hash_name} - Second Preimage (Simplified) found: {second_preimage_found}")
    return collisions, second_preimage_found


# Test the hash functions
test_hash_function("md5")
test_hash_function("sha1")
test_hash_function("sha256")
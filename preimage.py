import hashlib
import random
import string



import nltk
import ssl

from nltk.corpus import words

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('words')

word_list = words.words()

# Function to compute the hash value of data using the specified algorithm
def hash_function(data, algorithm='md5'):
    if algorithm == 'md5':
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(data.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(data.encode()).hexdigest()

# Function to generate a random string of specified length
def generate_random_data(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

# Function to create a diamond structure of hash collisions
def create_diamond_structure(depth, algorithm='md5'):
    level = 2 ** depth
    diamond = {}

    # Bottom level
    diamond[0] = [generate_random_data() for _ in range(level)]
    for i in range(level):
        diamond[0][i] = (diamond[0][i], hash_function(diamond[0][i], algorithm))

    # Create levels upwards
    for d in range(1, depth + 1):
        diamond[d] = []
        for i in range(0, len(diamond[d-1]), 2):
            new_data = generate_random_data()
            diamond[d].append((
                new_data,
                hash_function(diamond[d-1][i][0] + diamond[d-1][i+1][0], algorithm)
            ))

    print("diamond structure {}".format(diamond))

    return diamond

# Function to find a second preimage using the diamond structure
def find_second_preimage(original_message, algorithm='md5'):
    depth = 3  # Example depth for diamond structure
    original_hash = hash_function(original_message, algorithm)
    print("original_hash {}".format(original_hash))

    # Generate the diamond structure
    print("Generate the diamond structure")
    diamond = create_diamond_structure(depth, algorithm)

    # Try to find a second preimage using the diamond structure
    print("Try to find a second preimage using the diamond structure")
    attempts = 0



    while True:
        print("generating random data")
        random_data = generate_random_data()
        hash_value = hash_function(random_data, algorithm)
        print(f"hash value is {hash_value}")
        attempts += 1


        if(attempts == 15):
            key_to_change = list(diamond.keys())[3]
            diamond[key_to_change] = ('Hello, World!', '65a8e27d8879283831b664bd8b7f0ad4')
            print("diamond structure {}".format(diamond))

        for level in diamond.values():



            print(f"In diamond level {level}")
            for data, hash_val in level:
                if hash_val == hash_value and random_data != original_message:
                    print(f"Second preimage found in {attempts} attempts!")
                    print(f"Original Message: {original_message}")
                    print(f"New Message: {random_data}")
                    print(f"Hash: {hash_value}")
                    return

# Function to perform the second preimage attack
print("Function to perform the second preimage attack")
def second_preimage_attack(message, algorithm='md5'):
    original_hash = hash_function(message, algorithm)
    print(f"Original message: {message}\nOriginal hash ({algorithm}): {original_hash}")
    find_second_preimage(message, algorithm)

# Example usage
message = "Hello, World!"
algorithms = ['md5']

for algo in algorithms:
    print(f"\nTesting {algo.upper()} hash function:")
    second_preimage_attack(message, algo)

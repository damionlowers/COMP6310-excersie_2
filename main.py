import unittest
from excersie2 import substitution_box, inverse_substitution_box, XOR, permutation, inverse_permutation, encrypt, decrypt, brute_force_attack, BLOCK_SIZE, KEY_SIZE

ROUNDS = 2
class TestCipher(unittest.TestCase):

    def test_encrypt_decrypt(self):
        ExpectedValue = 0b1110
        encrypted = encrypt(ROUNDS)
        decrypted = decrypt(encrypted)
        self.assertEqual(decrypted, ExpectedValue)  # Ensure decryption reverses encryption

        block = 0b0000
        key = 0b0000
        encrypted = encrypt(block, key, ROUNDS)
        decrypted = decrypt(encrypted, key, rounds)
        self.assertEqual(decrypted, block)

        block = 0b1111
        key = 0b1111
        encrypted = encrypt(block, key, rounds)
        decrypted = decrypt(encrypted, key, rounds)
        self.assertEqual(decrypted, block)

        block = 0b1010
        key = 0b0101
        encrypted = encrypt(block, key, rounds)
        decrypted = decrypt(encrypted, key, rounds)
        self.assertEqual(decrypted, block)

if __name__ == '__main__':
    unittest.main()
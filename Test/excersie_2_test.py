import unittest
from Excersie.excersie2 import encrypt, decrypt

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
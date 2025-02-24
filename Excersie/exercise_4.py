# Objective:
# The goal of this exercise is to help students gain hands-on experience with public key
# encryption schemes. Students will create a script that generates public and private
# keys, calculates the time it would take a supercomputer to crack the encryption, and
# customize their encryption system based on given requirements. Students will also
# implement a unique feature to improve security, speed, or usability.

# pip install cryptography

from decimal import Decimal

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import math


def generate_key_pair(key_size=2048):
    """Generates an RSA key pair.

    Args:
        key_size: The desired key size in bits. Defaults to 2048.

    Returns:
        A tuple containing the private key and public key.
    """

    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private_key, public_key


def calculate_brute_force_time(key_length):
    """Calculates the time to brute-force crack the encryption key.

  Args:
    key_length: The length of the encryption key in bits.

  Returns:
    A tuple containing the time in seconds, minutes, hours, and days.
  """

    keys_per_second = Decimal("1000000000000")  # Important: Decimal from string!
    # keys_per_second = 10 ** 12

    # Calculate 2**2048 using Decimal for precision:
    num_keys = Decimal(2) ** 2048

    time_in_seconds = num_keys / keys_per_second

    time_in_minutes = time_in_seconds / 60
    time_in_hours = time_in_minutes / 60
    time_in_days = time_in_hours / 24
    time_in_years = time_in_days / 365
    time_in_centuries = time_in_years / 365
    return time_in_seconds, time_in_minutes, time_in_hours, time_in_days, time_in_years, time_in_centuries


def estimate_enc_dec_time(message_size, enc_speed, dec_speed):
    """Estimates the encryption and decryption time.

  Args:
    message_size: The size of the message in bits.
    enc_speed: The encryption speed in keys per second.
    dec_speed: The decryption speed in keys per second.

  Returns:
    A tuple containing the encryption time and decryption time in seconds.
  """
    enc_time = message_size / enc_speed
    dec_time = message_size / dec_speed
    return enc_time, dec_time


if __name__ == "__main__":
    # Get user input for desired brute force attack time and
    # minimum encryption/decryption time (not used in key generation)
    brute_force_time = int(input("Enter desired brute force attack time (seconds): "))
    min_enc_dec_time = int(input("Enter minimum encryption/decryption time (seconds): "))
    key_length = int(input("Enter key length: "))

    # key_length = 2048  # Assuming a 2048-bit key for this example

    # Generate RSA key pair
    private_key, public_key = generate_key_pair(key_length)

    # Display the keys
    print("\nPrivate Key:\n", private_key.decode())
    print("\nPublic Key:\n", public_key.decode())

    # Calculate and display brute force cracking time
    time_seconds, time_minutes, time_hours, time_days, time_in_years, time_in_centuries = calculate_brute_force_time(
        key_length)
    print("\nBrute force cracking time for key length", key_length, "bits:")
    print("Time in seconds:", time_seconds)
    print("Time in minutes:", time_minutes)
    print("Time in hours:", time_hours)
    print("Time in days:", time_days)
    print("Time in years:", time_in_years)
    print("Time in centuries:", time_in_centuries)

    # --- Part 3: Estimating Encryption/Decryption Speed ---
    enc_speed = int(input("\nEnter desired encryption speed (keys per second): "))
    dec_speed = int(input("Enter desired decryption speed (keys per second): "))
    message_size = 1024  # Assuming a message size of 1024 bits for this example

    enc_time, dec_time = estimate_enc_dec_time(message_size, enc_speed, dec_speed)
    print("\nEstimated encryption time:", enc_time, "seconds")
    print("Estimated decryption time:", dec_time, "seconds")

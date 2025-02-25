from cryptography.hazmat.primitives.asymmetric import rsa, dh, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from decimal import Decimal, getcontext
import os


# Objective:
# The goal of this exercise is to help students gain hands-on experience with public key
# encryption schemes. Students will create a script that generates public and private
# keys, calculates the time it would take a supercomputer to crack the encryption, and
# customize their encryption system based on given requirements. Students will also
# implement a unique feature to improve security, speed, or usability.

# pip install cryptography

# The idea of the customization is that two parties use a symmetrical key as a session key
# that is discarded after the session. A DH key exchange is used to calculate a shared secret
# from the each other's DH public key. This shared secret is then used to create a symmetrical key. 
# This symmetrical key is the session key that is discarded after communication is complete. 
# Both parties sign their DH public key with their RSA private key to confirm their identity.

def generate_dh_parameters():
    """Generate DH parameters once for both parties."""
    return dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())


def generate_dh_keypair(parameters):
    """Generate DH key pair using common parameters."""
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


# ======== SIGN DATA WITH RSA =========
def sign_data(private_key, data):
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify_signature(public_key, signature, data):
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False

    # ======== KEY DERIVATION FUNCTION (HKDF) =========
    """Derives session key from shared secret"""


def derive_session_key(shared_secret):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,  # AES-256 key
        salt=None,
        info=b"Diffie-Hellman key exchange",
        backend=default_backend()
    )
    return hkdf.derive(shared_secret)


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
    public_rsa = key.public_key()
    private_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_pem = public_rsa.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return key, public_rsa, private_pem, public_pem


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
    private_rsa_A, public_rsa_A, private_rsa_A_pem, public_rsa_A_pem = generate_key_pair(key_length)
    private_rsa_B, public_rsa_B, private_rsa_B_pem, public_rsa_B_pem = generate_key_pair(key_length)

    dh_parameters = generate_dh_parameters()

    # Generate DH key pairs
    private_dh_A, public_dh_A = generate_dh_keypair(dh_parameters)
    private_dh_B, public_dh_B = generate_dh_keypair(dh_parameters)

    # Serialize DH public keys
    public_dh_pem_A = public_dh_A.public_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)
    public_dh_pem_B = public_dh_B.public_bytes(encoding=serialization.Encoding.PEM,
                                               format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # Sign DH public keys with RSA
    signature_A = sign_data(private_rsa_A, public_dh_pem_A)
    signature_B = sign_data(private_rsa_B, public_dh_pem_B)

    # Verify signatures
    assert verify_signature(public_rsa_A, signature_A, public_dh_pem_A), "RSA Signature Verification Failed for A"
    assert verify_signature(public_rsa_B, signature_B, public_dh_pem_B), "RSA Signature Verification Failed for B"
    print("\n RSA Signatures Verified Successfully!")

    # Perform key exchange
    shared_secret_A = private_dh_A.exchange(public_dh_B)
    shared_secret_B = private_dh_B.exchange(public_dh_A)

    # Ensure shared secrets match
    assert shared_secret_A == shared_secret_B, "Key exchange failed - Shared secrets do not match"

    # Derive session key
    session_key = derive_session_key(shared_secret_A)
    print(f"\n Diffie-Hellman Key Exchange Successful! Derived Session Key: {session_key.hex()}")

    # Display the keys
    print("\nPrivate Key A:\n", private_rsa_A_pem.decode())
    print("\nPrivate Key B:\n", private_rsa_B_pem.decode())
    print("\nPublic Key A:\n", public_rsa_A_pem.decode())
    print("\nPublic Key B:\n", public_rsa_B_pem.decode())

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

    # Securely discard session key
    del session_key
    session_key = None
    print("\n Session keys securely discarded.")
    print("\n Key exchange process completed successfully")
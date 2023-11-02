import hashlib
import os


def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)  # Gere um "salt" aleatório

    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt, password_hash


def generate_password_hash():
    password = input("Digite a senha: ")
    salt, password_hash = hash_password(password)
    print(f"Salt: {salt.hex()}")
    print(f"Hash da senha: {password_hash.hex()}")


if __name__ == "__main__":
    generate_password_hash()

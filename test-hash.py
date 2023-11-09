from passlib.hash import pbkdf2_sha256

passwd = input("Digite a senha: ")

def hash_password(password):
    return pbkdf2_sha256.using(rounds=8000, salt_size=16).hash(password)


print(hash_password(passwd))

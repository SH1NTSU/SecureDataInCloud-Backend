from cryptography.fernet import Fernet


def generate_key(filename):
    key = Fernet.generate_key()

    with open(f'key_{filename}', 'wb') as mykey:
        mykey.write(key)

    return key


def encrypt_file(filename):
    key = generate_key(filename)

    f = Fernet(key)

    with open(f'{filename}', 'rb') as original_file:
        original = original_file.read()

    encrypted = f.encrypt(original)

    with open(f'enc_{filename}', 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decrypt_file(filename):
    with open(f'key_{filename}', 'rb') as mykey:
        key = mykey.read()

    f = Fernet(key)

    with open(f'enc_{filename}', 'rb') as encrypted_file:
        encrypted = encrypted_file.read()

    decrypted = f.decrypt(encrypted)

    with open(f'dec_{filename}', 'wb') as decrypted_file:
        decrypted_file.write(decrypted)


encrypt_file('plik.txt')
decrypt_file('plik.txt')

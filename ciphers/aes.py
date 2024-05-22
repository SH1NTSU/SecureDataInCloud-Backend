from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os


class EncAndDecFile:
    def __init__(self, filename):
        self.filename = filename

    def generate_key(self):
        key = os.urandom(32)
        with open(f"key_{self.filename}", "wb") as key_file:
            key_file.write(key)
        return key

    def pad_data(self, data):
        block_size = 16
        padder = padding.PKCS7(block_size * 8).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def unpad_data(self, data):
        block_size = 16
        unpadder = padding.PKCS7(block_size * 8).unpadder()
        unpadded_data = unpadder.update(data) + unpadder.finalize()
        return unpadded_data

    def encrypt_file(self):
        key = self.generate_key()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(self.filename, "rb") as file:
            original_data = file.read()
        padded_data = self.pad_data(original_data)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        encrypted_filename = f"enc_{self.filename}"
        with open(encrypted_filename, "wb") as file:
            file.write(iv + encrypted_data)

        return key, encrypted_filename

    def decrypt_file(self, key, encrypted_filename):
        with open(encrypted_filename, "rb") as file:
            iv = file.read(16)
            encrypted_data = file.read()

        cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        decrypted_data = self.unpad_data(decrypted_padded_data)

        decrypted_filename = f"dec_{os.path.basename(encrypted_filename)}"
        with open(decrypted_filename, "wb") as file:
            file.write(decrypted_data)

        return decrypted_filename

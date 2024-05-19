from cryptography.fernet import Fernet
import os

class EncAndDecFile:
    def __init__(self, filename):
        self.filename = filename
        self.key = None

    def generate_key(self):
        self.key = Fernet.generate_key()

        with open(f'key_{self.filename}.key', 'wb') as mykey:
            mykey.write(self.key)

        return self.key

    def encrypt_file(self):
        key = self.generate_key()

        f = Fernet(key)

        with open(f'{self.filename}', 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        encrypted_filename = f'enc_{self.filename}'
        with open(encrypted_filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print(key)

        
        return key, encrypted_filename


    def decrypt_file(self, key, encrypted_filename):

        f = Fernet(key)

        with open(encrypted_filename, 'rb') as encrypted_file:  
            encrypted = encrypted_file.read()

        decrypted = f.decrypt(encrypted)

        decrypted_filename = f'dec_{os.path.basename(encrypted_filename)}'

        with open(decrypted_filename, 'w') as decrypted_file:  
            decrypted_file.write(decrypted)

        return decrypted_filename



from cryptography.fernet import Fernet


class EncAndDecFile:
    def __init__(self, filename):
        self.filename = filename
        self.key = None


    def generate_key(self):
        self.key = Fernet.generate_key()

        with open(f'key_{self.filename}', 'wb') as mykey:
            mykey.write(self.key)

        return self.key


    def encrypt_file(self):
        key = self.generate_key()

        f = Fernet(key)

        with open(f'{self.filename}', 'rb') as original_file:
            original = original_file.read()

        encrypted = f.encrypt(original)

        with open(f'key_{self.filename}', 'rb') as key_file:
            key = key_file.read()

        with open(f'enc_{self.filename}', 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
        print(key)
        return key, f"{self.filename}"
    


    def decrypt_file(self, key, file_name):
        
        f = Fernet(key)

        with open(f'{file_name}', 'rb') as encrypted_file:
            encrypted = encrypted_file.read()

        decrypted = f.decrypt(encrypted)

        with open(f'dec_{self.filename}', 'wb') as decrypted_file:
            decrypted_file.write(decrypted)

        return decrypted_file

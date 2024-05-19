
import random
import ast

class ECC:
    def __init__(self):
        self.a = 0
        self.b = 7
        self.G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
                  32670510020758816978083085130507043184471273380659243275938904335757337482424)
        self.p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - 1
        self.n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

    def add_points(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 == y2:
            beta = (3 * x1 * x1 + self.a) * pow(2 * y1, -1, self.p)
        else:
            beta = (y2 - y1) * pow(x2 - x1, -1, self.p)

        x3 = (beta * beta - x1 - x2) % self.p
        y3 = (beta * (x1 - x3) - y1) % self.p

        return x3, y3
    
    
    def double_point(self, P):
        if P is None:
            return None

        x, y = P
        denominator = 2 * y % self.p
        if denominator == 0:
            return None  # The point is at infinity
        lam = (3 * x * x + self.a) * pow(denominator, -1, self.p)
        x_res = (lam * lam - 2 * x) % self.p
        y_res = (lam * (x - x_res) - y) % self.p
        return x_res, y_res

    def scalar_mult(self, k, P):
        if k == 0:
            return (0, 0)
        
        result = (0, 0)
        Q = P

        for bit in bin(k)[2:]:
            result = self.double_point(result)

            if bit == '1':
                result = self.add_points(result, Q)

        return result

    def generate_keys(self):
        private_key = random.randint(1, self.n - 1)
        public_key = self.scalar_mult(private_key, self.G)
        return private_key, public_key



class EncAndDecFile(ECC):
    def __init__(self, filename, recipient_public_key=None, private_key=None):
        super().__init__()
        self.filename = filename
        self.recipient_public_key = recipient_public_key
        self.private_key = private_key

    def encrypt(self):
        if self.recipient_public_key is None:
            raise ValueError("Recipient public key is required for encryption.")

        with open(self.filename, 'r') as org_file:
            org_text = org_file.read().strip()

        enc_text = []
        for char in org_text:
            m = ord(char)

            # Handle potential point at infinity
            while True:
                r = random.randint(1, self.n - 1)
                s = self.scalar_mult(m, self.G)
                if s != (0, 0):  # Check if s is not the point at infinity
                    break

            c1 = self.scalar_mult(r, self.G)
            c2 = self.add_points(self.scalar_mult(r, self.recipient_public_key), s)

            # Store the coordinates of c1 and c2 in a single string, separated by a comma
            enc_text.append(f'{c1},{c2}')

        with open(f'enc_{self.filename}', 'w') as enc_file:
            for item in enc_text:
                enc_file.write(f'{item}\n')

    def decrypt(self):
        if self.private_key is None:
            raise ValueError("Private key is required for decryption.")

        with open(f'enc_{self.filename}', 'r') as enc_file:
            enc_text = [line.strip() for line in enc_file]

        print(f"Number of lines in the encrypted file: {len(enc_text)}")

        dec_text = []

        for item in enc_text:
            # Split the string into c1 and c2 coordinates using a comma as delimiter
            parts = item.split(',')
            if len(parts) != 2:
                continue  # Skip malformed entries

            c1_str, c2_str = parts
            # Parse the coordinates as integers
            c1 = tuple(map(int, c1_str.strip('()').split()))
            c2 = tuple(map(int, c2_str.strip('()').split()))

            c1_prime = self.scalar_mult(self.private_key, c1)
            s_prime = self.add_points(c2, self.scalar_mult(-self.private_key, c1_prime))

            # Adjust modulo value or use a different encoding scheme if needed
            plaintext_char = chr(s_prime[0] % modulo_value)
            print(f"Decrypted integer: {s_prime[0]}")  # Add this line
            print(f"Decrypted character: {plaintext_char}")
            if not plaintext_char:
                print(f"Skipping character with integer value: {s_prime[0]}")
            dec_text.append(plaintext_char)

        dec_text = ''.join(dec_text)

        print(f"Decrypted text: {dec_text}")

        with open(f'dec_{self.filename}', 'w', encoding='utf-8') as dec_file:
            dec_file.write(dec_text)

if __name__ == "__main__":
    # Generate keys for encryption and decryption
    ecc = ECC()
    private_key, public_key = ecc.generate_keys()

    # Create a sample file to encrypt
    with open('plik.txt', 'w') as f:
        f.write('Hello, this is a test.')

    # Encrypt the file
    encryptor = EncAndDecFile('plik.txt', recipient_public_key=public_key)
    encryptor.encrypt()

    # Decrypt the file
    decryptor = EncAndDecFile('plik.txt', private_key=private_key)
    decryptor.decrypt()

    print("Encryption and Decryption completed successfully.")




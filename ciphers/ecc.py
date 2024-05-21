import random
import ast


class ECC:
    def __init__(self):
        self.a = 0
        self.b = 7
        self.G = (55066263022277343669578718895168534326250603453777594175500187360389116729240,
                  32670510020758816978083085130507043184471273380659243275938904335757337482424)
        self.p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
        self.n = 115792089237316195423570985008687907852837564279074904382605163141518161494337


    def add_points(self, P, Q, p):
        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 == y2:
            beta = (3 * x1 * x2 + self.a) * pow(2 * y1, -1, p)
        else:
            beta = (y2 - y1) * pow(x2 - x1, -1, p)

        x3 = (beta * beta - x1 - x2) % p
        y3 = (beta * (x1 - x3) - y1) % p

        self.is_on_curve((x3, y3), p)

        return x3, y3


    def is_on_curve(self, P, p):
        x, y = P
        return (y * y) % p == (pow(x, 3, p) + self.a * x + self.b) % p


    def apply_double_and_add_method(self, G, k, p):
        target_point = G

        k_binary = bin(k)[2:]

        for i in range(1, len(k_binary)):
            current_bit = k_binary[i: i + 1]

            target_point = self.add_points(target_point, target_point, p)

            if current_bit == '1':
                target_point = self.add_points(target_point, G, p)

        self.is_on_curve(target_point, p)

        return target_point


    def keys(self):
        ka = random.getrandbits(256)
        Qa = self.apply_double_and_add_method(G=self.G, k=ka, p=self.p)
        return ka, Qa


class EncAndDecFile(ECC):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename


    def encrypt(self):
        ka, Qa = self.keys()

        with open(self.filename, 'r') as org_file:
            org_text = org_file.read().strip()

        enc_text = []

        for char in org_text:
            m = ord(char)
            s = self.apply_double_and_add_method(G=self.G, k=m, p=self.p)

            r = random.getrandbits(128)
            c1 = self.apply_double_and_add_method(G=self.G, k=r, p=self.p)

            c2 = self.apply_double_and_add_method(G=Qa, k=r, p=self.p)
            c2 = self.add_points(c2, s, self.p)

            enc_text.append(f'({c1}, {c2})')

        with open(f'enc_{self.filename}', 'w') as enc_file:
            for item in enc_text:
                enc_file.write(f'{item}\n')


    def decrypt(self):
        ka, Qa = self.keys()

        with open(f'enc_{self.filename}', 'r') as enc_file:
            enc_text = [ast.literal_eval(line.strip()) for line in enc_file]

        dec_text = []

        for item in enc_text:
            c1, c2 = item

            c1_prime = c1[0], (-1 * c1[1]) % self.p

            s_prime = self.apply_double_and_add_method(G=c1_prime, k=ka, p=self.p)
            s_prime = self.add_points(P=c2, Q=s_prime, p=self.p)

            dec_text.append(chr(int(s_prime[0]) % 0x110000))

        dec_text = ''.join(dec_text)

        with open(f'dec_{self.filename}', 'w', encoding='utf-8') as dec_file:
            dec_file.write(dec_text)

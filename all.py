import random


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
        assert (y * y) % p == (pow(x, 3, p) + self.a * x + self.b) % p


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

ecc = ECC()
ecc.is_on_curve(ecc.G, ecc.p)


def encrypt_file(filename, G, Qa):
    with open(filename, 'r') as file:
        text = file.read()
        text_to_int = [int(i) for i in text.split()]

    m = text_to_int
    s = ecc.apply_double_and_add_method(G=G, k=m, p=p)

    r = random.getrandbits(128)
    c1 = ecc.apply_double_and_add_method(G=G, k=r, p=p)

    c2 = ecc.apply_double_and_add_method(G=Qa, k=r, p=p)
    c2 = ecc.add_points(c2, s, p)

    with open('encrypted.txt', 'w') as file:
        file.write(str(c1, c2))


ka = random.getrandbits(256)
Qa = ecc.apply_double_and_add_method(G=ecc.G, k=ka, p=p)
encrypted_file = encrypt_file(r"C:\Users\MarcelBudziszewski\SecureDataInCloud-Backend\hei.txt", G, Qa)
print(encrypted_file)

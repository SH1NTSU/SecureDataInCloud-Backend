import random
from ecc_for_files.ecc import ECC


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
Qa = ecc.apply_double_and_add_method(G=ecc.G, k=ka, p=ecc.p)
encrypt_file("plik.txt", ecc.G, Qa)

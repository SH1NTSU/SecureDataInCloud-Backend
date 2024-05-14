import random
from ecc_for_files.ecc import ECC


ecc = ECC()
ecc.is_on_curve(G, p)


def decrypt_file(filename, ka):
    with open(filename, 'r') as file:
        c1, c2 = eval(file.read().strip())
    c1_prime = c1[0], (-1 * c1[1]) % ecc.p
    s_prime = ecc.apply_double_and_add_method(G=c1_prime, k=ka)
    s_prime = ecc.add_points(P=c2, Q=s_prime)
    text = number_to_text(s_prime[0])
    with open('decrypted.txt', 'w', encoding='utf-8') as file:
        file.write(text)


ka = random.getrandbits(256)
decrypt_file('encrypted.txt', ka)

import random
from utils import *

class NoiselessPubKey:
    def __init__(self, n, q):
        self.n = n
        self.q = q
    def key_gen(self):
        A = sample_unif_matrix(self.n, self.q)
        self.sk = sample_unif_vector(self.n, self.q)
        As = matrix_vector_multiply(A, self.sk, self.q)
        self.pk = (A, As)

    def enc(self, m):
        (A, As) = self.pk
        # Sampling r
        r = sample_unif_vector(n, self.q)
        # Computing u := A^tr
        At = matrix_transpose(A)
        u = matrix_vector_multiply(At, r, self.q)
        # Computing r^t(As)
        rAs = vector_vector_inner_product(r, As, self.q)
        # Using r^t(As) as a random pad
        v = (rAs + m) % self.q
        return (u, v)

    def dec(self, ctxt):
        (u, v) = ctxt[0], ctxt[1]
        s = self.sk
        # Computing (r^tA)s
        rAs = vector_vector_inner_product(u, s, self.q)
        # Subtracting rAs from v
        m = (v - rAs) % q
        return m


if __name__ == "__main__":
    import time
    q = 3000
    n = 1000
    B = 10
    E = NoiselessPubKey(n,q)
    t= time.time()
    E.key_gen()
    t_keys = time.time()
    print(f"Generating keys took {t_keys-t} sec")
    m = random.randint(0,1)
    print("Encrypting Random message:")
    t = time.time()
    c =E.enc(m)
    t_enc =time.time()
    print(f"Encrypting took: {t_enc-t} sec")
    t = time.time()
    m_prime = E.dec(c)
    t_dec = time.time()
    print(f"Decrypting took: {t_dec-t} sec")
    # check encryption was correct
    assert m == m_prime
    print("Decryption was correct")

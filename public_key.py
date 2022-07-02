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
        r = sample_unif_vector(self.n, self.q)
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

class LWEPubKey:
    def __init__(self, n, q, B):
        self.n = n
        self.q = q
        self.B = B

    def key_gen(self):
        A = sample_unif_matrix(self.n, self.q)
        self.sk = sample_bounded_vector(self.n, self.B)
        As = matrix_vector_multiply(A, self.sk, self.q)
        e = sample_bounded_vector(self.n, self.B)
        b = vector_vector_add(As, e, self.q)
        self.pk = (A, b)

    def enc(self, m):
        (A, b) = self.pk
        # Sampling r
        r = sample_bounded_vector(self.n, self.B)
        e_prime = sample_bounded_vector(self.n, self.B)
        # Computing u := A^tr + e'
        At = matrix_transpose(A)
        u = matrix_vector_multiply(At, r, self.q)
        u = vector_vector_add(u, e_prime, self.q)
        # Approximately computing r^t(As)
        rAs = vector_vector_inner_product(r, b, self.q)
        # Adding e_double_prime so it is a "LWE encryption"
        e_prime_prime = sample_bounded_vector(1, self.B)[0]
        v = rAs+ e_prime_prime % self.q
        # Adding an encoding of m to the "random pad"
        v = (v + (self.q//2)*m) % self.q
        return (u, v)

    def dec(self, ctxt):
        (u, v) = ctxt[0], ctxt[1]
        s = self.sk
        # Approximately (r^tA)s
        rAs = vector_vector_inner_product(u, s, self.q)
        # Subtracting rAs from v
        v = (v - rAs) % self.q
        # Decoding (q//2)*m + error_terms
        return round(v / (self.q//2)) % 2


if __name__ == "__main__":
    import time
    q = 3000
    n = 1000
    B = 5
    #E = NoiselessPubKey(n,q)
    E = LWEPubKey(n,q, B)
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

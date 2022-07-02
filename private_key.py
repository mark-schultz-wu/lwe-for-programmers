import random
from utils import *

class NoiselessPrivKey:
    def __init__(self, n, q):
        self.n = n
        self.q = q
    def key_gen(self):
        self.s = sample_unif_vector(self.n, self.q)

    def enc(self, m):
        # Sampling A
        A = sample_unif_matrix(n, self.q)
        # Computing b := As
        b = matrix_vector_multiply(A, self.s, self.q)
        # Adding m to As
        b = vector_vector_add(b, m, self.q)
        return (A, b)

    def dec(self, ctxt):
        (A, b) = ctxt[0], ctxt[1]
        # Recomputing As
        As = matrix_vector_multiply(A, self.s, self.q)
        # Recovering m = b - As
        for i in range(self.n):
            b[i] = (b[i] - As[i]) % q
        return b

class LWEPrivKey:
    def __init__(self, n, q, B):
        self.n = n
        self.q = q
        self.B = B
    def key_gen(self):
        self.s = sample_unif_vector(self.n, self.q)

    def enc(self, m):
        # Sampling A, e
        A = sample_unif_matrix(n, self.q)
        e = sample_bounded_vector(self.n, self.B)
        # Computing b := As + e
        b = matrix_vector_multiply(A, self.s, self.q)
        b = vector_vector_add(b, e, self.q)
        # Scaling m -> (q//2) m
        scaled_m = [(self.q//2) * m[i] % self.q for i in range(self.n)]
        # Adding (q//2)m to b = As + e
        b = vector_vector_add(b, scaled_m, self.q)
        return (A, b)

    def dec(self, ctxt):
        (A, b) = ctxt[0], ctxt[1]
        # Recomputing As
        As = matrix_vector_multiply(A, self.s, self.q)
        # Recovering scaled_m = b - As
        for i in range(self.n):
            b[i] = (b[i] - As[i]) % q
        # Scaling (q//2)m + e -> m
        m = [0 for _ in range(self.n)]
        for i in range(self.n):
            m[i] = round(b[i] / (self.q//2)) % 2
        return m

if __name__ == "__main__":
    import time
    q = 3000
    n = 1000
    B = 10
    # E = NoiselessPrivKey(n,q)
    E = LWEPrivKey(n,q, B)
    t= time.time()
    E.key_gen()
    t_keys = time.time()
    print(f"Generating keys took {t_keys-t} sec")
    m = [random.randint(0,1) for _ in range(n)]
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

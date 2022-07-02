import random
from utils import *

class LWEPrivKey:
    def __init__(self, n, q, B):
        self.n = n
        self.q = q
        self.B = B
    def key_gen(self):
        self.s = sample_unif_vector(self.n, self.q)

    def enc(self, m):
        # Sampling the various values
        A = sample_unif_matrix(n, self.q)
        e = sample_bounded_vector(self.n, self.B)
        # Computing b := As
        b = matrix_vector_multiply(A, self.s)
        b = self.LWE_func(A, self.s, e)
        # Adding a scaled copy of m to b
        for i in range(self.n):
            b[i] += m[i] * (q//2) % self.q
        return (A, b)

    def dec(self, ctxt):
        (A, b) = ctxt[0], ctxt[1]
        # Recomputing As and subtracting it from b:= As + (q/2)m + e to get (q/2)m + e
        for i in range(self.n):
            for k in range(self.n):
                b[i] -= A[i][k] * self.s[k] % self.q
        # Recovering m from (q/2)m + e
        m = [0 for _ in range(self.n)]
        for i in range(self.n):
            m[i] = round(b[i] / (q//2)) % 2
        return m

if __name__ == "__main__":
    import time
    q = 3000
    n = 1000
    B = 10
    E = LWEPrivKey(n,q,B)
    t= time.time()
    E.key_gen()
    t_keys = time.time()
    print(f"Generating keys took {t_keys-t} sec")
    m = [random.randint(0,1) for _ in range(n)]
    print("Encrypting Random message:")
    print(m)
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

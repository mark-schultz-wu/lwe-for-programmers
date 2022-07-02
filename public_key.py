import random
from private_key import sample_vector, sample_matrix, LWEPrivKey

def transpose(matrix):
    n = len(matrix)
    B = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            B[i][j] = matrix[j][i]
    return B

class LWEPubKey(LWEPrivKey):

    def key_gen(self):
        self.sk = sample_vector(self.n, -self.B, self.B)
        A = sample_matrix(self.n, self.q)
        e = sample_vector(self.n, -self.B, self.B)
        b = self.LWE_func(A, self.sk, e)
        self.pk = (A, b)

    # Only encrypts a single bit now
    def enc(self, m):
        # pk is As + e
        A, b = self.pk
        r = sample_vector(self.n, -self.B, self.B)
        other_e = sample_vector(self.n, -self.B, self.B)
        # other_share = A^tr + e' ~ r^t A + e'
        other_share = self.LWE_func(transpose(A), r, other_e)
        # pad = r^t (As + e) = r^tAs + r^t e
        pad = sum(r[i] * b[i] for i in range(n))
        # Adding a scaled copy of m to pad
        pad += m * (q//2) % self.q
        return (other_share, pad)


    def dec(self, ctxt):
        other_share, pad = ctxt[0], ctxt[1]
        A, b = self.pk
        s = self.sk
        # pad is r^t A s + (small terms) + (q/2)m
        # other_share is r^t A + e'
        rAs = sum(other_share[i] * s[i] for i in range(n))
        pad -= rAs
        return round(pad / (self.q//2)) % 2

if __name__ == "__main__":
    import time
    q = 3000
    n = 1000
    B = 10
    E = LWEPubKey(n,q,B)
    t= time.time()
    E.key_gen()
    t_keys = time.time()
    print(f"Generating keys took {t_keys-t} sec")
    m = random.randint(0,1)
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

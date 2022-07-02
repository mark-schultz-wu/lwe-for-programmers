import random

class LWEPrivKey:
    def __init__(self, n, q, B):
        self.n = n
        self.q = q
        self.B = B
    def key_gen(self):
        self.s = [random.randint(0,self.q) for _ in range(self.n)]

    def enc(self, m):
        A = [[random.randint(0,self.q) for _ in range(self.n)] for _ in range(self.n)]
        e = [random.randint(-self.B, self.B) for _ in range(self.n)]
        # Computing b := As + e
        b = [0 for _ in range(self.n)]
        for i in range(self.n):
            b[i] += sum(A[i][k] * self.s[k] % self.q for k in range(self.n)) % self.q
            b[i] += e[i] % self.q
        # (A, b) is indistinguishable from random under the LWE assumption.
        for i in range(self.n):
            b[i] += m[i] * (q//2) % self.q
        return (A, b)

    def dec(self, ctxt):
        (A, b) = ctxt[0], ctxt[1]
        # Recomputing As and subtracting it from b:= As + (q/2)m + e to get (q/2)m + e
        for i in range(self.n):
            b[i] -= sum(A[i][k] * self.s[k] for k in range(self.n))
        # Recovering m from (q/2)m + e
        m = [0 for _ in range(self.n)]
        for i in range(self.n):
            m[i] = round(b[i] / (q//2)) % 2
        return m

if __name__ == "__main__":
    q = 3000
    n = 1000
    B = 10
    E = LWEPrivKey(n,q,B)
    E.key_gen()
    # generate a random message
    m = [random.randint(0,1) for _ in range(n)]
    c =E.enc(m)
    m_prime = E.dec(c)
    # check encryption was correct
    assert m == m_prime

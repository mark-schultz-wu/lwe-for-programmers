import random

# matrices assumed to be square

def sample_unif_vec(n, q):
    return [random.randint(0, q-1) for _ in range(n)]

def sample_bounded_vec(n, B):
    return [random.randint(-B, B) for _ in range(n)]

def sample_unif_matrix(n, q):
    return [sample_unif_vec(n,q) for _ in range(n)]

def matrix_vector_multiply(m, v):
    return [sum(m[i][j] * v[j] for j in range(n)) for i in range(n)]

def matrix_transpose(m):
    n = len(m)
    return [[m[i][j] for i in range(n)] for j in range(n)]

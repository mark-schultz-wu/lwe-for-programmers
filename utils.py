import random

# matrices assumed to be square

def sample_unif_vec(n, q):
    return [random.randint(0, q-1) for _ in range(n)]

def sample_bounded_vec(n, B):
    return [random.randint(-B, B) for _ in range(n)]

def sample_unif_matrix(n, q):
    return [sample_unif_vec(n,q) for _ in range(n)]

def sample_bounded_matrix(n, B):
    return [sample_bounded_vec(n,B) for _ in range(n)]

def matrix_vector_multiply(m, v):
    n = len(m)
    return [sum(m[i][j] * v[j] for j in range(n)) for i in range(n)]

def matrix_matrix_multiply(m, v):
    n = len(m)
    return [[sum(m[i][j] * v[j][k] for j in range(n)) for i in range(n)] for k in range(n)]

def matrix_transpose(m):
    n = len(m)
    return [[m[i][j] for i in range(n)] for j in range(n)]

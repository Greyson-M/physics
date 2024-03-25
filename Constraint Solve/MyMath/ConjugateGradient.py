import numpy as np

def conjugate_gradient(coeffs, b, x0):
    r = b - np.dot(coeffs, x0)
    p = r
    rold = np.dot(r, r)

    for i in range(len(b)):
        Ap = np.dot(coeffs, p)
        alpha = rold / np.dot(p, Ap)
        x0 = x0 + alpha * p
        r = r - alpha * Ap
        rnew = np.dot(r, r)

        if np.sqrt(rnew) < 1e-10:
            break

        beta = rnew / rold
        p = r + beta * p
        rold = rnew

    return x0

if __name__ == '__main__':
    coeffs = np.array([[1, 1], [0, 1]])
    b = np.array([1, 2])
    x0 = np.array([0, 0])
    x = conjugate_gradient(coeffs, b, x0)
    print(x)
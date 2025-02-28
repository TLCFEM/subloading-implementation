import numpy as np


def U(x):
    return pow(x, -2)


def dU(x):
    return -2 * pow(x, -3)


def compute():
    x = 1e-17

    jacobian = np.ones((2, 2))

    result = []
    for _ in range(20):
        jacobian[1, 0] = U(x)
        jacobian[1, 1] = x * dU(x) / U(x) - 1
        result.append((x, 1.0 / np.linalg.cond(jacobian)))

        x = x * 10

    return result


if __name__ == "__main__":
    np.savetxt("pow4.txt", np.array(compute()))

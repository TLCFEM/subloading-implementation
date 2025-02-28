import numpy as np
from scipy.integrate import solve_ivp

slope = 0.05

def f(t, y):
    return 1 - y / (slope * t + 1)


if __name__ == "__main__":
    sol = solve_ivp(f, [0, 10], [0], dense_output=True)
    t = np.linspace(0, 10, 101, endpoint=True)
    y = sol.sol(t).T
    joined = np.concatenate((t.reshape(-1, 1), y), axis=1)
    np.savetxt("hardening.inverse.txt", joined, delimiter=" ")

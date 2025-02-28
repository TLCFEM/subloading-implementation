import os
import subprocess
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


def norm(s):
    s = np.square(s)
    s[3:] = 2 * s[3:]
    return np.sqrt(np.sum(s))


yield_stress = 100
young_modulus = 2e5


def generate_main():
    with open("isomap.sp", "w") as f:
        f.write(f"""
material SubloadingMetal 1 {young_modulus} 0.2 \
{yield_stress} 2E3 0 0 \
0 0 0 0 \
5E2 0 0 0

materialtestbystrainhistory 1 hist

exit
""")


base_num = 500


def generate_base(size: float):
    num = base_num
    base_strain = np.linspace(0, size, num + 1, endpoint=True)
    strain = np.zeros((num, 6))
    strain[:, 0] = base_strain[1:]
    strain[:, 1] = base_strain[1:]
    return strain


def generate_increment(dx, dy):
    num = 200
    x = np.linspace(0, dx, num + 1, endpoint=True)
    y = np.linspace(0, dy, num + 1, endpoint=True)

    strain = np.zeros((num, 6))
    strain[:, 0] = x[1:]
    strain[:, 1] = y[1:]
    return strain


counter = 0


def run_analysis(strain):
    global counter
    np.savetxt("hist", strain)

    if os.path.exists("RESULT.txt"):
        os.remove("RESULT.txt")

    result = subprocess.run(
        ["suanpan", "-f", "isomap.sp"], capture_output=True, text=True
    )

    if "[ERROR]" in result.stdout:
        np.savetxt(f"error{counter}", strain)
        counter += 1

    while not os.path.exists("RESULT.txt"):
        sleep(0.01)

    stress = np.loadtxt("RESULT.txt")

    return stress[base_num - 1, :], stress[-1, :]


def plot():
    if os.name != "posix":
        print("This script only works on linux.")
        return

    if subprocess.run(["which", "suanpan"]).returncode != 0:
        print("suanPan not found, please install it first.")
        return

    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    os.chdir("tmp")

    generate_main()

    base_strain = 2e-3

    base = generate_base(base_strain)

    x = np.array(range(-30, 31)) * 5e-5

    ex_grid, ey_grid = np.meshgrid(x, x)

    grid = np.zeros((len(x), len(x)))
    abs_grid = np.zeros((len(x), len(x)))

    index = 0

    for i in range(len(x)):
        for j in range(len(x)):
            index += 1
            print(f"{index}/{grid.size}")
            ex, ey = x[i], x[j]
            increment = generate_increment(ex, ey)
            increment += base[-1, :]

            _, ref_stress = run_analysis(np.vstack((base, increment)))

            _, coarse_stress = run_analysis(np.vstack((base, increment[-1, :])))

            diff = ref_stress - coarse_stress

            abs_grid[i, j] = norm(diff)
            grid[i, j] = norm(diff) / norm(ref_stress) * 100

    ex_grid *= young_modulus / yield_stress
    ey_grid *= young_modulus / yield_stress

    plt.figure()
    contour = plt.contourf(ex_grid, ey_grid, grid, levels=20, cmap="coolwarm")
    plt.colorbar(contour)
    contour = plt.contour(
        ex_grid, ey_grid, grid, levels=20, colors="black", linewidths=0.2
    )
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon^i$")
    plt.ylabel("$\\Delta{}\\varepsilon_y/\\varepsilon^i$")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()
    plt.savefig("error.iso.biaxial.pdf")

    plt.figure()
    contour = plt.contourf(ex_grid, ey_grid, abs_grid, levels=20, cmap="coolwarm")
    plt.colorbar(contour)
    contour = plt.contour(
        ex_grid, ey_grid, abs_grid, levels=20, colors="black", linewidths=0.2
    )
    plt.clabel(contour, inline=True, fontsize=8)
    plt.xlabel("$\\Delta{}\\varepsilon_x/\\varepsilon^i$")
    plt.ylabel("$\\Delta{}\\varepsilon_y/\\varepsilon^i$")
    plt.gca().set_aspect("equal", adjustable="box")
    plt.tight_layout()
    plt.savefig("abs.error.iso.biaxial.pdf")


if __name__ == "__main__":
    plot()

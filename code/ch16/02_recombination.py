r"""Recombination of hydrogen in the expanding universe, from the Saha equation.

Question. Section "The microwave background" derives the Saha equation for the ionised fraction x
of hydrogen. At what redshift and temperature does x fall through one half, and why so much
below the 158 000 K that matches the ionisation energy?

Computes, with T = T0 (1 + z), T0 = 2.7255 K, and hydrogen density n_H = (1 - Y) eta n_gamma
(eta = 6.1e-10 baryons per photon, Y = 0.245, n_gamma = 411e6 m^-3 (1 + z)^3):
  x^2 / (1 - x) = (1 / n_H) (m_e k T / (2 pi hbar^2))^(3/2) exp(-B / k T),  B = 13.6057 eV,
  - x(z) from z = 600 to 2000,
  - the redshift and temperature where x = 1/2, and B/(k T) there,
  - for comparison, the temperature where k T = B (no photon excess).

Writes
  results/ch16/saha_x_of_z.dat   columns: z, x
  results/ch16/recombination.tex LaTeX number macros
"""
import os
import numpy as np
from scipy.optimize import brentq

out = os.path.join("results", "ch16")
os.makedirs(out, exist_ok=True)

kB, hbar, me, eV = 1.380649e-23, 1.054571817e-34, 9.1093837e-31, 1.602176634e-19
T0, eta, Y = 2.7255, 6.1e-10, 0.245
B = 13.6057 * eV
n_gamma0 = 411e6


def rhs(z):
    T = T0 * (1 + z)
    nH = (1 - Y) * eta * n_gamma0 * (1 + z) ** 3
    return (me * kB * T / (2 * np.pi * hbar**2)) ** 1.5 * np.exp(-B / (kB * T)) / nH


def x_of(z):
    s = rhs(z)
    # x^2 / (1 - x) = s  ->  x = (-s + sqrt(s^2 + 4 s)) / 2
    return (-s + np.sqrt(s * s + 4 * s)) / 2


zs = np.linspace(600, 2000, 281)
np.savetxt(os.path.join(out, "saha_x_of_z.dat"), np.column_stack([zs, [x_of(z) for z in zs]]), fmt="%.6f")

z_half = brentq(lambda z: x_of(z) - 0.5, 800, 2500)
T_half = T0 * (1 + z_half)
def tex_number(s):
    """1.58e+05 -> 1.58\\times10^{5} for use in math mode."""
    if "e" not in s:
        return s
    mant, exp = s.split("e")
    return f"{mant}\\times10^{{{int(exp)}}}"


macros = {
    "SixteenZhalf": f"{z_half:.0f}",
    "SixteenThalf": f"{T_half:.0f}",
    "SixteenBoverkT": f"{B / (kB * T_half):.1f}",
    "SixteenTionise": f"{B / kB:.3g}",
    "SixteenXatThousand": f"{x_of(1090):.2g}",
}
with open(os.path.join(out, "recombination.tex"), "w") as fh:
    for k, v in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{tex_number(v)}}}\n")
for k, v in macros.items():
    print(f"{k:22s} {v}")

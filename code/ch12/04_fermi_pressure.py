r"""Pressure of a fermion gas at fixed temperature, from thin and hot to dense and degenerate.

Question. Section "Pressure, Opacity and Burning" says degeneracy pressure is ordinary gas pressure,
the same pressure integral with a different occupation number. Does one Fermi-Dirac calculation run
smoothly from P = n k_B T to P ~ n^{5/3}?

Reads   nothing.

Computes, for slow (non-relativistic) spin-1/2 fermions at fixed T, in the units
  x = p / sqrt(2 m k_B T),  f(x) = 1 / (exp(x^2 - eta) + 1),  N0 = 8 pi (2 m k_B T)^{3/2} / h^3,
  n / N0      = int x^2 f dx                (density),
  P / (N0 kT) = (2/3) int x^4 f dx          (pressure integral, p v = 2 k_B T x^2),
  E_F / k_B T = (3 n / N0)^{2/3}            (Fermi energy of the same density),
over eta from -12 to 60; trapezoid rule on x in [0, sqrt(max(eta,0)) + 12] with 20000 points.
Limits: classical P = n k_B T; degenerate P = (2/5) n E_F = (2/15) (3 n/N0)^{5/3} N0 k_B T.

Writes
  results/ch12/fermi_pressure.dat   log10(n/N0), log10(P/(N0 kT)), log10 of the two limits, E_F/kT
"""
import os
import numpy as np

out = os.path.join("results", "ch12")
os.makedirs(out, exist_ok=True)

etas = np.linspace(-12, 60, 721)
rows = []
for eta in etas:
    x = np.linspace(0, np.sqrt(max(eta, 0.0)) + 12, 20000)
    f = 1 / (np.exp(np.clip(x**2 - eta, -700, 700)) + 1)
    n = np.trapezoid(x**2 * f, x)
    P = (2 / 3) * np.trapezoid(x**4 * f, x)
    EF = (3 * n) ** (2 / 3)
    rows.append((np.log10(n), np.log10(P), np.log10(n), np.log10((2 / 15) * (3 * n) ** (5 / 3)), EF))
rows = np.array(rows)
np.savetxt(os.path.join(out, "fermi_pressure.dat"), rows, fmt="%.5f",
           header="log10 n/N0, log10 P/(N0 kT), log10 classical, log10 degenerate, E_F/kT")

# self-check: P -> n kT in the thin limit and P -> (2/5) n E_F in the dense limit
assert abs(rows[0, 1] - rows[0, 2]) < 1e-3, rows[0]
assert abs(rows[-1, 1] - rows[-1, 3]) < 0.01, rows[-1]
i = np.argmin(np.abs(rows[:, 4] - 1))
print(f"E_F = kT at log10 n/N0 = {rows[i, 0]:.2f}; P/(n kT) there = {10**(rows[i, 1] - rows[i, 0]):.2f}")
print("self-check ok")

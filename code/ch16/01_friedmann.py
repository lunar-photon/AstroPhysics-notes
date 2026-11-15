r"""Expansion history of a flat universe with matter, radiation and a cosmological constant.

Question. Section "The Friedmann equation" derives H^2 = H0^2 [Om a^-3 + Or a^-4 + OL]. How old is
such a universe, when did each component dominate, and how does a(t) compare with the
single-component solutions?

Computes, for Planck 2018 parameters (H0 = 67.4 km/s/Mpc, Om = 0.315, Or = 9.1e-5, OL = 1 - Om - Or):
  - t(a) = int_0^a da' / (a' H(a')), the age t0 = t(1), and the curve a(t),
  - the single-component curves: matter only a = (3 H0 t / 2)^(2/3), radiation only
    a = (2 H0 t)^(1/2), Lambda only a = exp(H0 t), each with H0 set to the same value,
  - redshifts of matter-radiation equality and matter-Lambda equality, the redshift where the
    expansion starts to accelerate, the deceleration parameter today,
  - the comoving distance to z = 1 and the luminosity distance there.

Writes
  results/ch16/a_of_t_lcdm.dat, a_of_t_matter.dat, a_of_t_radiation.dat, a_of_t_lambda.dat
       columns: t (Gyr), a
  results/ch16/friedmann.tex   LaTeX number macros
"""
import os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

out = os.path.join("results", "ch16")
os.makedirs(out, exist_ok=True)

Mpc = 3.0857e22
Gyr = 3.15576e16
c = 2.99792458e8
H0_kms = 67.4
H0 = H0_kms * 1e3 / Mpc          # 1/s
Om, Or = 0.315, 9.1e-5
OL = 1.0 - Om - Or


def H(a):
    return H0 * np.sqrt(Om / a**3 + Or / a**4 + OL)


def t_of(a):
    """Cosmic time at scale factor a, in seconds."""
    return quad(lambda x: 1.0 / (x * H(x)), 0.0, a, limit=200, epsabs=0, epsrel=1e-10)[0]


t0 = t_of(1.0)
a_grid = np.concatenate([np.logspace(-4, -1, 60), np.linspace(0.101, 2.0, 160)])
t_grid = np.array([t_of(a) for a in a_grid]) / Gyr
np.savetxt(os.path.join(out, "a_of_t_lcdm.dat"), np.column_stack([t_grid, a_grid]), fmt="%.6f")

tt = np.linspace(0.0, 30.0, 300) * Gyr
np.savetxt(os.path.join(out, "a_of_t_matter.dat"),
           np.column_stack([tt / Gyr, (1.5 * H0 * tt) ** (2 / 3)]), fmt="%.6f")
np.savetxt(os.path.join(out, "a_of_t_radiation.dat"),
           np.column_stack([tt / Gyr, np.sqrt(2 * H0 * tt)]), fmt="%.6f")
tl = np.linspace(-30.0, 30.0, 300) * Gyr
np.savetxt(os.path.join(out, "a_of_t_lambda.dat"),
           np.column_stack([tl / Gyr + t0 / Gyr, np.exp(H0 * tl)]), fmt="%.6f")

z_eq_mr = Om / Or - 1.0
z_eq_mL = (OL / Om) ** (1 / 3) - 1.0
z_acc = (2 * OL / Om) ** (1 / 3) - 1.0                 # q = 0 when Om a^-3 / 2 = OL (radiation negligible)
q0 = Om / 2 + Or - OL
chi1 = quad(lambda z: c / H(1 / (1 + z)), 0, 1)[0]        # comoving distance to z = 1, m
dL1 = 2 * chi1

def tex_number(s):
    """1.58e+05 -> 1.58\\times10^{5} for use in math mode."""
    if "e" not in s:
        return s
    mant, exp = s.split("e")
    return f"{mant}\\times10^{{{int(exp)}}}"


macros = {
    "SixteenAge": f"{t0 / Gyr:.2f}",
    "SixteenHubbleTime": f"{1 / H0 / Gyr:.2f}",
    "SixteenAgeMatterOnly": f"{2 / (3 * H0) / Gyr:.2f}",
    "SixteenZeqMR": f"{z_eq_mr:.0f}",
    "SixteenZeqML": f"{z_eq_mL:.2f}",
    "SixteenZacc": f"{z_acc:.2f}",
    "SixteenQzero": f"{q0:.2f}",
    "SixteenDcomovingOne": f"{chi1 / Mpc:.0f}",
    "SixteenDlumOne": f"{dL1 / Mpc:.0f}",
    "SixteenOmegaL": f"{OL:.3f}",
    "SixteenTeqMRyr": f"{t_of(1 / (1 + z_eq_mr)) / (Gyr / 1e9):.3g}",
}
with open(os.path.join(out, "friedmann.tex"), "w") as fh:
    for k, v in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{tex_number(v)}}}\n")
for k, v in macros.items():
    print(f"{k:22s} {v}")

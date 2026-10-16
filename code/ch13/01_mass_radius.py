r"""Mass-radius relations of white dwarfs and neutron stars from degenerate Fermi gases.

Question. Section "White dwarfs" claims a maximum mass for stars held up by degenerate electrons,
and section "Computing a neutron star" claims that general relativity lowers the maximum mass of
a neutron star far below its Newtonian value. How large are these masses, and what do the
mass-radius curves look like?

Computes, for an ideal degenerate Fermi gas with x = p_F/(m c),
  P   = (pi m^4 c^5 / 3 h^3) [ x (2x^2 - 3) sqrt(1+x^2) + 3 asinh x ]
  eps = (pi m^4 c^5 /   h^3) [ x (2x^2 + 1) sqrt(1+x^2) -   asinh x ]   (energy density, rest mass included)
  - white dwarfs: electrons supply P, ions supply the mass, rho = mu_e m_H n_e, mu_e = 2;
    Newtonian hydrostatic equilibrium; one model per central x, from x_c = 0.01 to 300,
  - neutron stars made of an ideal neutron gas: Newtonian equilibrium (rho = m_n n) and the TOV
    equation (rho = eps/c^2 as the source of gravity), for x_c = 0.01 to 30,
  - the Chandrasekhar mass from the n = 3 polytrope formula, for comparison with the curve,
  - the radius of a 1.02 Msun white dwarf (Sirius B) on the curve.

Writes
  results/ch13/wd_MR.dat            R (1000 km)  M (Msun)
  results/ch13/ns_MR_tov.dat        R (km)       M (Msun)
  results/ch13/ns_MR_newton.dat     R (km)       M (Msun)
  results/ch13/mass_radius.tex      LaTeX macros
"""
import os
import numpy as np
from scipy.integrate import solve_ivp

out = os.path.join("results", "ch13")
os.makedirs(out, exist_ok=True)

G, c, h, hbar = 6.674e-11, 2.99792458e8, 6.62607015e-34, 1.054571817e-34
me, mn, mH, mu_amu = 9.1093837e-31, 1.67492750e-27, 1.6726e-27, 1.66053907e-27
Msun, Rsun = 1.989e30, 6.957e8
mu_e = 2.0


def fermi(m):
    """Return P(x), dP/dx(x), n(x), eps(x) for a degenerate gas of particles of mass m."""
    A = np.pi * m**4 * c**5 / (3 * h**3)

    def P(x):
        return A * (x * (2 * x**2 - 3) * np.sqrt(1 + x**2) + 3 * np.arcsinh(x))

    def dPdx(x):
        return 8 * A * x**4 / np.sqrt(1 + x**2)

    def n(x):
        return 8 * np.pi * (m * c * x) ** 3 / (3 * h**3)

    def eps(x):
        return 3 * A * (x * (2 * x**2 + 1) * np.sqrt(1 + x**2) - np.arcsinh(x))
    return P, dPdx, n, eps


def model(xc, P, dPdx, rho_source, rho_inertia=None, gr=False):
    """Integrate outward in r from the centre with x = p_F/(m c) as the variable; stop at x = 0."""
    if rho_inertia is None:
        rho_inertia = rho_source

    def rhs(r, y):
        x, mass = y
        x = max(x, 1e-12)
        rs, ri, p = rho_source(x), rho_inertia(x), P(x)
        if gr:
            dPdr = -G * (ri + p / c**2) * (mass + 4 * np.pi * r**3 * p / c**2) / (r**2 * (1 - 2 * G * mass / (r * c**2)))
        else:
            dPdr = -G * mass * ri / r**2
        return [dPdr / dPdx(x), 4 * np.pi * r**2 * rs]

    def surface(r, y):
        return y[0] - 1e-6 * xc
    surface.terminal, surface.direction = True, -1
    r0 = 1.0
    y0 = [xc, 4 / 3 * np.pi * r0**3 * rho_source(xc)]
    sol = solve_ivp(rhs, (r0, 1e9), y0, events=surface, rtol=1e-9, atol=[1e-12 * xc, 1e10],
                    max_step=np.inf, method="LSODA")
    R = sol.t_events[0][0] if sol.t_events[0].size else sol.t[-1]
    M = sol.y_events[0][0][1] if sol.t_events[0].size else sol.y[1][-1]
    return R, M


# white dwarfs
Pe, dPe, ne, _ = fermi(me)
rho_wd = lambda x: mu_e * mu_amu * ne(x)   # He, C, O: two atomic mass units per electron
wd = np.array([model(xc, Pe, dPe, rho_wd) for xc in np.logspace(-2, np.log10(300), 70)])
np.savetxt(os.path.join(out, "wd_MR.dat"), np.column_stack([wd[:, 0] / 1e6, wd[:, 1] / Msun]), fmt="%.6f")

# Chandrasekhar mass from the n = 3 polytrope: M = 4 pi omega3 (K/(pi G))^{3/2},
# K = (hc/8)(3/pi)^{1/3} / (mu_e mH)^{4/3}, omega3 = 2.01824
K_rel = (h * c / 8) * (3 / np.pi) ** (1 / 3) / (mu_e * mu_amu) ** (4 / 3)
M_ch = 4 * np.pi * 2.01824 * (K_rel / (np.pi * G)) ** 1.5

# Sirius B on the curve
order = np.argsort(wd[:, 1])
R_siriusB = np.interp(1.02 * Msun, wd[order, 1], wd[order, 0])

# neutron stars: ideal neutron gas
Pn, dPn, nn, epsn = fermi(mn)
rho_rest = lambda x: mn * nn(x)
rho_energy = lambda x: epsn(x) / c**2
xcs = np.logspace(-2, np.log10(30), 70)
ns_gr = np.array([model(xc, Pn, dPn, rho_energy, gr=True) for xc in xcs])
ns_nw = np.array([model(xc, Pn, dPn, rho_rest) for xc in xcs])
np.savetxt(os.path.join(out, "ns_MR_tov.dat"), np.column_stack([ns_gr[:, 0] / 1e3, ns_gr[:, 1] / Msun]), fmt="%.6f")
np.savetxt(os.path.join(out, "ns_MR_newton.dat"), np.column_stack([ns_nw[:, 0] / 1e3, ns_nw[:, 1] / Msun]), fmt="%.6f")

i_max = int(np.argmax(ns_gr[:, 1]))
macros = {
    "ThirteenMchFormula": f"{M_ch / Msun:.3f}",
    "ThirteenMwdLargest": f"{wd[:, 1].max() / Msun:.3f}",
    "ThirteenRsiriusB": f"{R_siriusB / 1e3:.0f}",
    "ThirteenMovMax": f"{ns_gr[i_max, 1] / Msun:.2f}",
    "ThirteenRovMax": f"{ns_gr[i_max, 0] / 1e3:.1f}",
    "ThirteenMnsNewtonLargest": f"{ns_nw[:, 1].max() / Msun:.2f}",
    "ThirteenCompactOV": f"{G * ns_gr[i_max, 1] / (ns_gr[i_max, 0] * c**2):.2f}",
}
with open(os.path.join(out, "mass_radius.tex"), "w") as fh:
    for k, v in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
for k, v in macros.items():
    print(f"{k:26s} {v}")

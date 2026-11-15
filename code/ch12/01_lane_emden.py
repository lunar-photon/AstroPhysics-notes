r"""Polytropes, the isothermal sphere and Eddington's standard model.

Question. Section "Polytropes and the isothermal sphere" writes hydrostatic equilibrium for
P proportional to rho^gamma as the Lane-Emden equation. What are its solutions, where is the
surface, and what do they say about the Sun and about massive stars?

Computes
  - theta(xi) for gamma = 2, 5/3, 4/3, 6/5 (n = 1, 1.5, 3, 5), integrated from the centre with
    the series theta = 1 - xi^2/6 + n xi^4/120, and the surface xi_1 and omega_1 = -xi^2 theta'(xi_1),
  - the isothermal sphere psi'' + 2 psi'/xi = exp(-psi), rho/rho_c = exp(-psi), out to xi = 1e4,
  - the n = 3 model scaled to the Sun's mass and radius (Eddington's standard model), with its
    central density, pressure and temperature,
  - the gas-to-total pressure ratio beta of the standard model for several masses, from
    Eddington's quartic 1 - beta = C mu^4 beta^4 (M/Msun)^2.

Writes
  results/ch12/lane_emden_n{1,1.5,3,5}.dat      xi theta
  results/ch12/isothermal.dat                     log10 xi, log10 rho/rho_c
  results/ch12/sun_n3_profile.dat                 r/R, rho/rho_c, T/T_c, P/P_c, m/M
  results/ch12/lane_emden.tex                     LaTeX macros (constants and numbers)
"""
import os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

out = os.path.join("results", "ch12")
os.makedirs(out, exist_ok=True)

# physical constants (SI) and the Sun
G, kB, a_rad, mH = 6.674e-11, 1.380649e-23, 7.5657e-16, 1.6726e-27
Msun, Rsun = 1.989e30, 6.957e8
mu_sun = 0.62


def lane_emden(n, xi_max=40.0):
    """Integrate theta'' + 2 theta'/xi = -theta^n from the centre to the first zero (or xi_max)."""
    xi0 = 1e-4
    th0 = 1 - xi0**2 / 6 + n * xi0**4 / 120
    dth0 = -xi0 / 3 + n * xi0**3 / 30

    def rhs(xi, y):
        th, dth = y
        return [dth, -max(th, 0.0) ** n - 2 * dth / xi]

    def surface(xi, y):
        return y[0]
    surface.terminal, surface.direction = True, -1
    sol = solve_ivp(rhs, (xi0, xi_max), [th0, dth0], events=surface,
                    rtol=1e-11, atol=1e-13, dense_output=True, max_step=0.01)
    if sol.t_events[0].size:
        xi1 = float(sol.t_events[0][0])
        dth1 = float(sol.sol(xi1)[1])
        return sol, xi1, -xi1**2 * dth1
    return sol, None, None


macros = {}
results = {}
for n, tag, word in [(1.0, "1", "One"), (1.5, "1.5", "OneHalf"), (3.0, "3", "Three"), (5.0, "5", "Five")]:
    sol, xi1, om1 = lane_emden(n, xi_max=40.0 if n < 5 else 12.0)
    xi_end = xi1 if xi1 else 12.0
    xs = np.linspace(1e-4, xi_end, 400)
    th = np.clip(sol.sol(xs)[0], 0, None)
    np.savetxt(os.path.join(out, f"lane_emden_n{tag}.dat"), np.column_stack([xs, th]), fmt="%.6f")
    results[n] = (xi1, om1)
    if xi1:
        macros[f"TwelveXi{word}"] = f"{xi1:.4f}"
        macros[f"TwelveOmega{word}"] = f"{om1:.4f}"
        macros[f"TwelveRhoRatio{word}"] = f"{xi1**3 / (3 * om1):.2f}"   # rho_c / mean rho

# analytic checks against the exact solutions
assert abs(results[1.0][0] - np.pi) < 1e-6, results[1.0]


# isothermal sphere
def iso_rhs(xi, y):
    psi, dpsi = y
    return [dpsi, np.exp(-psi) - 2 * dpsi / xi]


xi0 = 1e-4
iso = solve_ivp(iso_rhs, (xi0, 1e4), [xi0**2 / 6, xi0 / 3], rtol=1e-10, atol=1e-12,
                dense_output=True)
lx = np.linspace(-1, 4, 300)
rho_iso = np.exp(-iso.sol(10**lx)[0])
np.savetxt(os.path.join(out, "isothermal.dat"), np.column_stack([lx, np.log10(rho_iso)]), fmt="%.6f")
# compare the far field with the singular solution rho/rho_c = 2/xi^2
macros["TwelveIsoRatio"] = f"{rho_iso[-1] / (2 / (10**lx[-1]) ** 2):.3f}"


# Eddington's standard model: n = 3 polytrope for the Sun
xi1, om1 = results[3.0]
rho_mean = Msun / (4 / 3 * np.pi * Rsun**3)
rho_c = rho_mean * xi1**3 / (3 * om1)
r0 = Rsun / xi1                                   # length unit of the Lane-Emden variable
# r0^2 = (n+1) K rho_c^(1/n - 1) / (4 pi G)  with n = 3  ->  K, then P_c = K rho_c^(4/3)
Kpoly = 4 * np.pi * G * r0**2 / (4 * rho_c ** (1 / 3 - 1))
P_c = Kpoly * rho_c ** (4 / 3)


# beta from Eddington's quartic: P_gas = beta P, P_light = (1 - beta) P, P = K rho^{4/3}
def beta_of_M(M, mu):
    # mass of an n = 3 polytrope: M = 4 pi omega1 (K/(pi G))^{3/2}, and
    # K = [ (kB/(mu mH))^4 * 3 (1 - beta) / (a beta^4) ]^{1/3}
    def f(beta):
        K = ((kB / (mu * mH)) ** 4 * 3 * (1 - beta) / (a_rad * beta**4)) ** (1 / 3)
        return 4 * np.pi * om1 * (K / (np.pi * G)) ** 1.5 - M
    return brentq(f, 1e-6, 1 - 1e-12)


beta_sun = beta_of_M(Msun, mu_sun)
T_c = beta_sun * mu_sun * mH * P_c / (kB * rho_c)
macros.update({
    "TwelveSunRhoC": f"{rho_c:.3g}",
    "TwelveSunPC": f"{P_c:.3g}",
    "TwelveSunTC": f"{T_c:.3g}",
    "TwelveBetaSun": f"{beta_sun:.4f}",
})
for M_sol, word in [(10, "Ten"), (100, "Hundred"), (1000, "Thousand")]:
    macros[f"TwelveBeta{word}"] = f"{beta_of_M(M_sol * Msun, mu_sun):.3f}"

# profile of the solar n = 3 model
sol3, _, _ = lane_emden(3.0)
xs = np.linspace(1e-4, xi1, 200)
th, dth = sol3.sol(xs)
th = np.clip(th, 0, None)
m_frac = (-xs**2 * dth) / om1
np.savetxt(os.path.join(out, "sun_n3_profile.dat"),
           np.column_stack([xs / xi1, th**3, th, th**4, m_frac]), fmt="%.6f")


def tex_number(s):
    """'1.48e+05' -> '1.48\\times10^{5}' for use inside math mode."""
    if "e" not in s:
        return s
    mant, exp = s.split("e")
    return f"{mant}\\times10^{{{int(exp)}}}"


with open(os.path.join(out, "lane_emden.tex"), "w") as fh:
    for k, v in macros.items():
        fh.write(f"\\newcommand{{\\{k}}}{{{tex_number(v)}}}\n")

for k, v in macros.items():
    print(f"{k:24s} {v}")

# two-column copies of the solar profile, one per quantity, for plotting
for col, name in [(1, "rho"), (2, "T"), (3, "P"), (4, "m")]:
    prof = np.column_stack([xs / xi1, [th**3, th, th**4, m_frac][col - 1]])
    np.savetxt(os.path.join(out, f"sun_n3_{name}.dat"), prof, fmt="%.6f")

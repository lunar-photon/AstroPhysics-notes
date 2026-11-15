r"""Energy release of the proton-proton chain and the CNO cycle against temperature.

Question. Section "Pressure, opacity and burning" says both ways of burning hydrogen release the
same 26.7 MeV per helium nucleus but depend on temperature very differently. At what core
temperature does the CNO cycle take over from the pp chain?

Computes the energy release per unit mass with the standard fits of Kippenhahn, Weigert & Weiss,
Stellar Structure and Evolution (2012), Eqs. 18.63 and 18.65 (cgs, T9 = T / 1e9 K, psi = f = 1),
  eps_pp  = 2.57e4 g11 rho X^2 T9^(-2/3) exp(-3.381 T9^(-1/3)),
            g11 = 1 + 3.82 T9 + 1.51 T9^2 + 0.144 T9^3 - 0.0114 T9^4,
  eps_CNO = 8.24e25 g141 X_CNO X rho T9^(-2/3) exp(-15.231 T9^(-1/3) - (T9/0.8)^2),
            g141 = 1 - 2.00 T9 + 3.41 T9^2 - 2.43 T9^3,
for X = 0.70, X_CNO = 0.014 and rho = 100 g cm^-3 (both rates scale as rho, so the crossover does
not depend on it), and the logarithmic slopes d ln eps / d ln T at the Sun's centre (15.7 MK).

Writes
  results/ch12/pp_rate.dat    log10 T (K), log10 eps_pp (W/kg)
  results/ch12/cno_rate.dat   log10 T (K), log10 eps_CNO (W/kg)
  results/ch12/pp_cno.tex     LaTeX macros \TwelveTcross (MK), \TwelveNuPP, \TwelveNuCNO,
                              \TwelveCNOoverPP (ratio at 15.7 MK)
"""
import os
import numpy as np
from scipy.optimize import brentq

out = os.path.join("results", "ch12")
os.makedirs(out, exist_ok=True)

X, X_CNO, rho = 0.70, 0.014, 100.0          # mass fractions, density in g cm^-3


def eps_pp(T9):
    g11 = 1 + 3.82 * T9 + 1.51 * T9**2 + 0.144 * T9**3 - 0.0114 * T9**4
    return 2.57e4 * g11 * rho * X**2 * T9**(-2 / 3) * np.exp(-3.381 * T9**(-1 / 3))


def eps_cno(T9):
    g141 = 1 - 2.00 * T9 + 3.41 * T9**2 - 2.43 * T9**3
    return (8.24e25 * g141 * X_CNO * X * rho * T9**(-2 / 3)
            * np.exp(-15.231 * T9**(-1 / 3) - (T9 / 0.8)**2))


def slope(f, T9, h=1e-4):
    """d ln eps / d ln T by a centred difference in ln T."""
    return (np.log(f(T9 * np.exp(h))) - np.log(f(T9 * np.exp(-h)))) / (2 * h)


T = np.logspace(np.log10(4e6), np.log10(6e7), 300)        # K
T9 = T / 1e9
cgs_to_SI = 1e-4                                          # erg g^-1 s^-1 -> W kg^-1
np.savetxt(os.path.join(out, "pp_rate.dat"),
           np.column_stack([np.log10(T), np.log10(eps_pp(T9) * cgs_to_SI)]), fmt="%.5f")
np.savetxt(os.path.join(out, "cno_rate.dat"),
           np.column_stack([np.log10(T), np.log10(eps_cno(T9) * cgs_to_SI)]), fmt="%.5f")

T_cross = brentq(lambda t: eps_pp(t) - eps_cno(t), 0.010, 0.030) * 1e3   # MK
T_sun = 0.0157
nu_pp, nu_cno = slope(eps_pp, T_sun), slope(eps_cno, T_sun)
ratio = eps_cno(T_sun) / eps_pp(T_sun)

# self-check against the textbook numbers quoted in the chapter
assert 16 < T_cross < 20 and 3.5 < nu_pp < 4.5 and 17 < nu_cno < 22 and ratio < 1, \
    (T_cross, nu_pp, nu_cno, ratio)

with open(os.path.join(out, "pp_cno.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\TwelveTcross}}{{{T_cross:.1f}}}\n")
    fh.write(f"\\newcommand{{\\TwelveNuPP}}{{{nu_pp:.1f}}}\n")
    fh.write(f"\\newcommand{{\\TwelveNuCNO}}{{{nu_cno:.0f}}}\n")
    fh.write(f"\\newcommand{{\\TwelveCNOoverPP}}{{{ratio:.2f}}}\n")
print(f"crossover {T_cross:.2f} MK, slopes at 15.7 MK: pp {nu_pp:.2f}, CNO {nu_cno:.2f}, "
      f"CNO/pp there {ratio:.3f}")

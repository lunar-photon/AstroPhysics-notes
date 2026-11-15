r"""Synchrotron spectrum of one electron and of a power law of electrons.

Question. Section "Synchrotron radiation" claims that electrons with n(gamma) ∝ gamma^-p between
gamma_min and gamma_max give a spectrum j_nu ∝ nu^-(p-1)/2 between gamma_min^2 nu_g and
gamma_max^2 nu_g, whatever the shape of the one-electron spectrum, with a rise below and an
exponential fall above. Is that true for the exact one-electron spectrum?

Computes
  - the one-electron spectrum F(x) = x * int_x^inf K_{5/3}(t) dt, x = nu/nu_c, and its peak,
  - the population spectrum j(w) ∝ int_1^G g^-p F(w/g^2) dg, with g = gamma/gamma_min,
    G = gamma_max/gamma_min = 1000, w = nu/(gamma_min^2 nu_c0), for p = 2.5,
  - the logarithmic slope of j(w) in the middle of the range (expected -(p-1)/2 = -0.75).

Writes
  results/ch15/sync_single.dat       log10 x   log10 F(x)
  results/ch15/sync_population.dat   log10 w   log10 j(w)  (j scaled to 1 at w = 1)
  results/ch15/synchrotron.tex       LaTeX macros
"""
import os
import numpy as np
from scipy.special import kv
from scipy.integrate import quad

out = os.path.join("results", "ch15")
os.makedirs(out, exist_ok=True)

p = 2.5
G = 1000.0


def F(x):
    """One-electron synchrotron function x * int_x^inf K_{5/3}(t) dt."""
    # K_{5/3} = -2 K_{2/3}' - K_{1/3}, so int_x^inf K_{5/3} = 2 K_{2/3}(x) - int_x^inf K_{1/3} (no singular integrand)
    tail, _ = quad(lambda t: kv(1.0 / 3.0, t), x, np.inf, limit=400)
    return x * (2.0 * kv(2.0 / 3.0, x) - tail)


# table of F on a fine log grid, used by interpolation in the population integral
lx = np.linspace(-6.0, 1.7, 1541)
lF = np.log10([F(10.0**v) for v in lx])


def F_interp(x):
    l = np.log10(x)
    if l < lx[0]:
        return 10.0**(lF[0] + (l - lx[0]) / 3.0)      # F ∝ x^(1/3) at small x
    if l > lx[-1]:
        return F(x)
    return 10.0**np.interp(l, lx, lF)


# peak of F
xs = 10.0**np.linspace(-1.5, 0.3, 4001)
Fs = np.array([F_interp(x) for x in xs])
xpeak = xs[np.argmax(Fs)]

with open(os.path.join(out, "sync_single.dat"), "w") as f:
    for v in np.linspace(-3.0, 1.0, 161):
        f.write(f"{v:.4f} {np.log10(F_interp(10.0**v)):.5f}\n")


def j(w):
    # integrate over ln g for accuracy: dg = g dln g
    val, _ = quad(lambda s: np.exp(s) ** (1.0 - p) * F_interp(w / np.exp(2.0 * s)),
                  0.0, np.log(G), limit=400)
    return val


lw = np.linspace(-3.0, 8.0, 441)
jw = np.array([j(10.0**v) for v in lw])
j1 = j(1.0)
with open(os.path.join(out, "sync_population.dat"), "w") as f:
    for v, val in zip(lw, jw):
        f.write(f"{v:.4f} {np.log10(val / j1):.5f}\n")

# slope between w = 1e2 and w = 1e4 (well inside gamma_min^2 .. gamma_max^2 = 1 .. 1e6)
slope = (np.log10(j(1e4)) - np.log10(j(1e2))) / 2.0
# slope at low frequency, w = 1e-3 .. 1e-2
slope_low = (np.log10(j(1e-2)) - np.log10(j(1e-3))) / 1.0

with open(os.path.join(out, "synchrotron.tex"), "w") as f:
    f.write(f"\\newcommand{{\\FifteenSyncXpeak}}{{{xpeak:.2f}}}\n")
    f.write(f"\\newcommand{{\\FifteenSyncSlope}}{{{slope:.3f}}}\n")
    f.write(f"\\newcommand{{\\FifteenSyncSlopeLow}}{{{slope_low:.2f}}}\n")
    f.write(f"\\newcommand{{\\FifteenSyncP}}{{{p:g}}}\n")

print("x_peak", xpeak, "slope", slope, "slope_low", slope_low)

r"""Hertzsprung-Russell diagram of the Hipparcos stars and the nearby Gaia white dwarfs.

Question. Section "Scaling laws and the HR diagram" says that stars do not fill the
luminosity-temperature plane but crowd onto a main sequence, a giant branch and a white-dwarf
sequence. Where do real stars with good distances actually fall?

Reads
  data/ch12/hip_main.tsv       Hipparcos main catalogue (ESA 1997, VizieR I/239): HIP, V, parallax
                               and its error (mas), B-V and its error
  data/ch12/gaia_wd_100pc.tsv  Gaia EDR3 white dwarfs (Gentile Fusillo et al. 2021, VizieR
                               J/MNRAS/508/3877) with parallax > 10 mas, parallax/error > 10 and
                               white-dwarf probability > 0.75: pure-H fits of T_eff, log g (cgs)
                               and mass. Hipparcos was too shallow to see white dwarfs.

Computes, for stars with parallax error below 10% and B-V error below 0.05 mag,
  - the absolute magnitude M_V = V + 5 log10(parallax / 100 mas),
  - T_eff from B-V with the blackbody-based formula of Ballesteros (2012),
    T = 4600 K [1/(0.92 (B-V) + 1.7) + 1/(0.92 (B-V) + 0.62)],
  - the bolometric correction BC(T_eff) from the polynomials of Torres (2010, AJ 140, 1158),
  - log10 L/Lsun = (4.74 - M_V - BC) / 2.5.
No correction is made for interstellar reddening (small for stars this close).
For each white dwarf, R = sqrt(G M / g) and L/Lsun = (R/Rsun)^2 (T_eff / 5772 K)^4.

Writes
  results/ch12/hr_stars.png   the stars only, transparent, axes exactly
                              log10 T = 4.6 .. 3.4 (hot on the left) and log10 L = -4 .. 6,
                              9 cm x 7 cm, for fig_sources/fig_ch12_hr.tex to draw axes over
  results/ch12/hr.tex         LaTeX macros \TwelveHRN (Hipparcos stars), \TwelveHRMaxPc,
                              \TwelveHRNwd (white dwarfs)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

out = os.path.join("results", "ch12")
os.makedirs(out, exist_ok=True)

# ---- read the catalogue (VizieR tsv: '#' comments, a header, a units row, a dashes row) ----
rows = []
with open(os.path.join("data", "ch12", "hip_main.tsv")) as fh:
    lines = [l for l in fh if l.strip() and not l.startswith("#")]
for l in lines[3:]:
    f = l.rstrip("\n").split("\t")
    try:
        rows.append([float(x) for x in f[1:6]])
    except ValueError:          # a blank field (no V, parallax or colour)
        continue
V, plx, e_plx, bv, e_bv = np.array(rows).T

good = (plx > 0) & (e_plx / plx < 0.10) & (e_bv < 0.05) & (bv > -0.4) & (bv < 2.0)
V, plx, bv = V[good], plx[good], bv[good]

# ---- absolute magnitude, temperature, bolometric correction, luminosity ----
MV = V + 5.0 * np.log10(plx / 100.0)
T = 4600.0 * (1.0 / (0.92 * bv + 1.7) + 1.0 / (0.92 * bv + 0.62))
x = np.log10(T)


def bolometric_correction(x):
    """Torres (2010) BC_V as a function of x = log10 T_eff."""
    lo = [-0.190537291496456e5, 0.155144866764412e5, -0.421278819301717e4, 0.381476328422343e3]
    mid = [-0.370510203809015e5, 0.385672629965804e5, -0.150651486316025e5,
           0.261724637119416e4, -0.170623810323864e3]
    hi = [-0.118115450538963e6, 0.137145973583929e6, -0.636233812100225e5,
          0.147412923562646e5, -0.170587278406872e4, 0.788731721804990e2]
    poly = lambda c, x: sum(ci * x**i for i, ci in enumerate(c))
    return np.where(x < 3.70, poly(lo, x), np.where(x < 3.90, poly(mid, x), poly(hi, x)))


BC = bolometric_correction(x)
logL = (4.74 - MV - BC) / 2.5
print(f"BC of the Sun (5772 K): {float(bolometric_correction(np.log10(5772.0))):.3f}")

inside = (x > 3.4) & (x < 4.6) & (logL > -4) & (logL < 6)
x, logL = x[inside], logL[inside]
N = x.size
dmax = (1000.0 / plx[inside]).max() if N else 0.0
print(f"stars plotted: {N}, farthest at {dmax:.0f} pc")

# ---- white dwarfs: radius from mass and surface gravity, then Stefan-Boltzmann ----
G_cgs, Msun_g, Rsun_cm = 6.674e-8, 1.989e33, 6.957e10
wd = []
with open(os.path.join("data", "ch12", "gaia_wd_100pc.tsv")) as fh:
    lines = [l for l in fh if l.strip() and not l.startswith("#")]
for l in lines[3:]:
    f = l.rstrip("\n").split("\t")
    try:
        wd.append([float(v) for v in f[4:7]])
    except ValueError:          # no pure-H fit
        continue
Twd, loggwd, Mwd = np.array(wd).T
Rwd = np.sqrt(G_cgs * Mwd * Msun_g / 10.0**loggwd) / Rsun_cm
xwd = np.log10(Twd)
logLwd = 2 * np.log10(Rwd) + 4 * (xwd - np.log10(5772.0))
keep = (xwd > 3.4) & (xwd < 4.6) & (logLwd > -4) & (logLwd < 6)
xwd, logLwd = xwd[keep], logLwd[keep]
Nwd = xwd.size
print(f"white dwarfs plotted: {Nwd}, median radius {np.median(Rwd):.4f} Rsun")

x, logL = np.concatenate([x, xwd]), np.concatenate([logL, logLwd])

# ---- the picture: stars coloured from red (cool) to blue (hot), dark enough for white paper ----
cmap = LinearSegmentedColormap.from_list("stars", [
    (0.00, "#A3201B"), (0.20, "#D9581C"), (0.32, "#C8901A"),
    (0.45, "#8C8F6A"), (0.58, "#5E86C0"), (1.00, "#1F3F99")])
cnorm = plt.Normalize(3.45, 4.35)
rng = np.random.default_rng(12)
order = rng.permutation(x.size)     # no colour sits on top of another by catalogue order

cm = 1 / 2.54
fig = plt.figure(figsize=(9 * cm, 7 * cm))
ax = fig.add_axes([0, 0, 1, 1])
ax.scatter(x[order], logL[order], s=0.6, c=x[order], cmap=cmap, norm=cnorm,
           alpha=0.55, linewidths=0, rasterized=True)
ax.set_xlim(4.6, 3.4)
ax.set_ylim(-4, 6)
ax.axis("off")
fig.savefig(os.path.join(out, "hr_stars.png"), dpi=600, transparent=True)

with open(os.path.join(out, "hr.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\TwelveHRN}}{{{N:,}}}\n".replace(",", "\\,"))
    fh.write(f"\\newcommand{{\\TwelveHRMaxPc}}{{{dmax:.0f}}}\n")
    fh.write(f"\\newcommand{{\\TwelveHRNwd}}{{{Nwd:,}}}\n".replace(",", "\\,"))

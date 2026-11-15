r"""The SDSS galaxy redshift map: galaxies in a thin slice of sky, placed by distance.

Question. Section "Groups, Clusters and the Cosmic Web" says that galaxies lie on walls and
filaments around empty voids. Does a map of real galaxy positions show it?

Reads
  data/ch14/sdss_slice.csv   SDSS DR17 SpecObj (SkyServer SQL, class = GALAXY, zWarning = 0,
                             survey = sdss, sciencePrimary = 1) with -2.5 < dec < 2.5 deg,
                             120 < ra < 250 deg, 0.01 < z < 0.2. Columns ra, dec (deg), z.
                             The file is the raw download. Only RA 132 .. 234 deg is used (see below).

Coverage cut. The galaxies per 2 deg of RA (printed by the script) are 0 at RA < 130 deg, ramp up
between 130 and 132, rise to 600-1200 by RA 146 and stay there to RA 234, and fall to 240-430 beyond RA 236. The slice
has no spectroscopy below RA 130 (the survey stripe ends there) and is half filled above RA 236.
So the map keeps RA_LO = 132 .. RA_HI = 234 deg, centred on RA_C = 183 deg.

Computes
  - the comoving distance D(z) = c * int_0^z dz' / H(z') in a flat universe with
    H^2 = H_0^2 (Omega_m (1+z)^3 + Omega_Lambda), H_0 = 67.4 km/s/Mpc, Omega_m = 0.315
    (the values of the chapter on the expanding universe; radiation is negligible at z < 0.2),
  - the age of the same universe, t_0 = int_0^1 da / (a H(a)),
  - each galaxy's position in the plane of the slice, x = D sin(ra - 183 deg),
    y = D cos(ra - 183 deg), with the observer at the origin.

Writes
  results/ch14/sdss_wedge.png  the galaxies only, transparent, axes exactly x = -660 .. 660 Mpc
                               and y = 0 .. 860 Mpc, 15.6 cm x 8.6 cm (0.01 cm per Mpc), for
                               fig_sources/fig_ch14_sdss_wedge.tex to draw the outline over
  results/ch14/sdss.tex        LaTeX macros \FourteenSdssN, \FourteenSdssDecWidth,
                               \FourteenSdssDepth, \FourteenSdssDtenth (D at z = 0.1), \FourteenSdssRAlo, \FourteenSdssRAhi,
                               \FourteenAge
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RA_LO, RA_HI, RA_C = 132.0, 234.0, 183.0   # coverage cut, see the docstring
out = os.path.join("results", "ch14")
os.makedirs(out, exist_ok=True)

C, H0, OM = 299792.458, 67.4, 0.315          # km/s, km/s/Mpc, matter density parameter
OL = 1.0 - OM


def E(z):
    return np.sqrt(OM * (1 + z) ** 3 + OL)


zg = np.linspace(0.0, 0.25, 25001)
Dg = C / H0 * np.concatenate([[0], np.cumsum(0.5 * (1 / E(zg[1:]) + 1 / E(zg[:-1])) * np.diff(zg))])
D = lambda z: np.interp(z, zg, Dg)

# age: t0 = int_0^1 da / (a H(a)), substitution a = u^2 removes the integrable singularity at 0
u = np.linspace(1e-6, 1.0, 200001)
a = u ** 2
Ha = H0 * np.sqrt(OM / a ** 3 + OL)
f = 2 * u / (a * Ha)                           # da = 2u du
t0_s = np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(u)) * 3.0857e19   # km/s/Mpc -> seconds
t0 = t0_s / 3.15576e16                         # Gyr

ra, dec, z = np.loadtxt(os.path.join("data", "ch14", "sdss_slice.csv"), delimiter=",",
                        skiprows=1, unpack=True)
h, _ = np.histogram(ra, bins=np.arange(120, 252, 2))
print("galaxies per 2 deg of RA from 120:", h.tolist())
keep = (ra >= RA_LO) & (ra <= RA_HI)
ra, dec, z = ra[keep], dec[keep], z[keep]
d = D(z)
th = np.radians(ra - RA_C)
x, y = d * np.sin(th), d * np.cos(th)

L, YH = 660.0, 860.0
cm = 1 / 2.54
fig = plt.figure(figsize=(2 * XL * 0.01 * cm, YH * 0.01 * cm))
ax = fig.add_axes([0, 0, 1, 1])
ax.scatter(x, y, s=0.35, c="#1E1C1A", alpha=0.55, linewidths=0, rasterized=True)
ax.set_xlim(-XL, XL)
ax.set_ylim(0, YH)
ax.axis("off")
fig.savefig(os.path.join(out, "sdss_wedge.png"), dpi=600, transparent=True)

with open(os.path.join(out, "sdss.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\FourteenSdssN}}{{{ra.size:,}}}\n".replace(",", "\\,"))
    fh.write(f"\\newcommand{{\\FourteenSdssDecWidth}}{{{dec.max() - dec.min():.0f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenSdssDepth}}{{{D(0.2):.0f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenSdssRAlo}}{{{RA_LO:.0f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenSdssRAhi}}{{{RA_HI:.0f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenAge}}{{{t0:.1f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenSdssDtenth}}{{{D(0.1):.0f}}}\n")

print(f"N = {ra.size}, D(0.1) = {D(0.1):.1f} Mpc, D(0.2) = {D(0.2):.1f} Mpc, t0 = {t0:.2f} Gyr")
print(f"max radius {d.max():.0f}, max |x| {abs(x).max():.0f}, max y {y.max():.0f}")
assert 400 < D(0.1) < 450
assert 13.6 < t0 < 14.0
assert d.max() < YH and abs(x).max() < XL and y.min() >= 0
assert 30000 < ra.size < 60000
assert h[(130 - 120) // 2 + 1:(236 - 120) // 2].min() > 300   # RA 132..236 is fully covered
assert ra.min() >= RA_LO and ra.max() <= RA_HI
print("self-check ok")

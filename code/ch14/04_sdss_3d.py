r"""The SDSS galaxies in three dimensions: the volume that the wedge map is one thin slice of.

Question. The wedge map of the section "Groups, Clusters and the Cosmic Web" shows walls and
filaments in a slice 5 deg thick. What do they look like in the full volume?

Reads
  data/ch14/sdss_3d.csv   SDSS DR17 SpecObj (SkyServer SQL, class = GALAXY, zWarning = 0,
                          survey = sdss, sciencePrimary = 1) with 130 < ra < 240 deg,
                          0 < dec < 60 deg, 0.01 < z < 0.065. Every galaxy of the block is
                          kept, no thinning. Columns ra, dec (deg), z.

Computes
  - the comoving distance D(z) as in 02_sdss_wedge.py (flat, H_0 = 67.4, Omega_m = 0.315),
  - comoving Cartesian coordinates with the observer at the origin,
    x = D cos(dec) cos(ra), y = D cos(dec) sin(ra), z = D sin(dec),
    so +x points to RA 0, +y to RA 90 deg and +z to the north celestial pole,
  - an orthographic view (equal scale everywhere) from one fixed direction, near galaxies darker,
  - where Earth falls on the picture, how the three axes and a 100 Mpc bar project.
  Run with the argument "trial" to write a contact sheet of previews (elevation 10, 25, 40 deg and
  azimuth every 30 deg) instead of the final picture. The chosen view is ELEV, AZIM below.

Writes
  results/ch14/sdss3d.png      the galaxies only, transparent, 13 cm x 9 cm
  results/ch14/sdss3d_pos.tex  TikZ data in cm, for fig_sources/fig_ch14_sdss3d.tex
  results/ch14/sdss3d.tex      LaTeX macros \FourteenThreeN, \FourteenThreeDepth,
                               \FourteenThreeSample, \FourteenThreeBar
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

out = os.path.join("results", "ch14")
os.makedirs(out, exist_ok=True)

C, H0, OM = 299792.458, 67.4, 0.315
OL = 1.0 - OM
BAR, ARROW = 100.0, 60.0                       # scale bar and axis arrow length (Mpc)
ELEV, AZIM = 25.0, 30.0                        # chosen view direction in degrees (best of the trial sheet)
W_CM, H_CM = 13.0, 9.0
PT, AL0, AL1 = 0.5, 0.07, 0.6                  # point size, alpha far and near


def E(z):
    return np.sqrt(OM * (1 + z) ** 3 + OL)


zg = np.linspace(0.0, 0.2, 20001)
Dg = C / H0 * np.concatenate([[0], np.cumsum(0.5 * (1 / E(zg[1:]) + 1 / E(zg[:-1])) * np.diff(zg))])
D = lambda z: np.interp(z, zg, Dg)

ra, dec, z = np.loadtxt(os.path.join("data", "ch14", "sdss_3d.csv"), delimiter=",",
                        skiprows=1, unpack=True)
d = D(z)
DMAX = D(0.065)
a, b = np.radians(ra), np.radians(dec)
X, Y, Z = d * np.cos(b) * np.cos(a), d * np.cos(b) * np.sin(a), d * np.sin(b)
XYZ = np.c_[X, Y, Z]


def render(el, az, path, w_cm, h_cm, dpi, transparent=True):
    fig = plt.figure(figsize=(w_cm / 2.54, h_cm / 2.54))
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.set_proj_type("ortho")
    e, s = np.radians(el), np.radians(az)
    toward = np.array([np.cos(e) * np.cos(s), np.cos(e) * np.sin(s), np.sin(e)])   # points at the viewer
    t = XYZ @ toward
    t = (t - t.min()) / np.ptp(t)               # 0 far, 1 near
    col = np.tile([0.118, 0.110, 0.102, 1.0], (ra.size, 1))
    col[:, 3] = AL0 + (AL1 - AL0) * t ** 1.5
    ax.scatter(X, Y, Z, s=PT, c=col, linewidths=0, depthshade=False, rasterized=True)
    lim = np.array([[-DMAX, 10.0], [-0.9 * DMAX, 0.9 * DMAX], [0.0, 0.9 * DMAX]])
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2])
    ax.set_box_aspect(np.ptp(lim, axis=1), zoom=1.75)
    ax.view_init(elev=el, azim=az)
    ax.set_axis_off()
    fig.savefig(path, dpi=dpi, transparent=transparent, facecolor=None if transparent else "white")
    return fig, ax


if len(sys.argv) > 1 and sys.argv[1] == "trial":
    for el in (10, 25, 40):
        for az in range(-90, 91, 30):
            f, _ = render(el, az, os.path.join(out, f"try3d_e{el}_a{az}.png"), 6.5, 4.5, 110, False)
            plt.close(f)
    print("trial previews written")
    sys.exit(0)

fig, ax = render(ELEV, AZIM, os.path.join(out, "sdss3d.png"), W_CM, H_CM, 600)
fig.canvas.draw()
M = ax.get_proj()


def pos(p):
    x2, y2, _ = proj3d.proj_transform(*p, M)
    px, py = ax.transData.transform((x2, y2))
    w, h = fig.get_size_inches() * fig.dpi
    return np.array([px / w * W_CM, py / h * H_CM])


az = np.radians(AZIM)
horiz = np.array([-np.sin(az), np.cos(az), 0.0])   # runs along the picture's horizontal
earth = pos(np.zeros(3))
vec = {k: pos(v) - earth for k, v in {"RA0": [ARROW, 0, 0], "RA90": [0, ARROW, 0], "North": [0, 0, ARROW]}.items()}
barcm = np.linalg.norm(pos(BAR * horiz) - earth)
with open(os.path.join(out, "sdss3d_pos.tex"), "w") as fh:
    fh.write(f"\\coordinate (pEarth) at ({earth[0]:.3f},{earth[1]:.3f});\n")
    for k, v in vec.items():
        n = {"RA0": "A", "RA90": "B", "North": "C"}[k]
        fh.write(f"\\def\\fourteenthree{n}x{{{v[0]:.3f}}}\\def\\fourteenthree{n}y{{{v[1]:.3f}}}\n")
    fh.write(f"\\def\\fourteenthreeBar{{{barcm:.3f}}}\n")
    fh.write(f"\\def\\fourteenthreeW{{{W_CM}}}\\def\\fourteenthreeH{{{H_CM}}}\n")
with open(os.path.join(out, "sdss3d.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\FourteenThreeN}}{{{ra.size:,}}}\n".replace(",", "\\,"))
    fh.write(f"\\newcommand{{\\FourteenThreeDepth}}{{{DMAX:.0f}}}\n")
    fh.write("\\newcommand{\\FourteenThreeSample}{every galaxy of the block}\n")
    fh.write(f"\\newcommand{{\\FourteenThreeBar}}{{{BAR:.0f}}}\n")

print(f"N = {ra.size}, depth = {DMAX:.1f} Mpc, bar = {barcm:.3f} cm, earth = {earth}")
print({k: v.round(2).tolist() for k, v in vec.items()})
# self-check
assert 100000 < ra.size < 115000
assert 260 < DMAX < 300 and d.max() <= DMAX + 1e-6
assert ra.min() > 130 and ra.max() < 240 and dec.min() > 0 and dec.max() < 60
assert np.allclose(np.linalg.norm(XYZ, axis=1), d)
assert 0 < earth[0] < W_CM and 0 < earth[1] < H_CM
# orthographic: the bar along the horizontal and the vertical arrow share one scale
assert abs(pos(BAR * horiz)[1] - earth[1]) < 1e-3
s_bar = barcm / BAR
s_z = np.linalg.norm(vec["North"]) / (ARROW * np.cos(np.radians(ELEV)))
assert abs(s_bar / s_z - 1) < 0.02
print("self-check ok")

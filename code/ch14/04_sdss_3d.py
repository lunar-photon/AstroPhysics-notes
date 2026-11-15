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
  - a mild perspective view from one fixed direction, near galaxies darker, with the survey volume
    drawn as a wireframe in the same projection (cone edges, far face grid, 100 and 200 Mpc arcs,
    floor at dec = 0, drop lines),
  - where Earth, the ends of the distance arcs and the tick marks fall on the picture.

Writes
  results/ch14/sdss3d.png      the galaxies and the wireframe, transparent, 13 cm x 9 cm
  results/ch14/sdss3d_pos.tex  TikZ coordinates in cm, for fig_sources/fig_ch14_sdss3d.tex
  results/ch14/sdss3d.tex      LaTeX macros \FourteenThreeN, \FourteenThreeDepth
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

out = os.path.join("results", "ch14")
os.makedirs(out, exist_ok=True)

C, H0, OM = 299792.458, 67.4, 0.315
OL = 1.0 - OM
ELEV, AZIM = 22.0, 25.0                        # view direction in degrees
FOCAL, ZOOM = 0.5, 1.25                        # mild perspective, picture zoom
W_CM, H_CM = 13.0, 9.0
PT, AL0, AL1 = 0.4, 0.07, 0.6                  # point size, alpha far and near
RA_LO, RA_HI, DEC_LO, DEC_HI = 130.0, 240.0, 0.0, 60.0
RA_TICKS, DEC_TICKS, TICK = (130, 170, 210, 240), (0, 30, 60), 3.5   # tick marks, TICK in degrees
GREY = (0.35, 0.33, 0.30)


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


def sph(ra_, dec_, r):
    a_, b_ = np.radians(ra_), np.radians(dec_)
    return np.array([r * np.cos(b_) * np.cos(a_), r * np.cos(b_) * np.sin(a_), r * np.sin(b_)])


def line(ax, p, lw=0.4, alpha=0.7, ls="-"):
    p = np.array(p)
    ax.plot(p[:, 0], p[:, 1], p[:, 2], color=GREY + (alpha,), lw=lw, ls=ls, solid_capstyle="butt")


def ra_arc(r, dec_):                       # points along RA at fixed dec and distance
    return [sph(u, dec_, r) for u in np.linspace(RA_LO, RA_HI, 60)]


def dec_arc(r, ra_):                       # points along dec at fixed RA and distance
    return [sph(ra_, u, r) for u in np.linspace(DEC_LO, DEC_HI, 30)]


def wireframe(ax):
    O = np.zeros(3)
    ax.add_collection3d(Poly3DCollection([[O] + ra_arc(DMAX, 0.0)], facecolor=GREY + (0.07,), edgecolor="none"))   # floor
    for r in (100.0, 200.0):               # distance arcs on the floor and the two side faces
        line(ax, ra_arc(r, 0.0), alpha=0.6)
        line(ax, dec_arc(r, RA_LO), alpha=0.6)
        line(ax, dec_arc(r, RA_HI), alpha=0.6)
    for ra_ in (RA_LO, RA_HI):             # edges of the cone and of the floor
        for dec_ in (DEC_LO, DEC_HI):
            line(ax, [O, sph(ra_, dec_, DMAX)], lw=0.6, alpha=0.9)
    for dec_ in (0, 15, 30, 45, 60):       # far face, a curved grid on the sphere D = DMAX
        line(ax, ra_arc(DMAX, dec_), lw=0.5 if dec_ in (0, 60) else 0.35, alpha=0.9 if dec_ in (0, 60) else 0.6)
    for ra_ in (130, 150, 170, 190, 210, 230, 240):
        line(ax, dec_arc(DMAX, ra_), lw=0.5 if ra_ in (130, 240) else 0.35, alpha=0.9 if ra_ in (130, 240) else 0.6)
    for ra_ in (RA_LO, RA_HI):             # drop lines from the far top corners to the floor
        top = sph(ra_, DEC_HI, DMAX)
        line(ax, [top, np.array([top[0], top[1], 0.0])], lw=0.35, alpha=0.6, ls=(0, (3, 3)))
    for r_ in RA_TICKS:                    # ticks on the top edge of the far face, pointing out of it (the bottom edge lies inside the cloud)
        line(ax, [sph(r_, DEC_HI, DMAX), sph(r_, DEC_HI + TICK, DMAX)], lw=0.7, alpha=0.95)
    for u in DEC_TICKS:                    # and up the RA = 240 edge of the far face, pointing out of it
        line(ax, [sph(RA_HI, u, DMAX), sph(RA_HI + TICK, u, DMAX)], lw=0.7, alpha=0.95)


def render(el, az, path, w_cm, h_cm, dpi, transparent=True):
    fig = plt.figure(figsize=(w_cm / 2.54, h_cm / 2.54))
    ax = fig.add_axes([0, 0, 1, 1], projection="3d")
    ax.set_proj_type("persp", focal_length=FOCAL)
    e, s = np.radians(el), np.radians(az)
    toward = np.array([np.cos(e) * np.cos(s), np.cos(e) * np.sin(s), np.sin(e)])   # points at the viewer
    t = XYZ @ toward
    t = (t - t.min()) / np.ptp(t)               # 0 far, 1 near
    col = np.tile([0.118, 0.110, 0.102, 1.0], (ra.size, 1))
    col[:, 3] = AL0 + (AL1 - AL0) * t ** 1.5
    ax.scatter(X, Y, Z, s=PT, c=col, linewidths=0, depthshade=False, rasterized=True)
    wireframe(ax)
    lim = np.array([[-DMAX, 10.0], [-0.9 * DMAX, 0.9 * DMAX], [0.0, 0.9 * DMAX]])
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_zlim(*lim[2])
    ax.set_box_aspect(np.ptp(lim, axis=1), zoom=ZOOM)
    ax.view_init(elev=el, azim=az)
    ax.set_axis_off()
    fig.savefig(path, dpi=dpi, transparent=transparent, facecolor=None if transparent else "white")
    return fig, ax


fig, ax = render(ELEV, AZIM, os.path.join(out, "sdss3d.png"), W_CM, H_CM, 600)
fig.canvas.draw()
M = ax.get_proj()


def pos(p):
    x2, y2, _ = proj3d.proj_transform(*p, M)
    px, py = ax.transData.transform((x2, y2))
    w, h = fig.get_size_inches() * fig.dpi
    return np.array([px / w * W_CM, py / h * H_CM])


anch = {"Earth": pos(np.zeros(3))}
for r in (100, 200, 285):
    anch[f"L{r}"] = pos(sph(RA_LO, 0.0, float(r)))                     # arcs, right end of the floor edge
for r_ in RA_TICKS:
    anch[f"B{r_}"] = pos(sph(r_, DEC_HI, DMAX))                        # RA ticks, on the top edge of the far face
    anch[f"A{r_}"] = pos(sph(r_, DEC_HI + TICK, DMAX))                 # and their outer ends
for u in DEC_TICKS:
    anch[f"D{u}"] = pos(sph(RA_HI + TICK, u, DMAX))                    # outer ends of the declination ticks
with open(os.path.join(out, "sdss3d_pos.tex"), "w") as fh:
    for k, v in anch.items():
        fh.write(f"\\coordinate (p{k}) at ({v[0]:.3f},{v[1]:.3f});\n")
    fh.write(f"\\def\\fourteenthreeW{{{W_CM}}}\\def\\fourteenthreeH{{{H_CM}}}\n")
with open(os.path.join(out, "sdss3d.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\FourteenThreeN}}{{{ra.size:,}}}\n".replace(",", "\\,"))
    fh.write(f"\\newcommand{{\\FourteenThreeDepth}}{{{DMAX:.0f}}}\n")

print(f"N = {ra.size}, depth = {DMAX:.1f} Mpc")
print({k: v.round(2).tolist() for k, v in anch.items()})
# self-check
assert ra.size == 106405
assert 260 < DMAX < 300 and d.max() <= DMAX + 1e-6
assert ra.min() > RA_LO and ra.max() < RA_HI and dec.min() > DEC_LO and dec.max() < DEC_HI
assert np.allclose(np.linalg.norm(XYZ, axis=1), d)
assert all(0 < v[0] < W_CM and 0 < v[1] < H_CM for v in anch.values())
assert np.allclose(np.linalg.norm(sph(RA_HI, DEC_HI, DMAX)), DMAX)

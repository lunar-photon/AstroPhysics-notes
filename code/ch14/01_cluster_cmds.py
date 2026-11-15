r"""Colour-magnitude diagrams of three star clusters from Gaia DR3.

Question. All stars of a cluster share one age, distance and composition. What does the
colour-magnitude diagram of a young, an old and an old metal-poor cluster look like, where
is each turn-off, and how many blue stragglers does M67 hold?

Reads
  data/ch14/{pleiades,m67,ngc6397}.csv  Gaia DR3 (VizieR I/355/gaiadr3, cones of 2.5, 0.7 and
                                        0.25 degrees) with RUWE < 1.4, BP and RP present,
                                        G < 18 (18.5 for NGC 6397)

Computes, per cluster,
  - the proper-motion clump: the peak bin (0.5 mas/yr bins, stars within a rough literature parallax window only, so that the field does not win) of a 2-D histogram of (pmra, pmdec), then the median
    of the stars within 1.5 mas/yr of it
  - members: within R_PM of the clump centre (4, 1.5, 1.5 mas/yr) and with parallax within
    3 sigma of the cluster parallax, sigma^2 = error^2 + (0.05 mas)^2
  - the distance d = 1000 / (median parallax of members with G < 15 and error < 0.1 mas + 0.017),
    where 0.017 mas is the global Gaia DR3 zero-point offset (Lindegren et al. 2021), applied
    as one constant. It is a rough value. The true offset depends on magnitude and colour.
  - M_G = G + 5 log10(parallax_cluster / 100 mas) - A_G, every member at the cluster distance,
    and (BP-RP)_0 = (BP-RP) - E(BP-RP), with A_G = 2.74 E(B-V) and E(BP-RP) = 1.34 E(B-V)
    (approximate, they depend on colour) and E(B-V) from memory, 0.04, 0.04 and 0.18
  - the turn-off, the bluest point of the upper main sequence. The ridge is the median colour in
    0.4-mag bins of M_G holding at least 3 members. For the Pleiades the brightest Gaia stars are missing (saturated or RUWE-flagged), so its bin is only the brightest populated one and a lower limit on the true turn-off brightness. Going up the main sequence it runs blueward,
    and at the turn-off it turns redward onto the subgiant branch. The bin with the bluest
    median is the turn-off, and its centre and median give M_G and colour. The search starts
    at M_G_MIN (-3, 0, 2.5), which keeps the horizontal branch of NGC 6397 out of it.
  - blue stragglers of M67 by a box. Members brighter than the turn-off by more than 0.5 mag
    and not brighter than 2.5 mag above the turn-off (so, not giants), and bluer than the turn-off
    colour. The subgiant branch and the red clump are redder than the turn-off, so a colour
    cut at the turn-off colour leaves them out.

Writes
  results/ch14/{pleiades,m67,ngc6397}_members.dat  colour_0, M_G, blue-straggler flag
  results/ch14/cmd_clusters.png, cmd_m67.png  the points of Figures A and B on exact axes (transparent)
  results/ch14/m67_msline_xy.dat, m67_bs_xy.dat  the line and the stragglers as (colour, -M_G) for TikZ
  results/ch14/m67_msfit.dat  quadratic fit of the lower main sequence of M67, extended upward
  results/ch14/clusters.tex  macros (Age in Gyr from Eq. st:eq:turnoff, BS = mean of the stragglers) \FourteenPleN, \FourteenPleDist, \FourteenPleMTO,
                             \FourteenPleCTO, and the same with Mst (M67) and Ngc (NGC 6397),
                             and \FourteenMstNBS
"""
import os
import numpy as np

os.makedirs("results/ch14", exist_ok=True)
ZP = 0.017  # mas
CL = {  # name: (macro key, E(B-V), PM radius, PM histogram half-range, M_G search start, seed parallax window mas)
    "pleiades": ("Ple", 0.04, 4.0, 70, -3.0, (6, 9)),
    "m67": ("Mst", 0.04, 1.5, 30, 0.0, (0.9, 1.5)),
    "ngc6397": ("Ngc", 0.18, 1.5, 20, 2.5, (0.2, 0.6)),
}
rows, tex = {}, []
for name, (key, ebv, rpm, hr, mgmin, pw) in CL.items():
    d = np.genfromtxt(f"data/ch14/{name}.csv", delimiter=",", names=True)
    G, bp, rp = d["phot_g_mean_mag"], d["phot_bp_mean_mag"], d["phot_rp_mean_mag"]
    plx, e_plx, pmra, pmde = d["parallax"], d["parallax_error"], d["pmra"], d["pmdec"]
    ok = np.isfinite(pmra) & np.isfinite(pmde) & np.isfinite(plx) & (plx > 0)
    H, xe, ye = np.histogram2d(pmra[ok & (plx > pw[0]) & (plx < pw[1])], pmde[ok & (plx > pw[0]) & (plx < pw[1])], bins=int(2*hr/0.5), range=[[-hr, hr], [-hr, hr]])
    i, j = np.unravel_index(np.argmax(H), H.shape)
    c0 = np.array([0.5 * (xe[i] + xe[i + 1]), 0.5 * (ye[j] + ye[j + 1])])
    near = ok & (np.hypot(pmra - c0[0], pmde - c0[1]) < 1.5)
    c = np.array([np.median(pmra[near]), np.median(pmde[near])])
    inpm = ok & (np.hypot(pmra - c[0], pmde - c[1]) < rpm)
    plx0 = np.median(plx[inpm & (G < 15) & (e_plx < 0.1)])
    for _ in range(2):
        mem = inpm & (np.abs(plx - plx0) < 3 * np.sqrt(e_plx**2 + 0.05**2))
        plx0 = np.median(plx[mem & (G < 15) & (e_plx < 0.1)])
    dist = 1000.0 / (plx0 + ZP)
    MG = G[mem] + 5 * np.log10((plx0 + ZP) / 100.0) - 2.74 * ebv
    col = (bp - rp)[mem] - 1.34 * ebv
    cen, med = [], []
    for lo in np.arange(mgmin, MG.max(), 0.4):
        b = (MG >= lo) & (MG < lo + 0.4)
        if b.sum() >= 3:
            cen.append(lo + 0.2)
            med.append(np.median(col[b]))
    k = int(np.argmin(med))
    mtu, ctu = cen[k], med[k]
    flag = np.zeros(mem.sum(), int)
    if name == "m67":
        flag = ((MG < mtu - 0.5) & (MG > mtu - 2.5) & (col < ctu)).astype(int)
    np.savetxt(f"results/ch14/{name}_members.dat", np.c_[col, MG, flag],
               fmt="%.4f %.4f %d", header="colour_0 M_G flag_blue_straggler")
    rows[name] = dict(n=int(mem.sum()), dist=dist, mtu=mtu, ctu=ctu, nbs=int(flag.sum()))
    print(name, rows[name], "pm centre", c, "plx", plx0)
    r = rows[name]
    tex += [f"\\providecommand{{\\Fourteen{key}N}}{{{r['n']}}}",
            f"\\providecommand{{\\Fourteen{key}Dist}}{{{r['dist']:.0f}}}",
            f"\\providecommand{{\\Fourteen{key}MTO}}{{{r['mtu']:.1f}}}",
            f"\\providecommand{{\\Fourteen{key}CTO}}{{{r['ctu']:.2f}}}"]
tex.append(f"\\providecommand{{\\FourteenMstNBS}}{{{rows['m67']['nbs']}}}")


# ---- ages and masses from the notes' scalings (Eq. st:eq:turnoff, L ~ M^3.5), M_G(Sun) = 4.67,
# no bolometric correction (small for F and A stars). Rough, as the text says.
MGSUN = 4.67
def lum(m):
    return 10 ** (0.4 * (MGSUN - m))
for key, nm in (("Ple", "pleiades"), ("Mst", "m67"), ("Ngc", "ngc6397")):
    t = 1e10 * lum(rows[nm]["mtu"]) ** (-5 / 7) / 1e9
    tex.append(f"\\providecommand{{\\Fourteen{key}Age}}{{{t:.1f}}}")   # Gyr
mm = np.loadtxt("results/ch14/m67_members.dat")
mbs = mm[mm[:, 2] == 1, 1].mean()
ltu, lbs = lum(rows["m67"]["mtu"]), lum(mbs)
tex += [f"\\providecommand{{\\FourteenMstLTO}}{{{ltu:.1f}}}",
        f"\\providecommand{{\\FourteenMstMassTO}}{{{ltu ** (1 / 3.5):.1f}}}",
        f"\\providecommand{{\\FourteenBSMG}}{{{mbs:.1f}}}",
        f"\\providecommand{{\\FourteenBSLratio}}{{{lbs / ltu:.1f}}}",
        f"\\providecommand{{\\FourteenBSMass}}{{{lbs ** (1 / 3.5):.1f}}}",
        f"\\providecommand{{\\FourteenBSLife}}{{{1e10 * lbs ** (-5 / 7) / 1e9:.1f}}}"]
# main-sequence extension for Figure B. M67 has no stars up the main sequence above its turn-off, so the line is
# taken from the Pleiades, whose main sequence is intact (both have solar metals): a cubic fit of colour against
# M_G for Pleiades members with -0.6 < M_G < 4.5 and colour < 0.9, drawn for 0.3 < M_G < 3.4 (the cubic hooks back above that).
ple = np.loadtxt("results/ch14/pleiades_members.dat")
sel = (ple[:, 1] > -0.6) & (ple[:, 1] < 4.5) & (ple[:, 0] < 0.9)
p = np.polyfit(ple[sel, 1], ple[sel, 0], 3)
g = np.linspace(0.3, 3.4, 40)
line = list(zip(np.polyval(p, g), g))
np.savetxt("results/ch14/m67_msfit.dat", line, fmt="%.4f", header="colour_0 M_G")
open("results/ch14/clusters.tex", "w").write("\n".join(tex) + "\n")
assert 125 < rows["pleiades"]["dist"] < 145
assert 750 < rows["m67"]["dist"] < 950
assert 2000 < rows["ngc6397"]["dist"] < 2800
assert rows["pleiades"]["mtu"] < rows["m67"]["mtu"] <= rows["ngc6397"]["mtu"] + 0.5
assert rows["ngc6397"]["ctu"] < rows["m67"]["ctu"] + 0.2
assert 3 <= rows["m67"]["nbs"] <= 60
print("self-check ok")

# ---- point images for the figures (axes and labels are drawn by TikZ over them) ----
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def png(path, groups, xlim, ylim, w, h):
    fig = plt.figure(figsize=(w / 2.54, h / 2.54))
    ax = fig.add_axes([0, 0, 1, 1])
    for data, color, s, a in groups:
        ax.scatter(data[:, 0], data[:, 1], s=s, c=color, alpha=a, linewidths=0, rasterized=True)
    ax.set_xlim(*xlim); ax.set_ylim(ylim[1], ylim[0]); ax.axis("off")
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)

ld = {n: np.loadtxt(f"results/ch14/{n}_members.dat") for n in CL}
# Figure A: colour -0.4 .. 2.0 (8.4 cm), M_G -3 .. 13 (9.6 cm). Colours as the book's astroblue, orange, accent.
png("results/ch14/cmd_clusters.png",
    [(ld["ngc6397"][:, :2], "#A13D2C", 1.2, 0.35), (ld["m67"][:, :2], "#E8A33D", 2.5, 0.7),
     (ld["pleiades"][:, :2], "#1B4F72", 2.5, 0.8)], (-0.4, 2.0), (-3, 13), 8.4, 9.6)
# Figure B: M67 members in grey, colour -0.4 .. 2.0 (7.2 cm), M_G -2.5 .. 8 (8.4 cm)
png("results/ch14/cmd_m67.png", [(ld["m67"][ld["m67"][:, 2] == 0][:, :2], "#6B665D", 5, 0.9)],
    (-0.4, 2.0), (-2.5, 8), 7.2, 8.4)
# files for TikZ (y = -M_G so that bright is up): the main-sequence line and the blue stragglers
np.savetxt("results/ch14/m67_msline_xy.dat", [(c, -m) for c, m in line], fmt="%.4f")
np.savetxt("results/ch14/m67_bs_xy.dat", [(c, -m) for c, m, fl in ld["m67"][:, [0, 1, 2]] if fl == 1], fmt="%.4f")

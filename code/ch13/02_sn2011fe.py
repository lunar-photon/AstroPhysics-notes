r"""Type Ia supernova light curve: SN 2011fe in M101.

Question. Section "Type Ia Supernovae" says the light rises for about three weeks, then follows
the decay of cobalt-56, falling by 0.98 mag per 100 days if all the decay energy stays in the
debris, a little faster in real tails. Brighter explosions fade more slowly (Phillips). What does a
real, well-observed light curve show?

Reads
  data/ch13/sn2011fe_BV.tsv   B and V photometry of SN 2011fe from the Open Supernova Catalog file
                              (Munari et al. 2013, NewA 20, 30; Tsvetkov et al. 2013, CoSka 43, 94)
                              columns mjd, band, mag, err, source

Computes
  - the time and magnitude of B maximum, from a quadratic fit to the Munari B points within
    6 days of the brightest one; the same for V.
  - Delta m15(B) = B(t_max + 15 d) - B_max, B at +15 d from a quadratic fit to the B points
    between +10 and +20 d.
  - straight-line fits of mag against time on the cobalt tail, from +60 to +300 d (both sources)
    and from +300 to +650 d (Tsvetkov), as mag per 100 days, against the full-trapping 0.98.
  - the distance modulus and distance from B_max with the book's peak M_B = -19.3 and the
    Milky Way dust A_B = 4.1 E(B-V), E(B-V) = 0.0077 from the catalogue file.

Writes
  results/ch13/sn_B.dat, sn_V.dat   days since B maximum, mag, source flag (0 Munari, 1 Tsvetkov)
  results/ch13/sn2011fe.tex         \Thirteen... macros quoted in the text and used by the figure
"""
import os
import numpy as np

out = os.path.join("results", "ch13")
os.makedirs(out, exist_ok=True)

rows = [l.rstrip("\n").split("\t") for l in open(os.path.join("data", "ch13", "sn2011fe_BV.tsv"))
        if not l.startswith("#") and not l.startswith("mjd")]
t = np.array([float(r[0]) for r in rows])
band = np.array([r[1] for r in rows])
mag = np.array([float(r[2]) for r in rows])
src = np.array([0 if r[4] == "Munari2013" else 1 for r in rows])


def peak(b):
    s = (band == b) & (src == 0)
    i0 = np.argmin(mag[s])
    tt, mm = t[s], mag[s]
    w = np.abs(tt - tt[i0]) < 6
    c = np.polyfit(tt[w] - tt[i0], mm[w], 2)
    dt = -c[1] / (2 * c[0])
    return tt[i0] + dt, np.polyval(c, dt), w.sum()


tB, Bmax, nB = peak("B")
tV, Vmax, nV = peak("V")
d = t - tB

sB = (band == "B") & (d > 10) & (d < 20)
c15 = np.polyfit(d[sB], mag[sB], 2)
dm15 = np.polyval(c15, 15.0) - Bmax


def slope(b, d0, d1, which=None):
    s = (band == b) & (d > d0) & (d < d1)
    if which is not None:
        s &= src == which
    c = np.polyfit(d[s], mag[s], 1)
    return 100 * c[0], c[1], s.sum()


kV, aV, nTV = slope("V", 60, 300)
kB, aB, nTB = slope("B", 60, 300)
kVl, aVl, nLV = slope("V", 300, 700, which=1)

EBV = 0.0077
AB = 4.1 * EBV
mu = Bmax - AB - (-19.3)
dist_Mpc = 10 ** (mu / 5 + 1) / 1e6

for b in ("B", "V"):
    s = band == b
    np.savetxt(os.path.join(out, f"sn_{b}.dat"), np.c_[d[s], mag[s], src[s]], fmt="%.3f %.3f %d")

print(f"B max at MJD {tB:.2f} ({nB} pts), B = {Bmax:.2f}; V max at MJD {tV:.2f}, V = {Vmax:.2f} ({tV - tB:+.1f} d)")
print(f"Delta m15(B) = {dm15:.2f}")
print(f"tail 60-300 d: V {kV:.2f}, B {kB:.2f} mag/100 d ({nTV}, {nTB} pts); 300-650 d V {kVl:.2f} ({nLV} pts)")
print(f"mu = {mu:.2f}, d = {dist_Mpc:.1f} Mpc; last epoch {d.max():.0f} d; N B {np.sum(band == 'B')}, V {np.sum(band == 'V')}")

M = {
    "ThirteenSnTmax": f"{tB:.1f}", "ThirteenSnBmax": f"{Bmax:.2f}", "ThirteenSnVmax": f"{Vmax:.2f}",
    "ThirteenSnVlag": f"{tV - tB:.1f}", "ThirteenSnDmB": f"{dm15:.2f}",
    "ThirteenSnSlopeV": f"{kV:.2f}", "ThirteenSnSlopeB": f"{kB:.2f}", "ThirteenSnSlopeLate": f"{kVl:.2f}",
    "ThirteenSnVa": f"{aV:.4f}", "ThirteenSnVk": f"{kV / 100:.6f}",
    "ThirteenSnLa": f"{aVl:.4f}", "ThirteenSnLk": f"{kVl / 100:.6f}",
    "ThirteenSnAB": f"{AB:.2f}", "ThirteenSnMu": f"{mu:.2f}", "ThirteenSnDist": f"{dist_Mpc:.1f}",
    "ThirteenSnN": str(len(t)), "ThirteenSnLast": f"{d.max():.0f}",
}
with open(os.path.join(out, "sn2011fe.tex"), "w") as fh:
    fh.write("% from code/ch13/02_sn2011fe.py\n")
    for k, v in M.items():
        fh.write(f"\\providecommand{{\\{k}}}{{{v}}}\n")

# self-check: B max of SN 2011fe fell in mid-September 2011 near B = 10, its decline rate is
# ordinary (0.8 < dm15 < 1.6), and the tail falls near, but not slower than about, the cobalt rate.
assert 55805 < tB < 55825 and 9.5 < Bmax < 10.5, (tB, Bmax)
assert 0 < tV - tB < 5
assert 0.8 < dm15 < 1.6, dm15
assert 0.8 < kV < 2.5 and 0.8 < kB < 2.5, (kV, kB)
print("self-check ok")

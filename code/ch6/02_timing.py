r"""Timing curves of a pulsar with planets and of a pulsating star with a planet.

Question. Section "Other Ways to Find Planets" says a planet shows in the arrival times of a
steady clock. What does that signal look like for PSR B1257+12 and for V391 Peg?

Reads nothing. No machine-readable arrival times could be found (VizieR has no table of
PSR B1257+12 pulse arrival times, and for V391 Peg the O-C values of Silvotti et al. 2007 and
2018 exist only in figures; VizieR J/A+A/611/A85 holds the raw photometry only). The curves are
therefore computed from the published orbits.
  PSR B1257+12 (Konacki & Wolszczan 2003, ApJ 591, L147, Table 2; arXiv astro-ph/0305536)
      planet   x = a sin(i)/c (ms)   e         omega (deg)   P_orb (d)   Tp (MJD)
      A        0.0030                0.0       0.0           25.262      49765.1
      B        1.3106                0.0186    250.4         66.5419     49768.1
      C        1.4134                0.0252    108.3         98.2114     49766.5
  V391 Peg b (Silvotti et al. 2007, Nature 449, 189; Silvotti et al. 2018, A&A 611, A85)
      P_orb = 3.2 yr, m_p sin(i) = 3.2 M_Jup, a = 1.7 AU. These three numbers are quoted from the
      abstracts. The star mass 0.5 Msun is assumed here (the sdB mass is not measured), and
      the phase of the sine is arbitrary.
  The pulsar mass is taken as 1.4 Msun.

Computes the delay of each planet with the Roemer formula (Chapter 6, Section Roemer delay)
  dt = x [ (cos E - e) sin w + sqrt(1 - e^2) sin E cos w ],  E - e sin E = 2 pi (t - Tp)/P,
the sum of the three, and for each planet a_* sin(i) = c x, a from Kepler's third law and
m_p sin(i) = M a_* sin(i) / a (valid for m_p << M).

Writes
  results/ch6/timing_psr_B.dat, timing_psr_C.dat, timing_psr_sum.dat   days since MJD 49750, ms
  results/ch6/timing_peg.dat                                         years since 1999.0, seconds
  results/ch6/timing.tex   macros \SixTim...
"""
import os
import numpy as np

out = os.path.join("results", "ch6")
os.makedirs(out, exist_ok=True)
C, AU, MSUN, MEARTH, MJUP = 2.99792458e8, 1.495978707e11, 1.98847e30, 5.9722e24, 1.89813e27
YR = 365.25

def kepler_E(M, e):
    E = M.copy()
    for _ in range(50):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def delay_ms(t, x, e, w, P, Tp):
    E = kepler_E(2 * np.pi * (t - Tp) / P % (2 * np.pi), e)
    return x * ((np.cos(E) - e) * np.sin(w) + np.sqrt(1 - e**2) * np.sin(E) * np.cos(w))

# (x ms, e, w deg, P d, Tp MJD)
planets = {"A": (0.0030, 0.0, 0.0, 25.262, 49765.1),
           "B": (1.3106, 0.0186, 250.4, 66.5419, 49768.1),
           "C": (1.4134, 0.0252, 108.3, 98.2114, 49766.5)}
t = np.arange(0.0, 400.0 + 1e-9, 1.0)
d = {k: delay_ms(49750.0 + t, v[0], v[1], np.radians(v[2]), v[3], v[4]) for k, v in planets.items()}
tot = d["A"] + d["B"] + d["C"]
for name, y in (("B", d["B"]), ("C", d["C"]), ("sum", tot)):
    np.savetxt(os.path.join(out, f"timing_psr_{name}.dat"), np.c_[t, y], fmt="%.4f")

# V391 Peg: circular orbit, O-C = (a_* sin i / c) sin(2 pi (t - t0)/P)
Mstar = 0.5 * MSUN
Pp = 3.2 * YR
mp = 3.2 * MJUP
Mtot = Mstar + mp
a_peg = (6.674e-11 * Mtot * (Pp * 86400) ** 2 / (4 * np.pi**2)) ** (1 / 3)
astar_peg = mp / Mtot * a_peg
amp_peg = astar_peg / C
yr = np.arange(1999.0, 2009.0 + 1e-9, 0.02)
np.savetxt(os.path.join(out, "timing_peg.dat"), np.c_[yr - 1999.0, amp_peg * np.sin(2 * np.pi * (yr - 1999.0) / 3.2)], fmt="%.4f")

M = 1.4 * MSUN
mac = []
def add(n, v): mac.append(r"\newcommand{\SixTim%s}{%s}" % (n, v))
for k in "ABC":
    x, e, w, P, Tp = planets[k]
    astar = C * x * 1e-3
    a = (6.674e-11 * M * (P * 86400) ** 2 / (4 * np.pi**2)) ** (1 / 3)
    msini = M * astar / a / MEARTH
    add("x" + k, f"{x:.4g}")
    add("P" + k, f"{P:.2f}")
    add("a" + k, f"{a / AU:.2f}")
    add("astarkm" + k, f"{astar / 1e3:.0f}")
    add("m" + k, f"{msini:.2g}" if k == "A" else f"{msini:.1f}")
    if k == "B": mB = msini
    if k == "C": mC = msini
add("ratio", f"{planets['C'][3] / planets['B'][3]:.2f}")
add("repeat", f"{2 * planets['C'][3]:.0f}")
add("sumMax", f"{abs(tot).max():.1f}")
add("PegAmp", f"{amp_peg:.1f}")
add("PegP", "3.2")
add("PegAstarR", f"{astar_peg / 6.957e8:.1f}")
add("PegA", f"{a_peg / AU:.1f}")
add("PegM", "0.5")
add("PegPeriod", "349.5")
with open(os.path.join(out, "timing.tex"), "w") as fh:
    fh.write("\n".join(mac) + "\n")

# ---- self-checks ----
earth = MEARTH / (1.4 * MSUN + MEARTH) * AU / C * 1e3
assert abs(earth - 1.07) < 0.02, earth                      # chapter quotes 1.1 ms
assert abs(mB - 4.3 * np.sin(np.radians(53.4))) < 0.3, mB   # K&W 2003: 4.3 Me at i = 53 deg
assert abs(mC - 3.9 * np.sin(np.radians(47.3))) < 0.3, mC
assert abs(a_peg / AU - 1.7) < 0.1, a_peg / AU               # published 1.7 AU
assert 4.5 < amp_peg < 6.0, amp_peg                          # about 5 s
assert abs(tot).max() < 1.3106 + 1.4134 + 0.01
print(" ".join(mac))

r"""Extinction efficiency of a sphere against its size, and the B-to-V step that sets the colour excess.

Question. Section "Reddening and the Colour Excess" says E(B-V)/A_V = sigma(B)/sigma(V) - 1. Going from V
(0.55 um) to B (0.44 um) multiplies 2 pi a / lambda by 550/440 = 1.25 for a grain of any size, so the step
sigma(B)/sigma(V) is the factor by which the extinction efficiency grows over that 1.25 in size parameter.
Where on the Mie curve is the step 2.44 (tiny particles), 1.25 (the 1/lambda law), 1.32 (measured dust,
A_V = 3.1 E(B-V)) and 1 (large grains)? Is a single 0.1 um grain at 1.25?

Reads   nothing.

Computes Q_ext = sigma_ext / (pi a^2) for a sphere of refractive index m = 1.5 (a silicate-like grain, no
absorption) from the Mie series (Bohren & Huffman 1983, BHMIE: downward recurrence for the logarithmic
derivative, upward for the Riccati-Bessel functions), on x = 2 pi a / lambda from 0.02 to 100 (log grid), averaged over a +-15% spread in grain size,
and the step S(x) = Q(1.25 x) / Q(x), with x the size parameter in V.

Writes
  results/ch4/mie.dat   x, Q_ext(x), S(x) = Q(1.25 x)/Q(x)
  results/ch4/mie.tex   macros: x where S = 2.40 / 1.32 / 1.25 on the rising side, S at x_V = 1.14
                        (a = 0.1 um), and the size parameters of three example pairs
"""
import os
import numpy as np

M = 1.5


def qext_qsca(x, m=M):
    nstop = int(x + 4 * x ** (1 / 3) + 2)
    mx = m * x
    nmx = int(max(nstop, abs(mx)) + 16)
    D = np.zeros(nmx + 1, dtype=complex)
    for n in range(nmx, 0, -1):
        D[n - 1] = n / mx - 1 / (D[n] + n / mx)
    psi0, psi1 = np.cos(x), np.sin(x)
    chi0, chi1 = -np.sin(x), np.cos(x)
    xi1 = complex(psi1, -chi1)
    qe = qs = 0.0
    for n in range(1, nstop + 1):
        psi = (2 * n - 1) * psi1 / x - psi0
        chi = (2 * n - 1) * chi1 / x - chi0
        xi = complex(psi, -chi)
        da = D[n] / m + n / x
        db = m * D[n] + n / x
        an = (da * psi - psi1) / (da * xi - xi1)
        bn = (db * psi - psi1) / (db * xi - xi1)
        qe += (2 * n + 1) * (an + bn).real
        qs += (2 * n + 1) * (abs(an) ** 2 + abs(bn) ** 2)
        psi0, psi1, chi0, chi1 = psi1, psi, chi1, chi
        xi1 = complex(psi1, -chi1)
    return 2 * qe / x ** 2, 2 * qs / x ** 2


out = os.path.join("results", "ch4")
os.makedirs(out, exist_ok=True)

# fine log grid, wide enough that the size average and the 1.25 shift stay inside it
xf = np.logspace(np.log10(0.01), np.log10(160), 6000)
Qf = np.array([qext_qsca(v)[0] for v in xf])
# real grains are never all one size: average Q over a size spread of +-15% (uniform in log a).
# This removes the narrow resonance ripple of a single sphere and keeps the broad shape.
lx = np.log10(xf)
half = int(round(np.log10(1.15) / (lx[1] - lx[0])))
Qs = np.convolve(Qf, np.ones(2 * half + 1) / (2 * half + 1), mode="same")
keep = (xf >= 0.02) & (xf <= 100)
x, Q = xf[keep], Qs[keep]
S = np.interp(np.log10(1.25 * x), lx, Qs) / Q
np.savetxt(os.path.join(out, "mie.dat"), np.column_stack([x, Q, S]), fmt="%.6g",
           header="x = 2 pi a/lambda,  Q_ext averaged over +-15% in size,  S = Q(1.25x)/Q(x)   (m = 1.5)")

# self-checks: no absorption so Q_ext = Q_sca; Rayleigh limit; large-sphere limit Q -> 2
for v in (0.05, 1.0, 7.0, 60.0):
    qe, qs = qext_qsca(v)
    assert abs(qe - qs) < 1e-6 * qe, (v, qe, qs)
r = (M**2 - 1) / (M**2 + 2)
qr = qext_qsca(0.02)[0]  # single sphere, no averaging
assert abs(qr / (8 / 3 * 0.02**4 * r**2) - 1) < 1e-3, qr
assert abs(S[0] - 1.25**4) < 0.01, S[0]
# Q -> 2 only slowly (edge correction ~ x^(-2/3)), so check it is near 2 and still closing in
qa, qb = np.mean(Q[(x > 20) & (x < 40)]), np.mean(Q[x > 60])
assert abs(qb - 2) < 0.2 and abs(qb - 2) < abs(qa - 2), (qa, qb)


def first_x(target):
    """first x (rising side, before the main peak) where S falls to target"""
    i = np.argmax(S < target)
    return np.interp(target, [S[i], S[i - 1]], [x[i], x[i - 1]])


xa = 2 * np.pi * 0.1 / 0.55
S01 = np.interp(xa, x, S)
x240, x132, x125 = first_x(2.40), first_x(1.32), first_x(1.25)
ipk = np.argmax(Q)
big = x > 30
print(f"Rayleigh check Q(0.02) = {qr:.4g}; S(0.02) = {S[0]:.4f} (1.25^4 = {1.25**4:.4f})")
print(f"a = 0.1 um: x_V = {xa:.3f}, S = {S01:.3f}")
print(f"S = 2.40 at x = {x240:.3f};  S = 1.32 at x = {x132:.3f};  S = 1.25 at x = {x125:.3f}")
print(f"S min {S.min():.3f} at x = {x[np.argmin(S)]:.2f}")
print(f"main peak Q = {Q[ipk]:.3f} at x = {x[ipk]:.2f};  for x > 30, S ranges {S[big].min():.3f}..{S[big].max():.3f}, mean {S[big].mean():.3f}")
print(f"grain radius for S = 1.25 in V: {x125 * 0.55 / (2 * np.pi):.3f} um; for S = 1.32: {x132 * 0.55 / (2 * np.pi):.3f} um")

with open(os.path.join(out, "mie.tex"), "w") as f:
    f.write("% from code/ch4/01_mie_extinction.py\n")
    for name, val, fmt in [("FourMieSzeroone", S01, "%.2f"), ("FourMieXzeroone", xa, "%.2f"),
                           ("FourMieXonetwofive", x125, "%.2f"), ("FourMieXonethreetwo", x132, "%.2f"),
                           ("FourMieAonetwofive", x125 * 0.55 / (2 * np.pi), "%.2f"),
                           ("FourMiePeakQ", Q[ipk], "%.1f"), ("FourMiePeakX", x[ipk], "%.1f")]:
        f.write("\\newcommand{\\%s}{%s}\n" % (name, fmt % val))
print("self-check ok")

r"""The Airy pattern of a round mirror, and two stars at the Rayleigh separation.

Question. Section "Diffraction" states I/I0 = [2 J1(b)/b]^2 with b = pi D theta / lambda, its first
dark ring at b = 3.8317 (theta = 1.22 lambda/D), the light inside the first two dark rings, and the
26.5% dip between two equal stars 1.22 lambda/D apart. Compute them for the figure and the text.

Reads   nothing.

Computes
  - J0, J1 from their integral forms Jn(x) = (1/pi) int_0^pi cos(n t - x sin t) dt (trapezoid,
    4001 points, exact to ~1e-12 for these smooth periodic integrands).
  - the Airy profile on theta in units of lambda/D, 0..3.5; the zeros of J1 by bisection;
    encircled energy 1 - J0^2 - J1^2 at the first two zeros (a closed form for this pattern);
    the sum of two profiles 1.22 lambda/D apart and its central dip.

Writes
  results/ch5/airy.dat       theta (lambda/D), single profile, sum of two (second at +1.2197)
  results/ch5/airy.tex       \Five... macros
"""
import os
import numpy as np

out = os.path.join("results", "ch5")
os.makedirs(out, exist_ok=True)
tau = np.linspace(0, np.pi, 4001)


def J(n, x):
    x = np.atleast_1d(x)[:, None]
    return np.trapezoid(np.cos(n * tau - x * np.sin(tau)), tau, axis=1) / np.pi


def airy(th):  # th in units of lambda/D
    b = np.pi * np.atleast_1d(th)
    b = np.where(b == 0, 1e-12, b)
    return (2 * J(1, b) / b) ** 2


def zero(a, c):
    for _ in range(80):
        m = 0.5 * (a + c)
        if J(1, a)[0] * J(1, m)[0] <= 0:
            c = m
        else:
            a = m
    return 0.5 * (a + c)


z1, z2 = zero(3.0, 4.5), zero(6.5, 7.5)
enc = lambda b: 1 - J(0, b)[0] ** 2 - J(1, b)[0] ** 2
e1, e2 = enc(z1), enc(z2)
sep = z1 / np.pi
th = np.linspace(-1.5, 3.2, 941)
one = airy(th)
two = one + airy(th - sep)
dip = 1 - two[np.argmin(np.abs(th - sep / 2))]
np.savetxt(os.path.join(out, "airy.dat"), np.c_[th, one, airy(th - sep), two], fmt="%.4f %.6f %.6f %.6f")

M = {"FiveAiryZeroOne": f"{z1:.4f}", "FiveAiryZeroTwo": f"{z2:.4f}", "FiveAiryRing": f"{sep:.2f}",
     "FiveAiryEncOne": f"{100 * e1:.1f}", "FiveAiryEncTwo": f"{100 * e2:.1f}", "FiveAiryDip": f"{100 * dip:.1f}"}
with open(os.path.join(out, "airy.tex"), "w") as fh:
    fh.write("% from code/ch5/02_airy.py\n")
    for k, v in M.items():
        fh.write(f"\\providecommand{{\\{k}}}{{{v}}}\n")
print(M)

# self-check: textbook values of the first two zeros of J1 and the 83.8% / 91.0% encircled energy
assert abs(z1 - 3.8317) < 1e-3 and abs(z2 - 7.0156) < 1e-3, (z1, z2)
assert abs(e1 - 0.838) < 2e-3 and abs(e2 - 0.910) < 2e-3, (e1, e2)
assert 0.25 < dip < 0.28, dip
print("self-check ok")

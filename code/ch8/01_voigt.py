r"""Voigt profile for the line-profile figure of the ISM chapter.

Question. Figure "line profile" compares a Lorentzian and a Gaussian with the same peak and the
same half-width. What does their convolution, the Voigt profile, look like on the same axes?

Computes the Voigt profile (scipy.special.voigt_profile) for a Gaussian of half-width 1
(sigma = 1/sqrt(2 ln 2)) and a Lorentzian of half-width 1, scaled to peak 1, on x = -4.5..4.5,
and its half-width at half maximum.

Writes
  results/ch8/voigt.dat    x, profile
  results/ch8/voigt.tex    LaTeX macro \EightVoigtHWHM
"""
import os
import numpy as np
from scipy.special import voigt_profile
from scipy.optimize import brentq

out = os.path.join("results", "ch8")
os.makedirs(out, exist_ok=True)

sigma = 1.0 / np.sqrt(2.0 * np.log(2.0))
gamma = 1.0
x = np.linspace(-4.5, 4.5, 361)
peak = voigt_profile(0.0, sigma, gamma)
v = voigt_profile(x, sigma, gamma) / peak
np.savetxt(os.path.join(out, "voigt.dat"), np.column_stack([x, v]), fmt="%.6f")

hwhm = brentq(lambda t: voigt_profile(t, sigma, gamma) / peak - 0.5, 0.5, 4.0)
with open(os.path.join(out, "voigt.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\EightVoigtHWHM}}{{{hwhm:.2f}}}\n")
print(f"Voigt half-width (units of the common half-width): {hwhm:.4f}")

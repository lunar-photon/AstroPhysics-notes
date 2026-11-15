r"""Cepheids: finding a period, the period-luminosity relation, and a distance to the LMC.

Question. Section "Standard Candles, Cepheids, RR Lyrae and Miras" says a Cepheid's period gives its
luminosity. What do the data look like, how is the period read off a light curve, and how does a
distance come out?

Reads
  data/ch3/OGLE-LMC-CEP-1252_I.dat, _V.dat  OGLE-III time series (HJD-2450000, mag, error) of one
                               fundamental-mode LMC Cepheid, from the OIII-CVS file server
                               (astrouw.edu.pl/ogle/ogle3/OIII-CVS/lmc/cep/phot/)
  data/ch3/ogle3_lmc_cepF.dat  OIII-CVS catalogue of fundamental-mode LMC Cepheids (Soszynski et al.
                               2008, Acta Astron. 58, 163; VizieR J/AcA/58/163): ID, intensity-mean
                               I and V, period, period error, time of maximum, I amplitude, Fourier terms

Computes
  - Lomb-Scargle periodogram of the I series (numpy, no weights, mean removed) on a grid uniform in
    ln P from 1 to 100 d, then a fine grid over +-0.5% around the peak. The peak is P.
    Checked against the catalogue period to 0.1%.
  - the folded light curve, phase = frac((t - t0)/P) with t0 the catalogue time of maximum;
    intensity-mean magnitude m = -2.5 log10 <10^(-0.4 m_i)> (I and V);
    amplitude = max - min of a 3-harmonic Fourier fit to the folded I curve.
  - for the fundamental-mode catalogue, least-squares fits m = a + b log10 P in V and I, with an
    iterated 3-sigma clip (drop points beyond 3 times the rms of the residuals, refit, until none go).
  - the LMC distance modulus. The fitted V line at log10 P = 1 is V1 = a + b. The book calibration
    (Eq. as:eq:pl) gives M_V = -4.05 at log10 P = 1, so m - M = V1 + 4.05. Dust takes
    A_V = 3.1 E(B-V) with E(B-V) = 0.08 (typical LMC value, from memory), mu0 = m - M - A_V,
    d = 10 pc * 10^(mu0/5).

Writes
  results/ch3/cep_lc_raw.dat      t, I (all points)
  results/ch3/cep_periodogram.dat P, power (max in bins, for plotting)
  results/ch3/cep_folded.dat      phase, I (one cycle)
  results/ch3/cep_pl.dat          log10 P, V, I of the fundamental-mode Cepheids (with an I flag)
  results/ch3/cep_fits.dat        fit lines at the ends of the log P range
  results/ch3/cepheids.tex        LaTeX macros \Three...
"""
import os
import numpy as np

D, OUT = os.path.join("data", "ch3"), os.path.join("results", "ch3")
os.makedirs(OUT, exist_ok=True)
STAR = "OGLE-LMC-CEP-1252"

# ---------------- catalogue ----------------
ids, cat = [], []
for l in open(os.path.join(D, "ogle3_lmc_cepF.dat")):
    # fixed-width columns (README byte ranges); a missing value is "-" and becomes nan
    num = lambda s: float(s) if s.strip() not in ("", "-") else np.nan
    ids.append(l[:17])
    cat.append([num(l[19:25]), num(l[26:32]), num(l[33:44]), num(l[45:54]), num(l[56:66]), num(l[68:73])])  # I, V, P, eP, t_max, amp_I
cat = np.array(cat)
Imean, Vmean, Pcat, _, t0, ampcat = cat[list(ids).index(STAR)]
print("catalogue", STAR, Imean, Vmean, Pcat, t0, ampcat)

# ---------------- time series ----------------
tI, mI, eI = np.loadtxt(os.path.join(D, STAR + "_I.dat")).T
tV, mV, eV = np.loadtxt(os.path.join(D, STAR + "_V.dat")).T


def lomb_scargle(t, y, freq):
    """Classical Lomb-Scargle power at angular frequencies freq (unweighted, mean removed)."""
    y = y - y.mean()
    w = 2 * np.pi * freq
    p = np.empty(len(w))
    for i in range(0, len(w), 2000):
        wi = w[i:i + 2000, None]
        tau = np.arctan2(np.sin(2 * wi * t).sum(1), np.cos(2 * wi * t).sum(1)) / (2 * w[i:i + 2000])
        arg = wi * (t - tau[:, None])
        c, s = np.cos(arg), np.sin(arg)
        p[i:i + 2000] = 0.5 * (((c * y).sum(1)) ** 2 / (c * c).sum(1) + ((s * y).sum(1)) ** 2 / (s * s).sum(1)) / y.var() / len(y)
    return p


Pgrid = np.exp(np.linspace(np.log(1.0), np.log(100.0), 40000))
pow_ = lomb_scargle(tI, mI, 1 / Pgrid)
P0 = Pgrid[np.argmax(pow_)]
Pfine = P0 * np.linspace(0.995, 1.005, 4001)
P = Pfine[np.argmax(lomb_scargle(tI, mI, 1 / Pfine))]
print("periodogram peak", P0, "refined", P, "catalogue", Pcat, "diff", abs(P - Pcat) / Pcat)
assert abs(P - Pcat) / Pcat < 1e-3

# ---------------- folded curve, mean magnitudes, amplitude ----------------
phase = ((tI - t0) / P) % 1.0
imean = lambda m: -2.5 * np.log10(np.mean(10 ** (-0.4 * m)))
I_bar, V_bar = imean(mI), imean(mV)
ph = np.linspace(0, 1, 1001)
A = lambda x: np.column_stack([np.ones_like(x)] + [f(2 * np.pi * k * x) for k in (1, 2, 3) for f in (np.cos, np.sin)])
coef = np.linalg.lstsq(A(phase), mI, rcond=None)[0]
curve = A(ph) @ coef
amp = curve.max() - curve.min()
print("mean I, V", I_bar, V_bar, "amp", amp)
assert abs(I_bar - Imean) < 0.03 and abs(amp - ampcat) < 0.05

np.savetxt(os.path.join(OUT, "cep_lc_raw.dat"), np.column_stack([tI, mI]), fmt="%.5f %.3f")
np.savetxt(os.path.join(OUT, "cep_folded.dat"), np.column_stack([phase, mI]), fmt="%.5f %.3f")
nb = len(Pgrid) // 8
pp = pow_[:nb * 8].reshape(nb, 8).max(1)
PP = Pgrid[:nb * 8].reshape(nb, 8).mean(1)
np.savetxt(os.path.join(OUT, "cep_periodogram.dat"), np.column_stack([PP, pp]), fmt="%.5f %.5f")

# ---------------- period-luminosity relation ----------------
logP = np.log10(cat[:, 2])
V, I = cat[:, 1], cat[:, 0]


def clipfit(x, y):
    ok = np.isfinite(x) & np.isfinite(y)          # stars with a missing magnitude are left out
    keep = ok.copy()
    while True:
        b, a = np.polyfit(x[keep], y[keep], 1)
        r = y - (a + b * x)
        s = r[keep].std()
        new = ok & (np.abs(r) < 3 * s)
        if (new == keep).all():
            return a, b, s, keep
        keep = new


aV, bV, sV, kV = clipfit(logP, V)
aI, bI, sI, kI = clipfit(logP, I)
print("V fit", aV, bV, sV, kV.sum(), "I fit", aI, bI, sI, kI.sum(), "of", len(logP))
assert -3.2 < bV < -2.2 and -3.4 < bI < -2.4

np.savetxt(os.path.join(OUT, "cep_pl.dat"), np.column_stack([logP, V, I, kV, kI]), fmt="%.5f %.3f %.3f %d %d", comments="")
x = np.array([logP.min(), logP.max()])
np.savetxt(os.path.join(OUT, "cep_fits.dat"), np.column_stack([x, aV + bV * x, aI + bI * x]), fmt="%.4f")

# ---------------- distance ----------------
V1 = aV + bV
mM = V1 + 4.05
AV = 3.1 * 0.08
mu0 = mM - AV
d_kpc = 10 ** (mu0 / 5 + 1) / 1e3
print("V(logP=1)", V1, "m-M", mM, "A_V", AV, "mu0", mu0, "d kpc", d_kpc)
assert 40 < d_kpc < 60
# self-check against the accepted value, mu = 18.48 (50 kpc), within 0.4 mag
assert abs(mu0 - 18.48) < 0.4

mac = {
    "CepName": STAR, "CepN": f"{kV.sum()}", "CepNtotal": f"{len(logP)}",
    "CepPcat": f"{Pcat:.4f}", "CepP": f"{P:.4f}", "CepPdiff": f"{abs(P - Pcat) / Pcat * 100:.3f}",
    "CepAmp": f"{amp:.2f}", "CepIbar": f"{I_bar:.2f}", "CepVbar": f"{V_bar:.2f}",
    "CepNpoints": f"{len(tI)}", "CepSpan": f"{(tI.max() - tI.min()) / 365.25:.1f}",
    "CepVslope": f"{bV:.2f}", "CepIslope": f"{bI:.2f}", "CepVscatter": f"{sV:.2f}", "CepIscatter": f"{sI:.2f}",
    "CepVone": f"{V1:.2f}", "CepMM": f"{mM:.2f}", "CepAV": f"{AV:.2f}", "CepMu": f"{mu0:.2f}",
    "CepDist": f"{d_kpc:.1f}",
}
with open(os.path.join(OUT, "cepheids.tex"), "w") as fh:
    for k, v in mac.items():
        fh.write("\\newcommand{\\Three%s}{%s}\n" % (k, v))
print(open(os.path.join(OUT, "cepheids.tex")).read())

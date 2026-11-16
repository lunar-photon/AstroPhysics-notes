r"""Four SDSS spectra (a star, a galaxy, an HII region, a quasar) and the imaging colours of objects that have spectra.

Question. Section "Telling Stars, Galaxies, Nebulae and Quasars Apart" asks how SDSS knows what a
point of light is. What do the spectra of the four kinds look like, how do their redshifts and line
widths come out of the line centres, and what does the imaging alone say?

Reads
  data/ch14/spectra/spec-PPPP-MMMMM-FFFF.fits   four SDSS DR17 spec-lite files (run2d 26, all
                              zWarning = 0): HDU 1 COADD (flux, loglam, ivar, wdisp), HDU 2
                              SPECOBJ (pipeline class, subclass, z, velDisp, S/N), HDU 3 SPZLINE
                              (the pipeline's Gaussian line fits).
  data/ch14/colours.csv       SkyServer SQL join of SpecObj with PhotoObj (DR17, zWarning = 0,
                              sciencePrimary, clean photometry, errors < 0.1 in u and < 0.05 in g, r,
                              psfMag_r < 19.5, a thinned subset by specObjID modulo): class, z,
                              psfMag u g r, modelMag_r.

Computes
  - the redshift of each object from its own line centres, 1 + z = lambda_obs / lambda_rest, with
    VACUUM rest wavelengths (SDSS wavelengths are vacuum). Each line gets a Gaussian plus a straight
    continuum, fitted by weighted least squares. Emission lines for the nebula and the quasar,
    absorption lines for the star and the galaxy.
  - line widths. sigma_obs in km/s from the fitted width, Delta v = c Delta lambda / lambda. The
    spectrograph's own width comes from the wdisp column (pixels of 69 km/s). The FWHM is
    2.355 sigma, and the intrinsic width is sqrt(obs^2 - inst^2).
  - for the quasar, a broad plus narrow Gaussian for H beta (narrow width and place from [O III]).
  - the pipeline's HDU 3 values for comparison.
  - the colour and shape statistics of the imaging sample.

Writes
  results/ch14/spec_{star,galaxy,nebula,quasar}.dat   observed wavelength (nm), binned flux
                              (3 pixels per bin, divided by its peak), about 1280 points each
  results/ch14/spec_ticks_{star,galaxy,nebula,quasar}.tex   labelled marks at the observed lines
  results/ch14/colours_a.png, colours_b.png   transparent point images, g-r on x, u-g (a) and
                              psfMag_r - modelMag_r (b) on y, exact axes ranges (see AX below)
  results/ch14/spectra.tex    LaTeX macros \FourteenSpec... and \FourteenCol...
"""
import os
import numpy as np
from astropy.io import fits
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

C = 299792.458                      # km/s
PIX = C * np.log(10) * 1e-4         # km/s per pixel (log10 lambda step 1e-4)
FWHM = 2.0 * np.sqrt(2.0 * np.log(2.0))
out = os.path.join("results", "ch14")
os.makedirs(out, exist_ok=True)

FILES = {
    "star": "spec-2305-54414-0097.fits",
    "galaxy": "spec-0564-52224-0507.fits",
    "nebula": "spec-1324-53088-0234.fits",
    "quasar": "spec-1744-53055-0630.fits",
}
# Vacuum rest wavelengths in Angstrom. Emission lines are those of the pipeline's own table
# (HDU 3 LINEWAVE). Absorption lines are from memory (air value converted to vacuum).
EMI = {"Hbeta": 4862.68, "[OIII]4959": 4960.29, "[OIII]5007": 5008.24, "Halpha": 6564.61,
       "[NII]6549": 6549.86, "[NII]6585": 6585.27, "[SII]6718": 6718.29, "[SII]6733": 6732.68,
       "Hgamma": 4341.68, "[OII]3727": 3727.09}
ABS = {"CaK": 3934.78, "CaH": 3969.59, "G": 4305.6, "Hbeta": 4862.68, "MgB": 5176.0, "CaI": 4227.93, "FeI": 5271.04,
       "NaD2": 5891.58, "NaD1": 5897.56, "Halpha": 6564.61}


def load(name):
    h = fits.open(os.path.join("data", "ch14", "spectra", FILES[name]))
    d = h[1].data
    w = 10.0 ** d["loglam"]
    s = h[2].data[0]
    meta = dict(cls=s["CLASS"].strip(), sub=s["SUBCLASS"].strip(), z=float(s["Z"]),
                vdisp=float(s["VDISP"]), sn=float(s["SN_MEDIAN_ALL"]),
                ra=float(s["PLUG_RA"]), dec=float(s["PLUG_DEC"]), zwarn=int(s["ZWARNING"]))
    lines = {n.strip(): (float(z), float(sg), float(a)) for n, z, sg, a in
             zip(h[3].data["LINENAME"], h[3].data["LINEZ"], h[3].data["LINESIGMA"], h[3].data["LINEAREA"])}
    return h, w, d["flux"].astype(float), d["ivar"].astype(float), d["wdisp"].astype(float), meta, lines


def gauss(x, c, s):
    return np.exp(-0.5 * ((x - c) / s) ** 2)


def fit_line(w, f, iv, lam, hw, sign, sig0=4.0):
    """Gaussian plus straight line in lam +- hw (Angstrom). Returns centre, sigma (A), amplitude."""
    m = (w > lam - hw) & (w < lam + hw) & (iv > 0)
    x, y, e = w[m], f[m], 1.0 / np.sqrt(iv[m])
    base = np.median(y)
    a0 = sign * (np.percentile(y, 95) - base if sign > 0 else base - np.percentile(y, 5))
    model = lambda x, c0, c1, a, c, s: c0 + c1 * (x - lam) + a * gauss(x, c, s)
    p, _ = curve_fit(model, x, y, p0=[base, 0.0, a0, lam, sig0], sigma=e, maxfev=20000,
                     bounds=([-np.inf, -np.inf, -np.inf, lam - hw / 2, 0.3], [np.inf, np.inf, np.inf, lam + hw / 2, hw / 2]))
    return p[3], p[4], p[2]


def fit_doublet(w, f, iv, lamA, lamB, hw, sign, sig0=4.0):
    """Two Gaussians of equal width at a fixed ratio of centres. Returns centre of A, sigma."""
    lam = 0.5 * (lamA + lamB)
    m = (w > lam - hw) & (w < lam + hw) & (iv > 0)
    x, y, e = w[m], f[m], 1.0 / np.sqrt(iv[m])
    base = np.median(y)
    model = lambda x, c0, c1, a1, a2, c, s: (c0 + c1 * (x - lam) + a1 * gauss(x, c, s)
                                             + a2 * gauss(x, c * lamB / lamA, s))
    p, _ = curve_fit(model, x, y, p0=[base, 0.0, -0.3 * base, -0.3 * base, lamA, sig0], sigma=e,
                     bounds=([-np.inf, -np.inf, -np.inf, -np.inf, lamA - hw / 2, 0.3],
                             [np.inf, np.inf, np.inf, np.inf, lamA + hw / 2, hw / 2]))
    return p[4], p[5]


def sig_kms(sig_A, centre):
    return C * sig_A / centre


def inst_kms(w, wd, centre):
    return float(np.interp(centre, w, wd)) * PIX


report = {}
mac = []   # (name, value string)


def put(name, val):
    mac.append((name, val))


HDR = {}
data = {k: load(k) for k in FILES}
for k, (h, w, f, iv, wd, meta, lines) in data.items():
    if k == "star":
        h.info()
        for i in (1, 2, 3):
            print("HDU", i, "columns:", h[i].columns.names[:12], "...")
    print(k, meta, "wave range", round(w.min(), 1), round(w.max(), 1), "npix", w.size)

# ---------------- star: absorption lines
res = {}
h, w, f, iv, wd, meta, lines = data["star"]
zs = []
starsig = {}
for nm in ("CaI", "Halpha", "Hbeta"):
    lam = ABS[nm]
    hw = {"CaI": 10, "Halpha": 15, "Hbeta": 12}[nm]
    c, s, a = fit_line(w, f, iv, lam, hw, -1, 3.0)
    z = c / lam - 1
    zs.append(z)
    starsig[nm] = sig_kms(s, c)
    print(f"star {nm}: centre {c:.2f} A, z = {z:.6f}, sigma_obs = {sig_kms(s, c):.0f} km/s")
c, s = fit_doublet(w, f, iv, ABS["NaD2"], ABS["NaD1"], 18, -1, 2.5)
zs.append(c / ABS["NaD2"] - 1)
print(f"star NaD: z = {zs[-1]:.6f}, sigma_obs = {sig_kms(s, c):.0f} km/s")
res["star"] = (np.mean(zs), np.std(zs, ddof=1))
print("star z own", res["star"], "pipeline", meta["z"])

# ---------------- galaxy: absorption lines
h, w, f, iv, wd, meta, lines = data["galaxy"]
zg = []
galsig = {}
zp = meta["z"]
for nm in ("CaK", "G", "MgB"):
    lam = ABS[nm] * (1 + zp)
    c, s, a = fit_line(w, f, iv, lam, 40, -1, 6.0)
    zg.append(c / ABS[nm] - 1)
    print(f"galaxy {nm}: centre {c:.2f} A, z = {zg[-1]:.6f}, sigma_obs = {sig_kms(s, c):.0f} km/s,"
          f" instrument sigma {inst_kms(w, wd, c):.0f} km/s")
    galsig[nm] = sig_kms(s, c)
    if nm == "CaK":
        gal_sig_cak = sig_kms(s, c)
c, s = fit_doublet(w, f, iv, ABS["NaD2"] * (1 + zp), ABS["NaD1"] * (1 + zp), 50, -1, 5.0)
zg.append(c / ABS["NaD2"] - 1)
print(f"galaxy NaD: z = {zg[-1]:.6f}, sigma_obs = {sig_kms(s, c):.0f} km/s")
res["galaxy"] = (np.mean(zg), np.std(zg, ddof=1))
print("galaxy z own", res["galaxy"], "pipeline", meta["z"], "velDisp", meta["vdisp"],
      "wdisp sigma (km/s) at 5000 A obs:", inst_kms(w, wd, 5000.0 * 1.0))

# ---------------- nebula: emission lines
h, w, f, iv, wd, meta, lines = data["nebula"]
zn, widths = [], {}
zp = meta["z"]
for nm in ("Halpha", "[NII]6585", "[NII]6549", "[SII]6718", "[SII]6733", "[OIII]5007", "[OIII]4959", "Hbeta"):
    lam = EMI[nm] * (1 + zp)
    c, s, a = fit_line(w, f, iv, lam, 10, +1, 1.8)
    zn.append(c / EMI[nm] - 1)
    widths[nm] = (sig_kms(s, c), inst_kms(w, wd, c))
    if nm == "Halpha":
        cen_ha, sig_ha_A = c, s
    print(f"nebula {nm}: centre {c:.2f} A, z = {zn[-1]:.6f}, sigma_obs = {widths[nm][0]:.0f} km/s,"
          f" instrument {widths[nm][1]:.0f} km/s, amplitude {a:.1f}")
res["nebula"] = (np.mean(zn), np.std(zn, ddof=1))
print("nebula z own", res["nebula"], "pipeline", meta["z"])
neb_ha = widths["Halpha"]
neb_o3 = widths["[OIII]5007"]
print("pipeline sigma Halpha, [OIII]5007:", lines["H_alpha"], lines["[O_III] 5007"])

# ---------------- quasar: [O III] narrow, H beta broad + narrow
h, w, f, iv, wd, meta, lines = data["quasar"]
zp = meta["z"]
lam = EMI["[OIII]5007"] * (1 + zp)
c5, s5, a5 = fit_line(w, f, iv, lam, 40, +1, 5.0)
zq_o3 = c5 / EMI["[OIII]5007"] - 1
print(f"quasar [OIII]5007: z = {zq_o3:.6f}, sigma_obs = {sig_kms(s5, c5):.0f} km/s")
cH = EMI["Hbeta"] * (1 + zq_o3)
c4 = EMI["[OIII]4959"] * (1 + zq_o3)
lo, hi = cH - 180, c4 + 40
m = (w > lo) & (w < hi) & (iv > 0)
x, y, e = w[m], f[m], 1.0 / np.sqrt(iv[m])
xm = 0.5 * (lo + hi)
model = lambda x, c0, c1, ab, cb, sb, an, a4: (c0 + c1 * (x - xm) + ab * gauss(x, cb, sb)
                                                + an * gauss(x, cH, s5) + a4 * gauss(x, c4, s5))
p, pc = curve_fit(model, x, y, p0=[np.median(y), 0, np.max(y) - np.median(y), cH, 40.0, 0.0, 0.0], sigma=e,
                  bounds=([-np.inf, -np.inf, 0, cH - 60, 12.0, 0, 0], [np.inf, np.inf, np.inf, cH + 60, 90.0, np.inf, np.inf]))
sb_kms = sig_kms(p[4], p[3])
fw_broad = FWHM * sb_kms
print(f"quasar Hbeta broad: centre {p[3]:.1f} A, sigma {sb_kms:.0f} km/s, FWHM {fw_broad:.0f} km/s, "
      f"z_broad = {p[3] / EMI['Hbeta'] - 1:.5f}")
print("pipeline Hbeta, Halpha, [OIII]5007:", lines["H_beta"], lines["H_alpha"], lines["[O_III] 5007"])
fw_pipe_hb = FWHM * lines["H_beta"][1]
fw_o3 = FWHM * sig_kms(s5, c5)
fw_o3_inst = FWHM * inst_kms(w, wd, c5)
# redshift from the narrow lines of the quasar
zq_n = []
for nm in ("[OIII]5007", "[OIII]4959", "Hbeta", "Halpha"):
    lamn = EMI[nm] * (1 + zq_o3)
    if nm in ("[OIII]5007", "[OIII]4959"):
        c, s, a = fit_line(w, f, iv, lamn, 40 if nm == "[OIII]5007" else 25, +1, 5.0)
        zq_n.append(c / EMI[nm] - 1)
res["quasar"] = (np.mean(zq_n), np.std(zq_n, ddof=1))
print("quasar z own ([OIII] pair)", res["quasar"], "pipeline", meta["z"])

# ---------------- binned spectra and ticks
TICK_ROWS = {
    "star": [("Ca H,K", "CaK", 0), ("G", "G", 1), ("H$\\beta$", "Hbeta", 0), ("Mg b", "MgB", 1),
             ("Na D", "NaD2", 0), ("H$\\alpha$", "Halpha", 1)],
    "galaxy": [("Ca H,K", "CaK", 0), ("G", "G", 1), ("H$\\beta$", "Hbeta", 0), ("Mg b", "MgB", 1),
               ("Na D", "NaD2", 0), ("H$\\alpha$", "Halpha", 1)],
    "nebula": [("H$\\beta$", "Hbeta", 0), ("[O\\,III]", "[OIII]5007", 1),
               ("H$\\alpha$,[N\\,II]", "Halpha", 1), ("[S\\,II]", "[SII]6718", 0)],
    "quasar": [("H$\\gamma$", "Hgamma", 0), ("H$\\beta$", "Hbeta", 0), ("[O\\,III]", "[OIII]5007", 1),
               ("H$\\alpha$", "Halpha", 1)],
}
zfinal = {"star": res["star"][0], "galaxy": res["galaxy"][0], "nebula": res["nebula"][0], "quasar": res["quasar"][0]}
for k, (h, w, f, iv, wd, meta, lines) in data.items():
    ok = (w > 3800) & (w < 9200)
    w2, f2 = w[ok], f[ok]
    nb = w2.size // 3
    wb = w2[: nb * 3].reshape(nb, 3).mean(axis=1)
    fb = f2[: nb * 3].reshape(nb, 3).mean(axis=1)
    sm = np.convolve(fb, np.ones(5) / 5, mode="same")
    norm = fb.max() if k == "nebula" else sm[5:-5].max()
    fb = fb / norm
    np.savetxt(os.path.join(out, f"spec_{k}.dat"), np.c_[wb / 10.0, fb], fmt="%.4f", header="lambda_obs_nm flux_norm")
    z = zfinal[k]
    with open(os.path.join(out, f"spec_ticks_{k}.tex"), "w") as fh:
        for lab, key, row in TICK_ROWS[k]:
            rest = (EMI.get(key) if k in ("nebula", "quasar") else ABS[key])
            if k == "nebula" and key == "Halpha":
                rest = EMI["Halpha"]
            fh.write(f"\\specmark{{{rest * (1 + z) / 10.0:.2f}}}{{{row}}}{{{lab}}}\n")
    print(k, "binned points", wb.size, "norm", norm)

# ---------------- imaging
rows = [l.strip().split(",") for l in open(os.path.join("data", "ch14", "colours.csv")).read().strip().split("\n")[1:]]
cls = np.array([r[0] for r in rows])
M = np.array([[float(v) for v in r[1:]] for r in rows])
u, g, r, mr = M[:, 1], M[:, 2], M[:, 3], M[:, 4]
ug, gr, pm = u - g, g - r, r - mr
col = {"STAR": "#1B4F72", "GALAXY": "#A13D2C", "QSO": "#3C8C50"}
AX = dict(a=(-0.5, 2.0, -0.3, 3.3), b=(-0.5, 2.0, -0.3, 3.3))   # same y span so the panels line up; 6 of 5563 points fall outside   # x0, x1, y0, y1
cm = 1 / 2.54
W, H = 5.8, 5.2   # cm
for key, yv in (("a", ug), ("b", pm)):
    x0, x1, y0, y1 = AX[key]
    fig = plt.figure(figsize=(W * cm, H * cm))
    ax = fig.add_axes([0, 0, 1, 1])
    for c in ("GALAXY", "STAR", "QSO"):
        s = cls == c
        ax.scatter(gr[s], yv[s], s=2.2, c=col[c], alpha=0.55, linewidths=0, rasterized=True)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.axis("off")
    fig.savefig(os.path.join(out, f"colours_{key}.png"), dpi=500, transparent=True)
    plt.close(fig)
nS, nG, nQ = [(cls == c).sum() for c in ("STAR", "GALAXY", "QSO")]
S, G, Q = cls == "STAR", cls == "GALAXY", cls == "QSO"
f_star_pt = np.mean(pm[S] < 0.15)
f_qso_pt = np.mean(pm[Q] < 0.15)
f_gal_ext = np.mean(pm[G] > 0.15)
blue = S & (gr < 0.4)
med_ug_star = np.median(ug[blue])
med_ug_qso = np.median(ug[Q])
f_qso_blue = np.mean(ug[Q] < 0.6)
f_star_blue = np.mean(ug[S] < 0.6)
f_star_blue_gr = np.mean(ug[blue] < 0.6)
print(f"N star {nS} galaxy {nG} qso {nQ}")
print(f"psf-model < 0.15: stars {f_star_pt:.3f}, qso {f_qso_pt:.3f}; galaxies above {f_gal_ext:.3f}")
print(f"median u-g: stars with g-r<0.4 {med_ug_star:.2f}, qso {med_ug_qso:.2f}; frac u-g<0.6 qso {f_qso_blue:.3f}, stars {f_star_blue:.3f}, stars g-r<0.4 {f_star_blue_gr:.3f}")
print("psf-model medians", np.median(pm[S]), np.median(pm[Q]), np.median(pm[G]))
print("axes ranges: u-g", AX["a"], "psf-model", AX["b"], "outside-range fractions", np.mean((gr < -0.5) | (gr > 2) | (ug < -0.3) | (ug > 3.3)), np.mean((pm < -0.3) | (pm > 3.3)))

# ---------------- macros
sk = data
put("StarZ", f"{res['star'][0]:.6f}")
put("StarZpipe", f"{sk['star'][5]['z']:.6f}")
put("StarV", f"{res['star'][0] * C:.0f}")
put("StarVpipe", f"{sk['star'][5]['z'] * C:.0f}")
put("StarSN", f"{sk['star'][5]['sn']:.0f}")
put("GalZ", f"{res['galaxy'][0]:.5f}")
put("GalZpipe", f"{sk['galaxy'][5]['z']:.5f}")
put("GalVdisp", f"{sk['galaxy'][5]['vdisp']:.0f}")
put("GalSN", f"{sk['galaxy'][5]['sn']:.0f}")
put("GalSigCaK", f"{galsig['CaK']:.0f}")
put("GalSigMgb", f"{galsig['MgB']:.0f}")
put("StarSigHa", f"{starsig['Halpha']:.0f}")
put("NebZ", f"{res['nebula'][0]:.6f}")
put("NebZpipe", f"{sk['nebula'][5]['z']:.6f}")
put("NebV", f"{res['nebula'][0] * C:.0f}")
put("NebSN", f"{sk['nebula'][5]['sn']:.0f}")
put("NebFwhmHa", f"{FWHM * neb_ha[0]:.0f}")
put("NebFwhmOIII", f"{FWHM * neb_o3[0]:.0f}")
put("NebFwhmInst", f"{FWHM * neb_ha[1]:.0f}")
put("QsoZ", f"{res['quasar'][0]:.4f}")
put("QsoZpipe", f"{sk['quasar'][5]['z']:.4f}")
put("QsoSN", f"{sk['quasar'][5]['sn']:.0f}")
put("QsoFwhmHb", f"{fw_broad:.0f}")
put("QsoFwhmHbPipe", f"{fw_pipe_hb:.0f}")
put("QsoFwhmOIII", f"{fw_o3:.0f}")
put("ColNStar", f"{nS}")
put("ColNGal", f"{nG}")
put("ColNQso", f"{nQ}")
put("ColStarPoint", f"{100 * f_star_pt:.0f}")
put("ColQsoPoint", f"{100 * f_qso_pt:.0f}")
put("ColGalExt", f"{100 * f_gal_ext:.0f}")
put("ColUGStar", f"{med_ug_star:.2f}")
put("ColUGQso", f"{med_ug_qso:.2f}")
put("ColQsoBlue", f"{100 * f_qso_blue:.0f}")
put("ColStarBlue", f"{100 * f_star_blue:.0f}")
put("NebHaObs", f"{cen_ha / 10:.3f}")
put("NebHaRest", f"{EMI['Halpha'] / 10:.3f}")
put("NebHaZ", f"{cen_ha / EMI['Halpha'] - 1:.6f}")
put("NebHaV", f"{C * (cen_ha / EMI['Halpha'] - 1):.0f}")
put("NebHaDl", f"{FWHM * sig_ha_A / 10:.2f}")
put("NebGasHa", f"{np.sqrt((FWHM * neb_ha[0]) ** 2 - (FWHM * neb_ha[1]) ** 2):.0f}")
put("NebGasOIII", f"{np.sqrt((FWHM * neb_o3[0]) ** 2 - (FWHM * neb_o3[1]) ** 2):.0f}")
put("GalV", f"{res['galaxy'][0] * C:.0f}")
put("QsoHbCentre", f"{p[3] / 10:.1f}")
put("QsoHbDl", f"{FWHM * p[4] / 10:.1f}")
put("QsoVz", f"{res['quasar'][0] * C:.0f}")
put("InstFwhm", f"{FWHM * PIX * float(np.median(data['nebula'][4])):.0f}")
with open(os.path.join(out, "spectra.tex"), "w") as fh:
    for n, v in mac:
        fh.write(f"\\providecommand{{\\FourteenSpec{n}}}{{{v}}}\n".replace("FourteenSpecCol", "FourteenCol"))
for n, v in mac:
    print(n, v)

# ---------------- self-check
for k in FILES:
    assert data[k][5]["zwarn"] in (0, 16)
assert data["nebula"][5]["cls"] == "GALAXY"
assert data["star"][5]["cls"] == "STAR" and data["quasar"][5]["cls"] == "QSO"
assert abs(res["star"][0] - data["star"][5]["z"]) * C < 100
assert abs(res["galaxy"][0] - data["galaxy"][5]["z"]) * C < 150
assert abs(res["nebula"][0] - data["nebula"][5]["z"]) * C < 40
assert abs(res["quasar"][0] - data["quasar"][5]["z"]) * C < 150   # narrow lines vs the pipeline z, which leans on the shifted broad lines
assert 3000 < fw_broad < 9000
assert abs(PIX - 69.02) < 0.05
assert nS > 1000 and nG > 2000 and nQ > 1000
print("self-check ok")

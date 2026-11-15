# Lyman-alpha absorption by gas clouds between us and a quasar.
# (awk port of the planned cluster script; the cluster was unreachable on 2026-11-12.)
#
# Computes
#   - the Lyman-alpha cross-section sigma(nu) = (e^2 / 4 eps0 m_e c) f phi(nu) with a Doppler
#     (Gaussian) profile of parameter b. shortcut: no damping wings; they matter only for
#     N > ~1e19 cm^-2, and the forest here stops at 1e17 cm^-2,
#   - a quasar spectrum: continuum F ~ lambda^-1.5 plus a Gaussian Lyman-alpha emission line at
#     121.567 (1 + z_q) nm (z_q = 3, FWHM 3000 km/s, peak 3 x continuum),
#   - case A: three clouds at z = 2.55, 2.75, 2.90 (N = 3e14 cm^-2, b = 30 km/s),
#     transmission exp(-tau), each dip at 121.567 (1 + z) nm,
#   - case B: a forest between z = 2.0 and z_q, Poisson in z with dN/dz = 6.1 (1+z)^2.47 above
#     N = 10^13.1 cm^-2 (Kim et al. 2002), N from dn/dN ~ N^-1.5 between 10^12.5 and 10^17 cm^-2,
#     b uniform in 20-40 km/s (awk srand(16), so the draw is fixed for a given awk),
#   - the Gunn-Peterson depth tau_GP = (e^2 / 4 eps0 m_e c) f lambda_alpha n_HI / H(z) of a fully
#     neutral IGM at z = 3 and 6 (h = 0.674, Omega_b h^2 = 0.0224, Y = 0.245, Omega_m = 0.315),
#     and the neutral fraction giving tau = 1 at z = 3.
# Writes results/ch16/lya_three.dat, lya_forest.dat (lambda_obs nm, F with, F without) and lya.tex.
# Usage (from the repo root): awk -f code/ch16/03_lya_forest.awk

function quasar(lam,   cont, w, L) {
  L = lam_a * (1 + zq)
  cont = (lam / L)^(-1.5)
  w = L * 3000e3 / c / 2.355
  return cont * (1 + 2.0 * exp(-0.5 * ((lam - L) / w)^2))
}
# add the optical depth of one cloud to tau[] on the grid lam0 + i*dl, i = 0..n
function add_cloud(z, Ncm2, bkms, lam0, dl, n,   lc, sl, i, i1, i2, lam, nu, sD, x) {
  lc = lam_a * (1 + z)
  sD = nu_a * bkms * 1e3 / c / sqrt(2)                 # Gaussian sigma in frequency
  sl = lc * sD / nu_a                                   # the same in observed wavelength
  i1 = int((lc - 10 * sl - lam0) / dl); if (i1 < 0) i1 = 0
  i2 = int((lc + 10 * sl - lam0) / dl) + 1; if (i2 > n) i2 = n
  for (i = i1; i <= i2; i++) {
    lam = lam0 + i * dl
    nu = c / (lam / (1 + z))                            # frequency in the cloud's frame
    x = (nu - nu_a) / sD
    tau[i] += Ncm2 * 1e4 * sigma0 * exp(-0.5 * x * x) / (sqrt(2 * pi) * sD)
  }
}
function poisson(mu,   L, p, k) { L = exp(-mu); p = 1; k = 0; do { k++; p *= rand() } while (p > L); return k - 1 }
function tex(s,   m, x) {
  if (s !~ /e/) return s
  split(s, m, "e"); x = m[2] + 0
  if (m[1] == "1" || m[1] == "1.0") return "10^{" x "}"
  return m[1] "\\times10^{" x "}"
}
function fail(msg) { print "SELF-CHECK FAILED: " msg > "/dev/stderr"; exit 1 }
BEGIN {
  pi = 3.141592653589793
  c = 2.998e8; e = 1.602e-19; eps0 = 8.854e-12; m_e = 9.109e-31; m_H = 1.6735e-27
  lam_a = 121.567e-9; f_osc = 0.4164
  nu_a = c / lam_a
  sigma0 = e^2 / (4 * eps0 * m_e * c) * f_osc          # integral of sigma over nu (m^2 Hz)
  zq = 3.0
  out = "results/ch16/"

  # ---- case A: three clouds ----
  nA = 4000; l0 = 405e-9; dl = 100e-9 / nA
  for (i = 0; i <= nA; i++) tau[i] = 0
  zA[1] = 2.55; zA[2] = 2.75; zA[3] = 2.90
  for (j = 1; j <= 3; j++) add_cloud(zA[j], 3e14, 30.0, l0, dl, nA)
  minT = 1
  for (i = 0; i <= nA; i++) {
    lam = l0 + i * dl; F = quasar(lam)
    printf "%.5f %.5f %.5f\n", lam * 1e9, F * exp(-tau[i]), F > (out "lya_three.dat")
    if (exp(-tau[i]) < minT) { minT = exp(-tau[i]); lmin = lam }
  }
  close(out "lya_three.dat")
  # the deepest dip must sit on one of the three lines 121.567 (1 + z) nm
  ok = 0
  for (j = 1; j <= 3; j++) if (lmin - lam_a * (1 + zA[j]) < 2 * dl && lam_a * (1 + zA[j]) - lmin < 2 * dl) ok = 1
  if (!ok) fail("deepest dip at " lmin)

  # ---- case B: a forest ----
  srand(16)
  logNlo = 12.5; logNhi = 17.0; logNref = 13.1; beta = 1.5
  fr = (10^(logNref * (1 - beta)) - 10^(logNhi * (1 - beta))) / (10^(logNlo * (1 - beta)) - 10^(logNhi * (1 - beta)))
  nz = 2000
  cum[0] = 0
  for (k = 0; k <= nz; k++) { zg[k] = 2.0 + k * (zq - 2.0) / nz; dndz[k] = 6.1 * (1 + zg[k])^2.47 / fr }
  for (k = 1; k <= nz; k++) cum[k] = cum[k - 1] + 0.5 * (dndz[k] + dndz[k - 1]) * (zg[k] - zg[k - 1])
  nlines = poisson(cum[nz])
  aN = 10^(logNlo * (1 - beta)); bN = 10^(logNhi * (1 - beta))
  nB = 20000; l0B = 400e-9; dlB = 100e-9 / nB
  delete tau
  for (i = 0; i <= nB; i++) tau[i] = 0
  for (q = 1; q <= nlines; q++) {
    r = rand() * cum[nz]                                # inverse CDF in z
    lo = 0; hi = nz
    while (hi - lo > 1) { mid = int((lo + hi) / 2); if (cum[mid] < r) lo = mid; else hi = mid }
    z = zg[lo] + (r - cum[lo]) / (cum[hi] - cum[lo]) * (zg[hi] - zg[lo])
    N = (aN + rand() * (bN - aN))^(1 / (1 - beta))      # inverse CDF of N^-1.5
    b = 20 + 20 * rand()
    add_cloud(z, N, b, l0B, dlB, nB)
  }
  sumT = 0; cnt = 0
  for (i = 0; i <= nB; i++) {
    lam = l0B + i * dlB; F = quasar(lam)
    if (i % 4 == 0) printf "%.5f %.5f %.5f\n", lam * 1e9, F * exp(-tau[i]), F > (out "lya_forest.dat")
    if (lam > 102.572e-9 * (1 + zq) && lam < 0.99 * lam_a * (1 + zq)) { sumT += exp(-tau[i]); cnt++ }
  }
  close(out "lya_forest.dat")
  meanT = sumT / cnt

  # ---- Gunn-Peterson depth of a fully neutral IGM ----
  h = 0.674; Obh2 = 0.0224; Y = 0.245; Om = 0.315
  H0 = 100 * h * 1e3 / 3.0857e22
  rhoc = 3 * H0^2 / (8 * pi * 6.674e-11)
  Ob = Obh2 / h^2
  tau3 = tauGP(3.0); tau6 = tauGP(6.0)
  x1 = 1 / tau3

  # self-checks: tau_GP(z=6) ~ 4e5 for a neutral IGM; observed mean transmission at z~2.7 is ~0.7-0.8
  if (!(tau6 > 2e5 && tau6 < 7e5)) fail("tau6 = " tau6)
  if (!(meanT > 0.6 && meanT < 0.9)) fail("meanT = " meanT)

  n = 0
  name[++n] = "SixteenLyaZq";      val[n] = sprintf("%.0f", zq)
  name[++n] = "SixteenLyaQSO";     val[n] = sprintf("%.1f", lam_a * (1 + zq) * 1e9)
  name[++n] = "SixteenLyaA";       val[n] = sprintf("%.1f", lam_a * (1 + zA[1]) * 1e9)
  name[++n] = "SixteenLyaB";       val[n] = sprintf("%.1f", lam_a * (1 + zA[2]) * 1e9)
  name[++n] = "SixteenLyaC";       val[n] = sprintf("%.1f", lam_a * (1 + zA[3]) * 1e9)
  name[++n] = "SixteenLyaLines";   val[n] = sprintf("%d", nlines)
  name[++n] = "SixteenLyaMeanT";   val[n] = sprintf("%.2f", meanT)
  name[++n] = "SixteenTauGPthree"; val[n] = tex(sprintf("%.1e", tau3))
  name[++n] = "SixteenTauGPsix";   val[n] = tex(sprintf("%.1e", tau6))
  name[++n] = "SixteenXHIone";     val[n] = tex(sprintf("%.0e", x1))
  for (i = 1; i <= n; i++) {
    printf "\\newcommand{\\%s}{%s}\n", name[i], val[i] > (out "lya.tex")
    printf "%-20s %s\n", name[i], val[i]
  }
}
function tauGP(z,   nH, H) {
  nH = (1 - Y) * Ob * rhoc / m_H * (1 + z)^3
  H = H0 * sqrt(Om * (1 + z)^3 + 1 - Om)
  return sigma0 * lam_a * nH / H
}

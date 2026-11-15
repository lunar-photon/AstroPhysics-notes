# Radial-velocity curves of a star pulled by a planet, and the numbers of the method.
# (awk port of the planned cluster script; the cluster was unreachable on 2026-11-12.)
#
# Computes
#   - v_r/K = cos(omega + v) + e cos(omega) against phase (t - t_p)/P, with v from Kepler's
#     equation l = u - e sin u (Newton), for (e, omega) = (0, 0), (0.5, 90 deg), (0.5, 0 deg),
#   - K = (2 pi G / P)^(1/3) m_p sin(iota) / (M_* + m_p)^(2/3) / sqrt(1 - e^2) for Jupiter and the
#     Earth pulling the Sun (iota = 90 deg),
#   - m_p sin(iota) of 51 Peg b from P = 4.230785 d, K = 55.9 m/s, e = 0, M_* = 1.11 Msun
#     (mass function solved with m_p included, bisection in log m), and its semi-major axis,
#   - the fraction of isotropic orbits whose true mass exceeds twice the minimum, 1 - cos 30 deg.
# Writes results/ch6/rv_e0.dat, rv_e05_w90.dat, rv_e05_w0.dat (phase, v_r/K) and rv.tex (\Six...).
# Usage (from the repo root): mkdir -p results/ch6 && awk -f code/ch6/01_rv_curves.awk

function true_anomaly(ell, e,   u, k) {
  u = ell
  for (k = 0; k < 50; k++) u -= (u - e * sin(u) - ell) / (1 - e * cos(u))
  return 2 * atan2(sqrt(1 + e) * sin(u / 2), sqrt(1 - e) * cos(u / 2))
}
function curve(file, e, wdeg,   i, ph, v, w) {
  w = wdeg * pi / 180
  for (i = 0; i <= 800; i++) {
    ph = 2 * i / 800
    v = true_anomaly(2 * pi * ph, e)
    printf "%.5f %.5f\n", ph, cos(w + v) + e * cos(w) > file
  }
  close(file)
}
function K_of(mp, Ms, P, e) { return (2 * pi * G / P)^(1 / 3) * mp / (Ms + mp)^(2 / 3) / sqrt(1 - e * e) }
function tex(s,   m, x) {           # "4.2e-08" -> "4.2\times10^{-8}"
  if (s !~ /e/) return s
  split(s, m, "e"); x = m[2] + 0
  return m[1] "\\times10^{" x "}"
}
function fail(msg) { print "SELF-CHECK FAILED: " msg > "/dev/stderr"; bad = 1; exit 1 }
BEGIN {
  pi = 3.141592653589793
  G = 6.674e-11; Msun = 1.989e30; MJ = 1.898e27; ME = 5.972e24
  yr = 3.15576e7; day = 86400.0; AU = 1.496e11
  out = "results/ch6/"

  curve(out "rv_e0.dat", 0.0, 0.0)
  curve(out "rv_e05_w90.dat", 0.5, 90.0)
  curve(out "rv_e05_w0.dat", 0.5, 0.0)

  KJ = K_of(MJ, Msun, 11.862 * yr, 0.0489)
  KE = K_of(ME, Msun, 1.0 * yr, 0.0167)

  P51 = 4.230785 * day; K51 = 55.9; M51 = 1.11 * Msun
  f51 = P51 * K51^3 / (2 * pi * G)
  lo = log(1e20); hi = log(1e30)
  for (k = 0; k < 200; k++) {
    mid = (lo + hi) / 2; m = exp(mid)
    if (m^3 / (M51 + m)^2 - f51 > 0) hi = mid; else lo = mid
  }
  m51 = exp((lo + hi) / 2)
  a51 = (G * (M51 + m51) * P51^2 / (4 * pi^2))^(1 / 3)
  ptwice = 1 - cos(30 * pi / 180)

  # self-checks against well-known values: Jupiter 12.5 m/s, Earth 9 cm/s, 51 Peg b ~0.46 MJ
  if (!(KJ > 12.0 && KJ < 13.0)) fail("K_J = " KJ)
  if (!(KE > 0.085 && KE < 0.095)) fail("K_E = " KE)
  if (!(m51 / MJ > 0.40 && m51 / MJ < 0.52)) fail("m51/MJ = " m51 / MJ)
  # the e = 0 curve must be cos(2 pi phase)
  if ((getline line < (out "rv_e0.dat")) > 0) { split(line, c, " "); if (c[2] != "1.00000") fail("e=0 start " c[2]) }

  n = 0
  name[++n] = "SixKJup";     val[n] = sprintf("%.1f", KJ)
  name[++n] = "SixKEarth";   val[n] = sprintf("%.0f", 100 * KE)          # cm/s
  name[++n] = "SixJupShift"; val[n] = tex(sprintf("%.1e", KJ / 2.998e8))
  name[++n] = "SixPegMsini"; val[n] = sprintf("%.2f", m51 / MJ)          # Jupiter masses
  name[++n] = "SixPegA";     val[n] = sprintf("%.3f", a51 / AU)          # AU
  name[++n] = "SixPTwice";   val[n] = sprintf("%.0f", 100 * ptwice)      # percent
  for (i = 1; i <= n; i++) {
    printf "\\newcommand{\\%s}{%s}\n", name[i], val[i] > (out "rv.tex")
    printf "%-14s %s\n", name[i], val[i]
  }
}

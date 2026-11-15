# Numbers for the subsection "Finding Planets in Transit" (cc:sec:transit) and Problem 5.
# Usage: awk -f 01_transit_snr.awk
function ptail(k) { return exp(-k*k/2) / (k * sqrt(2*pi)) }   # cc:eq:tail_approx
BEGIN {
  pi = 3.141592653589793
  Re = 6.371e6; Rs = 6.957e8; AU = 1.496e11; yr = 365.25*86400
  depth = (Re/Rs)^2
  ttr = yr/pi * Rs/AU                       # ch6 central-crossing duration
  printf "R_E/R_S = %.5f  depth = %.3e = %.1f ppm  t_tr = %.2f h\n", Re/Rs, depth, depth*1e6, ttr/3600
  printf "Jupiter depth (0.10)^2 = %.3f\n", (7.149e7/Rs)^2
  # photon rate of a 12th-magnitude Sun-like star
  Fref = 2.518e-8; m = 12; D = 0.95; thr = 0.5; lam = 600e-9; h = 6.626e-34; c = 2.998e8
  F = Fref * 10^(-0.4*m); A = pi*(D/2)^2; Eph = h*c/lam
  rate = F*A/Eph*thr
  printf "F = %.3e W/m2  10^(-4.8) = %.4e  A = %.4f m2  E_ph = %.3e J  photons/s = %.3e  electrons/s = %.3e\n", F, 10^(-4.8), A, Eph, F*A/Eph, rate
  N65 = rate*6.5*3600; printf "N(6.5 h) = %.3e  1/sqrt = %.2f ppm\n", N65, 1e6/sqrt(N65)
  Nin = rate*ttr; s1 = depth*sqrt(Nin); printf "N_in(13 h) = %.3e  sqrt = %.3e  photon S/N per transit = %.2f\n", Nin, sqrt(Nin), s1
  # measured noise 30 ppm per 6.5 h, scaled to the transit duration as white noise
  sig = 30e-6 * sqrt(6.5*3600/ttr); s1r = depth/sig
  printf "noise over t_tr = %.1f ppm  S/N per transit = %.2f  star+instrument part = %.1f ppm\n", sig*1e6, s1r, sqrt(30^2 - (1e6/sqrt(N65))^2)
  k = 7.1; printf "transits for 7.1: Earth %.2f  2R_E: per transit %.2f, need %.3f  photon-only Earth %.3f\n", (k/s1r)^2, 4*s1r, (k/(4*s1r))^2, (k/s1)^2
  # number of independent (period, phase) trials per star, T (P_max - P_min)/t_tr^2
  T = 4*365.25; Pmax = T/3; Pmin = 0.5; tw = 0.5
  ntr = T*(Pmax-Pmin)/tw^2; ntot = 1.5e5*ntr
  printf "T = %.0f d  Pmax = %.0f d  trials per star = %.3e  total = %.3e  1/total = %.3e\n", T, Pmax, ntr, ntot, 1/ntot
  for (k = 6.5; k <= 7.31; k += 0.1) printf "k = %.1f  P_tail = %.3e  mean false alarms = %.3f\n", k, ptail(k), ntot*ptail(k)
  printf "exp(-7.1^2/2) = %.4e  P_tail(7.1) = %.3e\n", exp(-7.1^2/2), ptail(7.1)
  printf "95 Mpx: 42*2200*1024 = %.4e\n", 42*2200*1024
}

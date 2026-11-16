# Blackbody fit to the K1 star of fig_ch14_spectra (SDSS 2305-54414-0097).
# Reads results/ch14/spec_star.dat (lambda_obs nm, flux normalised to the peak), averages it in 10 nm
# bins over 450-900 nm (the blue below 450 nm is cut down by absorption lines, so it is left out),
# and fits a * B_lambda(T) by least squares: a analytically for each T, T on a 10 K grid.
# B_lambda(T) = 1 / (w^5 (exp(hc/(w k T)) - 1)), w in m, hc/k = 0.0143877 m K.
# Writes the macros to stdout:  awk -f code/ch14/06_star_blackbody.awk results/ch14/spec_star.dat > results/ch14/star_bb.tex
function B(l, T,   w) { w = l * 1e-9; return 1 / (w^5 * (exp(0.0143877 / (w * T)) - 1)) }
NR > 1 && $1 >= 450 && $1 <= 900 { k = int($1 / 10); s[k] += $2; n[k]++ }
END {
  for (k in s) { m++; L[m] = (k + 0.5) * 10; F[m] = s[k] / n[k] }
  best = 1e99
  for (T = 3500; T <= 7000; T += 10) {
    sfb = 0; sbb = 0
    for (i = 1; i <= m; i++) { b = B(L[i], T); sfb += F[i] * b; sbb += b * b }
    a = sfb / sbb; c = 0
    for (i = 1; i <= m; i++) { r = F[i] - a * B(L[i], T); c += r * r }
    if (c < best) { best = c; bT = T; bA = a }
  }
  rms = sqrt(best / m)
  # self-check: a cool star, a good fit
  if (bT < 4000 || bT > 6000 || rms > 0.06) { print "check failed: T=" bT " rms=" rms > "/dev/stderr"; exit 1 }
  print "% from code/ch14/06_star_blackbody.awk"
  printf "\\providecommand{\\FourteenStarT}{%d}\n", bT
  printf "\\providecommand{\\FourteenStarC}{%.4f}\n", bA * 1e30   # a / (1e-6)^5: the curve with lambda in micrometres
  printf "\\providecommand{\\FourteenStarRms}{%.0f}\n", 100 * rms
  printf "\\providecommand{\\FourteenStarPeak}{%.2f}\n", 2897.8 / bT   # Wien peak, micrometres
}

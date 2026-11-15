# Airy profile of a star and of a faint planet beside it, for fig_ch5_direct_imaging.
# J1(z) = (1/pi) int_0^pi cos(t - z sin t) dt, trapezoid rule with 2000 steps.
# Usage: awk -v check=1 -f 01_airy_planet.awk   (prints the checks)
#        awk -f 01_airy_planet.awk               (prints the table: x = theta/(lambda/D), star, planet)
function j1(z,   n, h, s, i, t) {
  n = 2000; h = 3.141592653589793 / n; s = 0
  for (i = 0; i <= n; i++) { t = i * h; s += (i == 0 || i == n ? 0.5 : 1) * cos(t - z * sin(t)) }
  return s * h / 3.141592653589793
}
function airy(b) { if (b < 1e-9) return 1; return (2 * j1(b) / b)^2 }
BEGIN {
  pi = 3.141592653589793; xp = 4.7; cp = 7.7e-4; floor = 1e-12
  if (check) {
    printf "J1(3.8317) = %.2e (zero)\nI(1.616) = %.4f (half)\nI(5.136) = %.4f (ring 0.0175)\n", j1(3.8317), airy(1.616), airy(5.136)
    exit
  }
  for (x = 0; x <= 10.0001; x += 0.01) {
    s = airy(pi * x); p = cp * airy(pi * (x > xp ? x - xp : xp - x))
    if (s < floor) s = floor; if (p < floor) p = floor
    printf "%.3f %.4e %.4e\n", x, s, p
  }
}

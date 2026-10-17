# Notation register (binding for every writer and agent)

Every agent reads this file before writing and before introducing any symbol. It is how agents agree on notation, so the notes read as one text.

Rules (template STYLE_GUIDE §5.17, plus the owner's "fewest symbols" rule of 2026-10-15):
1. **Fewest symbols.** A new letter is allowed only when the quantity is what the result is about, or the same expression recurs many times far apart. Otherwise write the expression out. Before adding a letter, ask whether the reader would lose anything if it were written out.
2. **Check here first, then grep the chapters.** The letter may already mean something else.
3. **One meaning per symbol within a chapter block, one symbol per quantity.** Resolve a clash by renaming or writing out, never by context.
4. **Define once, recall afterwards.** Later uses recall the definition with a `\eqref`/`\ref`, not a second definition.
5. **Log every change** (new symbol, rename, write-out) in the decision log below, with the date, in the same commit.

## Conventions
- SI units throughout, with astronomical units (M☉, R☉, L☉, AU, pc) for sizes. c, G, k_B and ħ are kept explicit (no c = 1).
- Vectors are `\vec{}`, with macros from `preamble.tex` (`\vecr`, `\vecL`, …). Unit vectors are hats.
- Transformations are written as matrix–vector equations (owner rule).
- Spherical symmetry, so profiles are functions of r. Lagrangian forms use the enclosed mass m as the coordinate.
- Time averages are `\avg{·}`.

## Symbols already in use (ch1–8). Do not reuse with another meaning in ch9–13.
| symbol | meaning | where | note for ch9–13 |
|---|---|---|---|
| μ | reduced mass | ch6 | ch9–13 use μ only for mean molecular weight (as ch8 does). The free-fall cross-check with the Kepler orbit uses a test particle, so no reduced mass appears. |
| μ | mean molecular weight | ch8 (`\mu m_{\rm H}`) | keep |
| Ω | longitude of ascending node | ch6 | **never** use for gravitational energy or rotation |
| ω | argument of periapsis, and angular frequency in the Jeans dispersion (ch8) | ch6, ch8 | ω stays an angular frequency in ch10 |
| ℓ | mean anomaly | ch6, ch8 free fall | **never** use for mean free path. Write 1/(κρ). |
| n | mean motion √(GM/a³) | ch6, ch8 | **not** the polytropic index (see the decision log) |
| n_d, n_{H₂} | number densities | ch8 | number density keeps the subscript form |
| a, e, λ | semi-major axis, eccentricity, semi-latus rectum | ch6 | λ_J stays the Jeans length (subscript makes it distinct) |
| τ, τ_λ | optical depth | ch4, ch8 | **reuse** τ for optical depth in ch11 |
| Φ | gravitational potential | ch8 | **reuse**. Also the metric potential in ch13, whose Newtonian limit is the same Φ |
| γ | systemic radial velocity | ch6 binaries | ch9–13 use γ for the adiabatic/polytropic exponent. No overlap within a block. |
| γ_e | electron Lorentz factor | ch8 | keep the subscript |
| κ | (used in ch6 for a frequency) | ch6 | ch11–12 use κ for opacity per unit mass. No overlap within a block. |
| ξ | auxiliary variable | ch6 | the free-fall substitution in ch10 uses ξ as a local integration variable only |
| K | kinetic energy (K_bulk, K_th) | ch8 | **K is kinetic energy only.** The polytropic constant gets another letter. |
| U | gravitational self-energy | ch8, lecture notes | keep (not Ω, not W) |
| I | second moment ∫r² dm | ch8 | in ch11 the specific intensity is I_ν (subscript ν always written) |
| M(r) vs m(r) | enclosed mass | ch8 uses both | unify to **m(r)** in ch9–13, with M the total mass |
| B_λ, B_ν | Planck function | ch4 | reuse |
| F | flux | ch4 | reuse |

## Planned symbols for ch9–13
| symbol | meaning | kind | units | first defined |
|---|---|---|---|---|
| ρ(r), P(r), T(r) | density, pressure, temperature profiles | fields | SI | ch10 (hydrostatic equilibrium) |
| m(r) | mass inside radius r | profile | kg | ch10 |
| M, R | total mass, radius | constants | kg, m | ch10 |
| T̄ | mass-averaged temperature | constant | K | ch10 (virial) |
| K, U, E | kinetic, gravitational, total energy | constants | J | ch8 → ch10 |
| γ | adiabatic exponent, P ∝ ρ^γ | constant | 1 | ch10 (virial, general γ) |
| C | heat capacity dE/dT̄ | constant | J/K | ch10 |
| c_s | sound speed | constant | m/s | ch8 |
| t_ff, t_KH, t_nuc | free-fall, Kelvin–Helmholtz, nuclear times | constants | s | ch10 |
| I_ν, j_ν, S_ν | specific intensity, emissivity, source function | fields | SI | ch11 |
| κ, κ_ν | opacity per unit mass (absorption coefficient written κ_νρ, no α_ν) | material | m²/kg | ch11 |
| L(r) | luminosity through radius r | profile | W | ch11/12 |
| T_eff | effective temperature | constant | K | ch4 → ch11 |
| ε | nuclear energy release per unit mass and time | material | W/kg | ch12 |
| X, Y, Z | mass fractions of H, He, metals | constants | 1 | ch12 |
| μ_e | mass per electron in units of m_H | constant | 1 | ch12 |

## Written out instead of named (deliberate)
- Mean free path, written 1/(κρ). (ℓ is taken.)
- Logarithmic gradients, written d ln T/d ln P. (No ∇, ∇_ad, ∇_rad, since ∇ is the gradient operator.)
- Compactness, written GM/(Rc²).
- Absorption coefficient, written κ_νρ. (No α_ν.)
- The board's χ in free fall, written √(8πGρ₀/3).
- Gas-to-total pressure ratio β, written P_gas/P if needed at all.

## Decision log (append; never edit old rows)
| date | where | symbol | old | new | files / to-dos |
|---|---|---|---|---|---|
| 2026-10-15 | plan | gravitational energy | Ω (plan draft) | U | Ω is the node longitude in ch6 |
| 2026-10-15 | plan | mean free path | ℓ (plan draft) | written out, 1/(κρ) | ℓ is the mean anomaly |
| 2026-10-15 | ch8 → ch9 | enclosed mass | M(r) and m(r) | m(r) | unify when ch8 §7–9 moves to ch9 |
| 2026-10-15 | ch11 | polytrope | index n, constant K | exponent γ (reused from the virial theorem), constant letter to choose when ch11 is written | n is the mean motion, K is kinetic energy. Write Lane–Emden with γ, and use n only as a label of solutions if needed. |
| 2026-10-15 | plan | chapter numbers | ch9 gas, ch10 radiation, ch11 structure, ch12 compact | ch9 Six Principles, ch10 gas, ch11 radiation, ch12 structure, ch13 compact | references above updated. P1–P6 are the principle labels (Conservation, Gravity of a sphere, Counting states, Balance of rates, Random walk, Compare two scales). Never reuse P1–P6 for anything else. Pressure stays P (no subscript clash, since principles are always written P1–P6). |
| 2026-10-16 | preamble | identity matrix | \\mathbb{1} (no glyph in amssymb) | \\Id = \\mathds{1} (dsfont) | ch9 Eq. momentum flux |
| 2026-10-16 | ch9, ch10 | L | box side L (ch9 P3), L→0 angular momentum (ch10) | box side b, quantum numbers q_x,q_y,q_z, angular momentum in words | L is the luminosity throughout ch10–13 |
| 2026-10-16 | ch12 | polytrope constant | (open) | \mathcal K in P = \mathcal K rho^gamma; Lane–Emden written with exponent 1/(gamma−1) (no n); r0 length unit, xi, theta; omega_1 written out as −xi^2 theta' at xi_1 | K stays kinetic energy, n stays number density |
| 2026-10-16 | ch12 | composition | — | X, Y, Z mass fractions; mu (ch10) and mu_e = 2/(1+X) | defined st:eq:mu |
| 2026-10-16 | ch12 | burning | — | epsilon = energy release per mass and time; E_G Gamow energy, E_0 Gamow peak, m_r reduced mass of the pair, alpha fine-structure constant (local) | alpha only in the Gamow paragraph |
| 2026-10-16 | ch12 | brown-dwarf estimate | — | \mathcal A, \mathcal B local coefficients | local to one paragraph |
| 2026-10-16 | ch10 | rotation | Omega_s (draft) | v_rot | Omega is the node longitude |
| 2026-10-16 | ch11 | Einstein coefficients | — | A_21, B_12, B_21 with level indices 1 (lower), 2 (upper) | B_nu (Planck) keeps its nu subscript |
| 2026-10-16 | ch1 rework | spin and periods | T_sidereal, T_solar, T_orb, Omega_prec, Omega_orb | omega_⊕ (spin rate against the equinox), T_sid, T_sol, T_yr, omega_prec | Omega reserved for the node longitude |
| 2026-10-16 | ch1 rework | anomalies | M, E (mean, eccentric) | ell, u (as ch6), v true anomaly; n = orbital mean motion (ch1–8 block only) | consistent with ch6 |
| 2026-10-16 | ch1 rework | longitudes, obliquity | — | lambda (terrestrial longitude), lambda_⊙ (Sun's ecliptic longitude), bar-lambda_⊙ (mean longitude), epsilon (obliquity, ch1–8 block; in ch12 epsilon is the burning rate) | different blocks |
| 2026-10-16 | ch1 rework | precession | m, n precession constants, tau torque | written out as omega_prec cos epsilon, omega_prec sin epsilon; torque written as dot-L; p-hat spin axis, k-hat ecliptic pole; A, C principal moments | tau is optical depth |
| 2026-10-16 | ch2 rework | frames | — | r-hat direction of a star, components with frame subscript (r-hat_eq, _mer, _hor, _ecl, _gal); R_z(theta), R_x(theta) passive rotations; M(phi_0) horizontal matrix (columns n-hat, e-hat, u-hat), det = −1 | — |
| 2026-10-16 | ch2 rework | zenith, refraction, scale height | z-hat (zenith), R (refraction), H (scale height) | u-hat zenith vector, Delta h refraction lift, H_air air scale height | clashes with zenith angle z, matrix R, hour angle H |
| 2026-10-16 | ch2 rework | Galactic constants, parallactic angle | theta_0 (mislabelled) | l_CP, alpha_GP, delta_GP; q parallactic angle | — |
| 2026-10-16 | ch2 rework | kept standard letters (ch1–8 block) | — | kappa aberration constant, X airmass, epsilon obliquity, lambda ecliptic longitude | in ch9–13 kappa = opacity, X = H fraction, epsilon = burning rate; different blocks |
| 2026-10-16 | ch3 rework | astrometry | varpi (parallax in problem) | p parallax, sigma_p its error; mu_alpha*, mu_delta, mu proper motion (OPEN: clashes with ch6 reduced mass, ch8–13 mean molecular weight, ch4 distance modulus); Q(alpha,delta) local-axes matrix (rows r-hat, alpha-hat, delta-hat); T Galactic matrix; v_r, v_alpha, v_delta, v_t; z fractional Doppler shift; Lorentz factor written out | owner to decide mu |
| 2026-10-16 | ch3 rework | (U,V,W) | — | kept as standard Galactic velocity components (OPEN: clash with U gravitational energy ch10, V potential ch6) | owner to decide |
| 2026-10-16 | ch4 rework | photometry | mu (distance modulus), R_*, Theta, varpi, E_{B−V}, F_0, R_V | m − M distance modulus, R radius, theta angular diameter, p parallax, E(B−V), F_ref zero-point flux (subscript 0 = no dust), R_V written as A_V/E(B−V); x = h nu/k_B T; psi angle from the normal in the hemisphere integral | M absolute magnitude, m apparent magnitude, a grain radius kept (ch1–8 block; clash with mass, m(r), semi-major axis noted) |
| 2026-10-16 | ch7 rework | noise | mu (Poisson mean), lambda (rate), E[·], Phi(k) normal CDF, theta_see | n-bar Poisson mean count, rates written R_src, n_pix R_sky, n_pix R_dark (no bare R), <·> expectation, delta X_i deviation, P(n) Poisson probability, P_tail(k), P_any(k), k threshold in sigma, n_trial, theta_seeing; eta quantum efficiency (ch1–8 block) | Phi is the gravitational potential |
| 2026-10-16 | ch5 rework | resolution | lambda (longitude), beta/gamma/v phases, theta_res/diff/Rayleigh/theta_1, C chord, f frequency, epsilon obscuration, p pixel scale | Lambda station longitude; pupil (xi, eta), polar (r, psi), azimuth chi, k = 2 pi/lambda; beta_a, beta_d, beta_D phases; u spatial frequency; theta_R Rayleigh limit; theta_see; theta_M, beta_M Moffat; y_pix; theta_pix; plate scale written d theta/dy; B baseline; nu frequency, nu_p plasma frequency, alpha grazing angle; b/D obscuration; d_2, F_eff | block-level clashes noted (eta, alpha, beta_M, u, E field) |
| 2026-10-16 | ch8 rework | lines and ISM | Delta tau (collision time) | Gamma decay/damping rate; t_col with 1/t_col = n sigma_col v-bar; phi(nu), phi_L, phi_D, phi_V line profiles; Delta nu_D Doppler width (standard deviation); sigma_v, sigma_turb; v_r line-of-sight velocity; E_21, g_1, g_2, n_1, n_2, A_21 as ch11; n_c coolant density; Sigma_d dust mass column, rho_grain, epsilon_r; psi scattering angle; theta shell angle; E-dot_heat; N_H; T_B; polarizability, Mie efficiency, dispersion measure written out | local clashes noted (mu_e etc. magnetic moments, alpha fine-structure, k wavenumber, n index) |
| 2026-10-16 | ch6 rework | two-body | nu/f true anomaly, theta polar angle, i inclination, T_0/t_p, Upsilon-hat, epsilon_1/2, Phi mean longitude, epsilon order parameter, alpha inverse-cube strength, A orbit constant | v true anomaly, phi polar angle, iota inclination, t_0 periapsis time, gamma-hat vernal equinox; e-vector = A/(GM mu^2) with e_x, e_y; bar-phi = omega + ell mean longitude, delta phi; O(F) for smallness; chi inverse-cube strength; C orbit-equation constant; c_s Fourier coefficients; psi flight-path angle; v_asy; V_CM; locals h = L/mu, script-E = E/mu, F_T thrust, w-vector | OPEN: subscripted speeds v_infty, v_apo, v_r next to true anomaly v |
| 2026-10-16 | preamble | \hatn | \hat\leo (rendered a Leo glyph) | \hat n | bug fix |
| 2026-10-16 | ch14–16 plan | cosmology and fast particles | — | scale factor a(t); radiation constant written a_rad in ch14–16; H(t), H_0; Omega_m, Omega_r, Omega_Lambda (subscripted, distinct from the node longitude of ch6); Lorentz factor gamma_L (gamma is the adiabatic exponent in ch9–13); beta = v/c; density contrast delta; w = P/(rho c^2) | new block ch14–16 |
| 2026-10-16 | ch14 | galaxies | v_c (plan) | v_circ circular speed (as ch12); R_0, v_0 Sun's Galactocentric distance and speed; omega(r) = v_circ/r; s-hat line of sight, J local 2×2 matrix; Sigma disk surface density, sigma_z vertical spread, h_z scale height (not H, not h); sigma line-of-sight spread (sigma_SB unchanged); b impact parameter; m_star one member's mass, N members, t_cross, t_relax, ln N written out; rho_c, r_c halo core (local); r_perp, theta projection (local); D_L, D_S, D_LS, theta_E lensing; iota inclination; W 21 cm width (local) | — |
| 2026-10-16 | ch15 | fast particles | — | Lambda(beta) Lorentz boost matrix, always with its argument (ch16 uses Lambda only as a subscript, Omega_Lambda, rho_Lambda, so no bare clash); gamma_L, beta; script-P one-particle power (P pressure); t_e; Theta angle from acceleration; lambda_D Debye length; Z_i ion charge (Z metal fraction); n_i; b impact parameter; g-bar Gaunt factor; nu_g, nu_c; u_B, u_rad (U gravitational energy); n(gamma_L) with index p; alpha radio index (local); lambda_C; psi scattering angle; y Compton parameter; x = h nu/k_B T; f occupation; N(x); eta accretion efficiency (ch7 eta other block); R_in, T_*, script-T torque, beta_app; acceleration written v-dot (a is the scale factor) | ch8 gamma_e could become gamma_L in a later pass |
| 2026-10-16 | ch12 HR figure | HR diagram | — | g surface gravity of a white dwarf, R = sqrt(GM/g) (same g as the gravitational acceleration of ch10); macros \TwelveHRN, \TwelveHRMaxPc, \TwelveHRNwd | data figure from code/ch12/02_hr_diagram.py |
| 2026-10-17 | ch6 | body paths from COM and relative orbit | q = m_2/M (pasted) | written m_2/M and 1 − m_2/M, no new symbol (q is the parallactic angle in ch2 and q-hat the periapsis frame in ch6); tb:eq:body_paths | — |

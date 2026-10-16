# Plan: six principles, and everything about stars derived from them

## The idea

Astrophysics looks like a long list of formulas. It is not. With six general principles, plus ordinary classical and quantum physics, every result in these chapters can be derived. The reader should not have to remember the results. They should remember the six principles and be able to rebuild any result from them.

So the notes show the same principles at work again and again. Every derivation starts by naming which principles it combines. By the end the reader has seen each principle produce ten different things, and that repetition is what removes the need to memorise.

The reader knows mechanics, electromagnetism, thermodynamics, statistical mechanics, quantum mechanics and GR. GR is not recapped, and TOV and the mass limits are quoted from the owner's GR notes.

## The six principles

Each one is stated once, in its general form and with the fewest symbols, in the new ch9. After that it is only *used*.

| | Principle | General statement | Already used in |
|---|---|---|---|
| **P1** | **Conservation** | Mass, momentum, energy and angular momentum of a parcel change only through what crosses its boundary or acts on it. | ch6 (E and L give the whole Kepler problem), ch8 (Euler equation) |
| **P2** | **Gravity of a sphere** | Outside a spherical shell, its pull is that of a point at the centre. Inside, the shell pulls nothing. So a mass element at r feels only m(r), at g = Gm(r)/r². | ch6, ch8 (free fall) |
| **P3** | **Counting states** | In equilibrium, each quantum state of energy ε is occupied with the Boltzmann, Bose or Fermi weight. Phase space comes in cells of size h³, and fermions take at most one per state. Pressure, energy density and populations all follow by counting. | ch4 (Planck), ch8 (Doppler width, Maxwell) |
| **P4** | **Balance of rates** | In a steady state every gain is matched by a loss. In full equilibrium every process is matched by its own reverse (detailed balance). | ch8 (heating = cooling) |
| **P5** | **Random walk** | N steps of length ℓ in random directions travel a distance √N ℓ. So anything that scatters often moves by diffusion, and its flux is proportional to minus the gradient. | (new) |
| **P6** | **Compare two scales** | Which physics matters is decided by the ratio of two times or two lengths. A ratio far from 1 picks the regime, and a ratio near 1 marks a transition or an instability. | ch5 (resolution λ/D), ch8 (scattering regimes, a vs λ) |

The quantum mechanics and relativity the reader already knows (the uncertainty principle, tunnelling, E² = p²c² + m²c⁴, the metric) are the tools the principles act through, not extra principles.

## The ledger (which principles make which result, a planning tool, not printed)

This is the backbone of the plan. Writers use it to know which principles each derivation must name. It is not printed in the notes (owner, 2026-10-15, no end-of-chapter summaries).

| Result | Principles | Section |
|---|---|---|
| Hydrostatic equilibrium | P1 (momentum) + P2 | 10.2 |
| Virial theorem, and "gravity sets the temperature" | P1 + P2, integrated over the star, + P3 (K = (3/2)Nk_BT̄) | 10.3 |
| Binding and γ, E ∝ (3γ−4) | virial + P3 | 10.3 |
| Negative heat capacity, and why it is no paradox | virial + P3 (ensembles) | 10.4 |
| Jeans criterion | P6 (sound-crossing time vs free-fall time), checked by P1 + P2 linearised | 10.5 |
| Free fall | P1 (energy) + P2 | 10.6 |
| The three clocks and quasi-static evolution | P6 | 10.6 |
| Disks from collapse | P1 (angular momentum) | 10.7 |
| Transfer equation | P1 (photon energy along a ray) + P4 (gain − loss) | 11.2 |
| Kirchhoff's law, LTE | P4 (detailed balance) + P3 (Planck) | 11.3 |
| Radiative diffusion, photon escape time | P5 | 11.4 |
| Optically thick vs thin | P6 (mean free path vs size) | 11.2 |
| Eddington luminosity | P1 (momentum of light) + P2 | 11.5 |
| Einstein coefficients, line formation | P4 + P3 | 11.6 |
| The four structure equations | P1 (mass, momentum, energy) + P2 + P5 (transport) | 12.2 |
| Convection criterion | P1 (buoyancy of a blob) + P3 (adiabat) | 12.2 |
| Equation of state: ideal, radiation, degenerate | P3 | 12.3 |
| When degeneracy matters | P6 (particle spacing vs de Broglie wavelength) | 12.3 |
| Opacity laws | P3 + P5 | 12.3 |
| Gamow peak, T-sensitivity of burning | P3 (Maxwell tail) × tunnelling | 12.3 |
| Lane–Emden, polytropes, isothermal sphere | P1 + P2 closed by P3 | 12.5 |
| Mass–luminosity, lifetimes | P5 + virial, by scaling | 12.6 |
| Lowest stellar mass (brown dwarfs) | virial + P3 (degeneracy) | 12.6 |
| Chandrasekhar mass | virial + P3 (relativistic degeneracy, γ = 4/3) | 13.2 |
| When GR matters | P6 (GM/Rc²) | 13.1 |
| Tolman–Ehrenfest, T e^{Φ/c²} = const | P3 + GR | 13.3 |

**Later chapters show the same six at work outside stars.** These are not written in this block, but the plan keeps them in view so the repetition carries on.
- Galaxies. Cluster masses and dark matter (virial). Rotation curves (P2). Isothermal halos (P1 + P2 + P3).
- The early universe. The Friedmann equation from a Newtonian shell (P1 + P2). The CMB spectrum (P3). Recombination (P3 + P4, Saha). Freeze-out (P6, reaction rate vs expansion rate). Big Bang nucleosynthesis (P3 × tunnelling, as in stars).

## Derivation homes (every derivation is done once, here; elsewhere it is cited)

Writers check this table before writing (STYLE_GUIDE rule 23a). A derivation not listed gets a row before it is written.

| Derivation | Home | Cited (not re-derived) in |
|---|---|---|
| Kepler orbit, E = −GMμ/2a, third law, eccentricity vector, osculating elements, planar Gauss equations, orbit averaging, Bessel series of Kepler's equation, Rømer delay | ch6 | ch10.6 (free fall as the L → 0 orbit) |
| Planck function, Stefan–Boltzmann, T_eff via L = 4πR²σT_eff⁴ | Planck derived in ch9 (P3). T_eff defined in ch4. | ch4 (rework points to ch9 for Planck's derivation), ch11.3, ch11.7 |
| Optical depth τ, extinction | ch4/ch8 | ch11.2 |
| Continuity and Euler equations | ch9 (P1) | ch10.2, ch10.5, ch12.2 |
| Shell theorem, m(r), dm/dr = 4πr²ρ, U = −∫Gm dm/r | ch9 (P2) | ch10, ch12.2 |
| Pressure integral, ideal gas, K = (3/2)Nk_BT, radiation u = aT⁴, P = aT⁴/3 | ch9 (P3) | ch10.3, ch11, ch12.3 |
| Random walk √N, flux ∝ −gradient | ch9 (P5) | ch11.4 |
| Hydrostatic equilibrium | ch10.2 | ch10.3, ch12.2, ch13 |
| Virial theorem (both routes), U of a uniform sphere, μ defined, E ∝ (3γ−4) | ch10.3 | ch10.4–10.6, ch12.6, ch13.2 |
| Negative heat capacity, ensembles | ch10.4 | ch12.3 (thermostat), ch12.6 (red giants) |
| Jeans criterion (energy and dispersion routes) | ch10.5 | — |
| Free fall, t_ff, t_KH, t_nuc | ch10.6 | ch12.4 |
| Three kinds of equilibrium, LTE | ch10.7 | ch11.3 |
| Transfer equation, source function | ch11.2 | ch11.3–11.7 |
| Kirchhoff, S_ν = B_ν | ch11.3 | ch11.6, ch11.7 |
| Radiative diffusion flux, photon escape time | ch11.4 | ch12.2 (transport) |
| Eddington luminosity | ch11.5 | ch12.5 (upper mass) |
| Einstein coefficients | ch11.6 | — |
| Grey atmosphere T(τ) | ch11.7 | — |
| Energy equation dL/dm, convection criterion | ch12.2 | — |
| μ for X, Y, Z, degeneracy pressure, when degeneracy matters, opacity laws, Gamow peak | ch12.3 | ch12.6, ch13.2 |
| Lane–Emden, polytropes, isothermal sphere, Eddington standard model | ch12.5 | ch13.2 |
| Homology, mass–luminosity, lowest stellar mass | ch12.6 | — |
| Chandrasekhar mass | ch13.2 | — |
| TOV, mass limits | owner's GR notes (quoted) | ch13.3–13.4 |
| Rotation matrices R_z, R_x, frame matrices, horizontal/ecliptic/Galactic transforms, angular distance, refraction, aberration, airmass, parallactic angle | ch2 | ch3 (equatorial → Galactic velocity), ch6 (orbital frame) |
| Driven-oscillator cross-section and its Rayleigh/Thomson/resonance limits, sigma_T, small-grain absorption, line profiles (natural, pressure, Doppler, Voigt), 21 cm energy and A_21 (is:eq:A21), two-level balance with critical density, dispersion delay, expanding-shell line profile, gas temperature from heating = cooling | ch8 | ch11 (A_21), ch7 (dispersion noise) |
| Plasma frequency and refractive index of free electrons, Fraunhofer integral, slit, grating, resolving power, Airy pattern and 1.22, encircled energy, Rayleigh and Sparrow limits, D/lambda image limit, Nyquist sampling, correlator output and lambda/B, Fried r0 scaling, Moffat FWHM | ch5 | ch7 (seeing), ch2 (central angle is cited by ch5) |
| Poisson distribution (binomial limit), its mean and variance, variance addition for independent quantities (cc:eq:var_add), Gaussian limit via Stirling, CCD S/N equation and regimes, magnitude error 1.0857/SNR, Gaussian tail, look-elsewhere | ch7 | ch9 P5 (sqrt N step cites cc:eq:var_add) |
| B_nu → B_lambda, Wien's law, hemisphere factor pi (ph:eq:flux_pi_B), pi^4/15 and zeta(4), colour–temperature relation, tau, A = 1.086 tau (ph:eq:extinction_tau), colour excess, A_V/E(B−V), angular diameter from flux | ch4 | ch8 (extinction, must cite ch4), ch11 (flux pi B, extinction) |
| Parallax and parsec, parallax ellipse, parallax bias (inversion, Lutz–Kelker), local sky axes Q, proper motion and 4.74, classical and exact Doppler, Earth-motion correction, space velocity, (U,V,W), LSR | ch3 | ch2 (ellipse sentence, local axes), ch8 (Doppler) |
| Sun's α, δ by rotation (ti:eq:sun_vector), equation of centre v − ℓ ≈ 2e sin ℓ (ti:eq:equation_of_centre, cited by ch6), equation of time, precession torque and rate, precession formulas for α and δ, TDB − TT | ch1 | ch2 (ecliptic rotation is the general case, cite ch1), ch2 noon zenith angle (cite ch1 Problem 1b) |

## How it is presented

All presentation, writing, figure and computing rules are in `STYLE_GUIDE.md` (ch6 is the model). This plan covers content only.

## Budget and selection

The notes aim at roughly 400–500 pages as a guide, not a cap. They are 158 pages now. Hard chapters get the pages they need. A topic goes in only if it is derived from the six principles and is used in more than one place, or is needed for such a derivation. Catalogue facts, detailed nuclear networks, the full mixing-length theory, stage-by-stage evolution and code internals get one sentence or nothing.

## Source material and what happens to it

- **ch8 §1–6 (ISM).** Stays. Light edits only. Where ch8 already uses a principle (heating = cooling is P4, line widths are P3, scattering regimes are P6), the text names it.
- **ch8 §7–9 (virial, Jeans, free fall).** Moves into ch10 and is rewritten. The virial theorem is now *read*, negative heat capacity is added, and the meta sentences go.
- **`Sources/stellar_collapse_notes_final.pdf`.** Dissolved into ch10 at the places where each point belongs.
- **Lecture 30/9 (photos).** The virial theorem with "giving out heat, the temperature rises" (ch10.3–10.4). The direct free-fall integration with R = R₀cos²ξ (ch10.6). "Gravity, pressure, rotation" (ch10.1).
- **Syllabus PHY 4206.** Covered by ch10–13, except galaxies and the early universe (later).

## Chapter layout

| Ch | Title | Pages (estimate) |
|---|---|---|
| 8 | The Interstellar Medium (as now, minus §7–9) | ~12 |
| 9 | Six Principles | ~10 |
| 10 | Self-Gravitating Gas | ~14 |
| 11 | Radiation in Matter | ~10 |
| 12 | The Equations of a Star | ~16 |
| 13 | Degenerate and Compact Stars | ~7 |

## Ch9 — Six principles

The thread. Each principle opens with an everyday case where it is obvious. Then it gets its general statement with the fewest symbols, its smallest derivation from classical or quantum physics, and a short list of where it has already appeared in ch1–8 and where it will return. No astrophysics is derived here beyond one-line examples. The point is to give the reader six things to hold.

- **P1 Conservation.** A parcel with fluxes through its surface gives continuity and the Euler equation in one pass, the same bookkeeping ch6 did for a single particle.
- **P2 Gravity of a sphere.** Gauss's law for gravity gives the shell theorem in two lines. U = −∫Gm(r)dm/r follows.
- **P3 Counting states.** One cell of phase space is h³. Fill states with the right weight and integrate. Pressure as momentum flux P = (1/3)∫ n(p) p v d³p is derived here, once. Worked here, because ch10–11 need them first: the ideal gas (P = nk_BT, K = (3/2)Nk_BT) and photons (Planck's B_ν, u = aT⁴, P = aT⁴/3). The degenerate case is *not* done here. Its home is ch12.3, where it is first needed. This is the most reused principle in the notes.
- **P4 Balance of rates.** Steady state versus detailed balance, shown on a non-radiative example (the heating = cooling balance of ch8, cited, and forward/backward rates of a reversible process). Einstein coefficients are *not* done here. Their home is ch11.6.
- **P5 Random walk.** √N from adding random vectors (the dot products of independent steps average to zero). Flux ∝ −gradient follows.
- **P6 Compare two scales.** Ratios already met (λ/D in ch5, a/λ in ch8) and those coming (t_sound/t_ff, mean free path/size, spacing/de Broglie wavelength, GM/Rc²).

Figure. One panel per principle, a single schematic each.

## Ch10 — Self-gravitating gas

The thread. Gravity pulls in, pressure pushes out, rotation resists sideways (the board). Which wins decides whether a cloud collapses. The way gravity stores energy decides what happens next.

- **10.1 Opening.** A cold cloud from ch8. Why does it become a star, and why does it get hotter as it loses energy? Pressure as a sum P = P_gas + P_rad + P_deg + …, each term a different case of P3 (from the PDF).
- **10.2 Hydrostatic equilibrium (P1 + P2).** The Euler equation of ch9 (P1) with v = 0 and the shell-theorem gravity of ch9 (P2), cited, not re-derived. The force on a slab appears only as the opening picture. Planets obey it too. Compression moves (P,T) across phase boundaries and gives layered interiors (one paragraph, from the PDF). Where else: atmospheric scale height, disk thickness, cluster gas.
- **10.3 The virial theorem (P1 + P2 integrated, then P3).** Route A. Hydrostatic equilibrium × 4πr³, integrated, gives 3∫P dV + U = 0. Route B. ½Ï = 2K + U (from ch8, shortened), which also covers what happens out of equilibrium. **Reading it.** ⟨K⟩ is set by the depth of the well. With P3, ⟨K⟩ = (3/2)Nk_BT̄, so k_BT̄ = GMμm_H/5R. Gravity is a thermometer. The Sun comes out at a few million kelvin from M and R alone. **General γ.** E = (3γ−4)/(3(γ−1)) U, so the star is barely bound as γ → 4/3. Where else: Zwicky's clusters and dark matter, galaxy velocity dispersions.
- **10.4 Negative heat capacity (virial + P3).** C = −(3/2)Nk_B, so losing energy heats the star. It is no paradox. C_V = ⟨(ΔE)²⟩/k_BT² ≥ 0 holds in the canonical ensemble, and an isolated star is microcanonical. For long-range gravity the ensembles need not agree. What it buys: the burning thermostat, cores that heat until the next fuel ignites, and instability against a heat bath. Where else: globular cluster core collapse, black hole thermodynamics.
- **10.5 Jeans criterion (P6, checked by P1 + P2).** The energy argument and the dispersion relation, both read as λ_J ≈ c_s t_ff. One line on the Jeans swindle. Fragmentation, and why stars form in groups (from the PDF). Where else: structure formation in cosmology.
- **10.6 Free fall (P1 + P2) and three clocks (P6).** Direct integration as on the board, cross-checked as the L → 0 Kepler orbit of ch6. t_ff, t_KH = |U|/L and t_nuc for the Sun. Their ordering is why a star is a sequence of hydrostatic models, which is the precise form of the PDF's "hopping between equilibria".
- **10.7 Rotation and the end of collapse (P1).** Conserved angular momentum makes the centrifugal/gravity ratio grow as 1/R, so collapse makes a disk. Opacity limit, the first core, and dissociation acting as γ < 4/3 (back to 10.3). Three kinds of equilibrium, from the PDF: hydrostatic, global thermodynamic (which a star is not) and local thermodynamic (the assumption behind ch11–12).

Figures. E, K, U versus R. T̄(E) with negative slope. Free-fall R(t). Timescale ladder. ω²(k).

## Ch11 — Radiation in matter

The thread. One equation describes light passing through any medium, and its two limits cover most of what astronomers measure.

- **11.1 Specific intensity (P1).** I_ν is constant along a ray in empty space, so surface brightness does not depend on distance (link to ch4).
- **11.2 The transfer equation (P1 + P4).** dI_ν/ds = −κ_νρ I_ν + j_ν (absorption written κ_νρ, no new letter). Optical depth τ (same τ as ch4/ch8) and the source function S_ν = j_ν/(κ_νρ). Formal solution. Thin gives emission lines and thick gives I_ν → S_ν (P6).
- **11.3 Kirchhoff and LTE (P4 + P3).** In equilibrium S_ν = B_ν(T). LTE makes this hold point by point. Absorption lines appear when T falls outward.
- **11.4 Diffusion (P5).** For τ ≫ 1, F = −(c/3κρ) d(aT⁴)/dr, read as a random walk with step 1/(κρ) ≈ 1 cm in the Sun. Photon escape time. This becomes the transport equation of ch12.
- **11.5 Eddington luminosity (P1 + P2).** Radiation force = gravity, so L_Edd = 4πGMc/κ. Where else: upper stellar masses, quasar accretion.
- **11.6 Lines (P4 + P3).** Einstein coefficients from detailed balance. LTE and when it fails. Links to ch8 broadening and the 21 cm line.
- **11.7 T_eff and the grey atmosphere (P5 + P4).** T⁴ = ¾T_eff⁴(τ + ⅔). The photosphere sits at τ ≈ ⅔.

Radiative processes (bremsstrahlung, synchrotron, Compton) go to the galaxies chapter, where they are used.

Figures. A ray through a slab. Emergent intensity versus τ. Grey atmosphere T(τ).

## Ch12 — The equations of a star

The thread. Four equations, each one a principle. Three material functions, each one P3 or P5. Count four unknowns, four equations and four boundary conditions.

- **12.1 The unknowns.** r, P, T, L as functions of m (m follows the gas).
- **12.2 The four equations.** Mass (P1). Momentum (P1 + P2, from ch10). Energy (P1), dL/dm = ε − T ds/dt, where the last term is Kelvin–Helmholtz contraction in local form. Transport, radiative (P5, from 11.4) or convective (P1 buoyancy + P3 adiabat, the Schwarzschild criterion written with d ln T/d ln P). Mixing-length theory gets one sentence.
- **12.3 Material functions.**
  - **EOS (P3).** The ideal gas and radiation pressure are cited from ch9. New here: μ for ionised X, Y, Z (μ itself was defined at its first use in ch10.3), and the degenerate case, which is the pressure integral of ch9 with n(p) a filled Fermi sphere (P ∝ ρ^{5/3} and ρ^{4/3}). When degeneracy matters (P6). Figure, the ρ–T plane with the regimes, the Sun's track and a white dwarf.
  - **Opacity (P3 + P5).** Electron scattering and Kramers' law.
  - **Energy generation (P3 × tunnelling).** The Gamow peak. pp ∝ T⁴, CNO ∝ T^{16–20}. Steep T-dependence plus negative C makes the thermostat sharp.
- **12.4 Boundary conditions and how stars are computed.** A two-point boundary value problem, solved by shooting or relaxation (a paragraph each). Evolution is a sequence of hydrostatic models (the clocks of 10.6).
- **12.5 Polytropes and the isothermal sphere (P1 + P2 closed by P3).** Lane–Emden for P ∝ ρ^γ (the same γ as the virial theorem, so E ∝ (3γ−4) applies directly). Exact solutions and the numerical ones. γ → 1 gives the isothermal sphere, ρ ∝ r⁻² and a flat rotation curve, the bridge to galaxies. Eddington's standard model gives the upper stellar mass.
- **12.6 Scaling and the HR diagram.** Mass–luminosity and lifetimes by scaling. The lowest stellar mass from virial + degeneracy. The HR diagram with constant-R lines. Red giants from negative C.

Figures. Solar profiles (computed). The ρ–T plane. Gamow peak. Lane–Emden solutions. HR diagram.

## Ch13 — Degenerate and compact stars

The thread. "Relativistic" means two separate things. Relativistic particles (P3 with E = pc) give γ = 4/3 and the Chandrasekhar mass in Newtonian gravity. Relativistic gravity changes the structure equations only when GM/Rc² is not small (P6).

- **13.1 Compactness (P6).** One table, Sun, white dwarf, neutron star.
- **13.2 White dwarfs (virial + P3).** R ∝ M^{−1/3}, then M_Ch from γ = 4/3. This is 10.3 again.
- **13.3 The relativistic structure set, stated.** The Newtonian equations of 12.2 side by side with their GR forms (TOV quoted). Tolman–Ehrenfest corrects the "uniform T" of 10.7.
- **13.4 Computing a neutron star.** The recipe. Maximum mass quoted, with links to the GR notes and the ch6 binary pulsars.
- **13.5 Black holes.** A few lines.

Figures. White dwarf and neutron star M–R curves (computed).

## Scripts

`code/ch12/lane_emden.py`, `code/ch12/sun_model.py`, `code/ch13/wd_mass_radius.py`, `code/ch13/tov.py` (rules in `STYLE_GUIDE.md` §5).

## Edits to existing material

- ch8. Move §7–9 into ch10. End at heating and cooling. Remove the meta sentences.
- ch4 and ch6 (light touch, later). One sentence each where P3 (Planck) and P1 + P2 (Kepler) already work, so the earlier chapters join the same thread.
- Preface. Introduce the six principles in one paragraph and update the chapter list.
- README. Add the new chapters.
- Preamble. Add `\eqby`, `\relby` and the `explain` list (from the template `notes.sty`), a `workdef` box and an `\unpack{}` macro (green bracket, used only inside working-definition boxes).

## Order of work

1. The ch8 split, with the notation unified per `NOTATION.md`.
2. Ch9, the six principles. Everything else leans on it, so it is written first and reviewed by the owner before the rest.
3. Ch10, then ch11.
4. Scripts and figures for ch12–13, on the cluster.
5. Ch12, then ch13.
6. Preface, README, full build, read-through for flow.
7. Rework ch1–8 to the same rules (fill gaps, full section openings, principles threaded through, meta sentences out, chapter numbers as \ref), one chapter at a time.

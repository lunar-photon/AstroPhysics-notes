# Plan: galaxies, fast particles and the expanding universe (ch14–16)

The last part of the syllabus (PHY 4206): "shape, size and contents of our galaxy, basics of stellar dynamics, normal and active galaxies, high energy and plasma processes, clusters of galaxies, expansion of the universe, microwave background, early universe". The same six principles carry it. Most results here are principles already met, applied to a much larger system. All rules are in `STYLE_GUIDE.md`, `STYLE_CH6.md` and `NOTATION.md`. The derivation-homes table below extends the one in `PLAN_stellar_physics.md`.

Target length about 65 pages (a guide). General ideas only. Catalogue facts get a sentence.

## How the six principles return

| Result | Principles | Section |
|---|---|---|
| Flat rotation curves need unseen mass | P2 (mass inside r) + P1 (circular orbit) | 14.2 |
| Relaxation time of a star system | P5 (random walk of velocity kicks) + P6 (relaxation time vs age) | 14.3 |
| Galaxies are collisionless, globular clusters are not | P6 | 14.3 |
| Masses of galaxies and clusters | virial (ch10) | 14.4 |
| Tully–Fisher L ∝ v⁴ | virial + P6 scaling | 14.5 |
| Larmor power, then bremsstrahlung | P3 (Maxwell electrons) + P6 (impact parameters) | 15.2 |
| Synchrotron frequency and power-law spectra | P1 (relativistic motion in B) + P3 (counting electrons) | 15.3 |
| Inverse Compton boost by γ² | Lorentz transformations as matrices | 15.4 |
| Accretion luminosity and efficiency | P1 (energy) + P2 + compactness (ch13) | 15.5 |
| Thin-disk temperature T ∝ r^{−3/4} | P1 + P4 (local heating = cooling) + Stefan–Boltzmann | 15.5 |
| Superluminal motion | P6 (light-travel times) | 15.5 |
| Friedmann equation | P1 (energy of a shell) + P2 | 16.2 |
| ρ ∝ a^{−3}, a^{−4}, const | P1 (first law for an expanding volume) | 16.2 |
| CMB stays a blackbody, T ∝ 1/a | P3 | 16.3 |
| Recombination at 3000 K, not 160 000 K | P3 + P4 (Saha) + P6 (photons per baryon) | 16.3 |
| Freeze-out, Γ ≈ H | P4 + P6 | 16.4 |
| Helium fraction Y ≈ 0.25 | P3 + P4 + P6 | 16.4 |
| Growth of structure, δ ∝ a | P1 + P2 (Jeans with expansion, ch10) | 16.5 |

## Derivation homes (extends the table in PLAN_stellar_physics.md)

| Derivation | Home | Cited in |
|---|---|---|
| Circular speed v_circ² = Gm(r)/r, rotation curves, flat-curve density, cored halo curve (ga:eq:halo_v), mass-to-light; gravity of a flat layer 2πGΣ, disk scale height (ga:eq:disk_height); line-of-sight velocity of circular orbits and the tangent-point method (ga:eq:vr_los, ga:eq:tangent) | ch14 | ch16 (dark matter) |
| Impulse of one encounter, sum of kicks with the logarithm (ga:eq:kicks_sum), relaxation time, escape speed and evaporation time | ch14 | ch15 (Coulomb logarithm in bremsstrahlung may cite ga:eq:kicks_sum) |
| Projected virial mass (ga:eq:Mvir), X-ray hydrostatic mass (ga:eq:mX), Einstein radius (ga:eq:einstein, deflection quoted from GR) | ch14 | — (ch10 Problem 2 already gives the cluster gas temperature; cite it) |
| Tully–Fisher and Faber–Jackson from the virial theorem | ch14 | — |
| Larmor formula (quoted), Lorentz boost matrix, power invariance, relativistic aberration and 1/γ beaming, Debye screening, bremsstrahlung emissivity and cooling (fp:eq:brems_total), free-free absorption, Kramers form (fp:eq:kramers) | ch15 | ch14 (cluster X-rays), ch12 (Kramers sentence) |
| Synchrotron frequency, power, cooling time and break, power-law spectrum index (p−1)/2 | ch15 | — |
| Compton shift (fp:eq:compton_shift), inverse Compton γ² boost, Compton y, Kompaneets (no recoil), Sunyaev–Zel'dovich effect (fp:eq:sz) | ch15 | ch8 (Compton), ch16 (CMB) |
| Accretion luminosity, efficiency, disk torque, thin-disk temperature and ν^{1/3} spectrum, superluminal motion | ch15 | — |
| Hubble's law, scale factor, redshift as stretching | ch16 | — |
| Friedmann, fluid and acceleration equations, critical density, solutions, age | ch16 | — |
| CMB temperature scaling, photon number density, Saha equation, recombination | ch16 | — |
| Freeze-out criterion, n/p ratio, helium fraction, deuterium bottleneck | ch16 | — |
| Growth of density contrast in an expanding universe | ch16 | — |
| Already elsewhere, cite only: Planck and photon gas (ch9), Eddington luminosity (ch11), isothermal sphere (ch12), virial theorem and Jeans (ch10), Gamow tunnelling (ch12), Chandrasekhar mass (ch13), Doppler (ch3), 21 cm (ch8), Thomson cross-section (ch8), Kirchhoff (ch11) | — | — |

## Chapter outlines

### Ch14 — Galaxies and the Motions of Stars (~22 pp)
- 14.1 Our Galaxy. Disk, bulge, halo, the Sun at 8 kpc. How each is measured (star counts, 21 cm from ch8, Galactic coordinates from ch2). Facts in one table.
- 14.2 Rotation curves and dark matter. v_c² = Gm(r)/r. Keplerian fall-off expected outside the light, flat curves observed. The isothermal sphere of ch12 gives a flat curve. Mass-to-light ratio.
- 14.3 Stars as a gas that rarely collides. One encounter deflects little. Velocity kicks add as a random walk (P5), giving t_relax ≈ (N/8 ln N) t_cross. Galaxies never relax, globular clusters do, and their cores collapse (negative heat capacity, ch10).
- 14.4 Weighing galaxies and clusters. Virial mass from σ and R. Zwicky's Coma. Hot cluster gas (ch10 Problem 2) shining by bremsstrahlung (ch15). Lensing mass, one paragraph with the deflection 4GM/(bc²) quoted from GR.
- 14.5 Normal galaxies. Hubble types in a paragraph. Tully–Fisher L ∝ v⁴ and Faber–Jackson L ∝ σ⁴ from the virial theorem with a fixed surface brightness.
- Problem set.

### Ch15 — Radiation from Hot and Fast Particles (~20 pp)
- 15.1 An accelerated charge radiates. The Larmor formula, quoted from electromagnetism, read with P6 (radiated vs kinetic energy).
- 15.2 Bremsstrahlung. One electron passing an ion, the spectrum flat up to 1/(collision time), then averaged over a Maxwell distribution (P3). Emissivity ∝ n_e n_i T^{−1/2} e^{−hν/kT}, cooling ∝ n² T^{1/2}. Cluster X-rays and the cooling time. Free-free absorption by Kirchhoff (ch11), the root of Kramers opacity (ch12).
- 15.3 Synchrotron. Gyration, beaming into a cone 1/γ, the critical frequency γ²ν_g, power ∝ γ²B². A power law of electrons gives a power law of light with index (p−1)/2. Radio galaxies, the Crab.
- 15.4 Compton and inverse Compton. The Compton shift. Inverse Compton by a Lorentz boost there and back (matrices), giving the γ² energy gain. The Compton y parameter and the Sunyaev–Zel'dovich dip in the CMB.
- 15.5 Accretion and active galaxies. L = GMṀ/R and the efficiency GM/(Rc²) (compactness, ch13). Eddington limit (ch11) and quasar black-hole masses. Thin-disk temperature T ∝ r^{−3/4}. Superluminal jets, apparent speed βsinθ/(1−βcosθ).
- Problem set.

### Ch16 — The Expanding Universe (~24 pp)
- 16.1 Hubble's law and the scale factor. Redshift as stretching, 1 + z = a₀/a.
- 16.2 The Friedmann equation from a Newtonian shell (P1 + P2), the same form as general relativity gives. Critical density. Fluid equation from the first law, ρ ∝ a^{−3(1+w)}. Matter, radiation and Λ eras, a(t) for each. The age of the universe (computed for Planck parameters on the cluster).
- 16.3 The microwave background. A blackbody stays a blackbody, T ∝ 1/a. Photon number density. The Saha equation from counting states and detailed balance. Recombination at about 3000 K because photons outnumber baryons by 10⁹ (P6). Last scattering at z ≈ 1100.
- 16.4 Freeze-out and the first three minutes. Γ ≈ H. Neutrino decoupling. Neutron-to-proton ratio, decay, helium fraction Y ≈ 0.25. The deuterium bottleneck.
- 16.5 Growth of structure. Jeans with expansion, the growing mode δ ∝ a in the matter era. Why baryons alone grow too little after recombination, and dark matter.
- 16.6 Accelerating expansion, one section: type Ia supernovae as standard candles (Chandrasekhar mass, ch13), the deceleration parameter.
- Problem set.

## Computing (cluster, via tools/run.sh)
- `code/ch16/01_friedmann.py`: a(t) for Planck 2018 parameters (H₀ = 67.4 km s⁻¹ Mpc⁻¹, Ω_m = 0.315, Ω_Λ = 0.685, Ω_r = 9.1×10⁻⁵), age, the three single-component solutions for comparison.
- `code/ch16/02_recombination.py`: ionisation fraction from the Saha equation against z, recombination redshift where x = 0.5.
- Analytic figures in TikZ: rotation curves (Keplerian vs isothermal), synchrotron power law, thin-disk T(r), superluminal speed vs angle, freeze-out n/p.

## Notation (to log in NOTATION.md)
- Scale factor a(t). In ch14–16 the radiation constant is written a_rad, since a is the scale factor there.
- Hubble parameter H(t), H₀ today. Density parameters Ω_m, Ω_r, Ω_Λ (Ω is the node longitude in ch6, a different block, and the subscript makes it distinct).
- Lorentz factor γ_L in ch15 (γ is the adiabatic exponent in ch9–13). Velocity ratio β = v/c.
- Density contrast δ. Equation-of-state ratio w = P/(ρc²).

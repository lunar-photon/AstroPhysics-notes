# Astrophysics Lecture Notes & Comprehensive Handbook

A comprehensive, mathematically rigorous graduate and advanced undergraduate level textbook and reference handbook covering observational, positional, dynamical, and instrumental astrophysics.

---

## 📚 Contents & Chapter Overview

### **Preface & Roadmap**
- Philosophical overview of observational astrophysics, reference frames, instrument resolution limits, and celestial mechanics.

### **Chapter 1: Time Standards and Systems**
- **Solar vs. Sidereal Time**: Earth rotation, geometric relations ($T_\odot / T_* = 366.25 / 365.25$).
- **Astronomical Years**: Sidereal, Tropical, and Anomalistic years and precession effects.
- **Equation of Time ($\mathrm{EoT}$)**: Decomposition into orbital eccentricity ($\Delta t_e$) and Earth's obliquity ($\Delta t_\varepsilon$) with analytical sinusoidal derivations and TikZ visualizations.
- **Modern Time Standards**: Solar, Sidereal (IAU GMST polynomial), Dynamical, and Relativistic Time Systems ($\UT0, \UT1, \TAI, \UTC, \TT, \TCG, \TCB, \TDB$).

### **Chapter 2: Celestial Coordinate Systems & Transformations**
- **Fundamental Coordinate Systems**:
  - Horizontal / Alt-Azimuth ($\mathrm{Alt}, \mathrm{Az}$)
  - Equatorial (Hour Angle & Right Ascension: $\mathrm{HA}, \delta$ and $\alpha, \delta$)
  - Ecliptic ($\lambda, \beta$)
  - Galactic ($l, b$) with transformation matrices and J2000 Galactic North Pole / Center anchors.
- **Observational Transformations**:
  - Diurnal motion and rising/setting/transit conditions.
  - Plane-parallel and spherical atmospheric refraction models ($\Delta z \approx 58.2'' \tan z$).
  - Airmass models ($X(z) = \sec z$ and Young & Irvine empirical corrections).
  - Parallactic angle ($\eta$) derivation via spherical trigonometry.

### **Chapter 3: Astrometry & Galactic Kinematics**
- **Trigonometric Parallax**: Heliocentric parallax ($\varpi$), parsec definition, and distance modulus.
- **Proper Motion**: Angular proper motions ($\mu_\alpha^*, \mu_\delta$) and exact derivation of the $4.74047\,\text{km}\,\text{s}^{-1}$ conversion constant.
- **3D Space Velocity & Galactic $(U, V, W)$ Motion**: Heliocentric to Galactocentric kinematic transformations relative to the Local Standard of Rest ($\mathrm{LSR}$).

### **Chapter 4: Photometry, Radiometry & Stellar Properties**
- **Flux, Luminosity, and Distance Modulus**: Inverse-square law, bolometric and monochromatic flux.
- **Pogson's Magnitude Scale**: Historical origins, logarithmic definition, and zero-point calibration.
- **Color Indices & Extinction**: $U, B, V, R, I$ photometric bands, color excess $E(B-V)$, and interstellar extinction law ($A_V = R_V E(B-V)$).
- **Blackbody Radiation & Stellar Radii**: Planck function, Wien's displacement law, Stefan-Boltzmann law, and radiometric radius estimation.

### **Chapter 5: Wave Optics, Telescope Geometry & Angular Resolution**
- **Telescope Geometries**: Refractors, Newtonians, and Cassegrain two-mirror systems (similar triangles and effective focal length).
- **Plate Scale & Pixel Scale**: $P = \dv{\theta}{s} = \frac{1}{F}$, plate scale evaluation $\theta_{\rm pix} \simeq \frac{y}{F}\big|_{y=p} = 2.06''/\text{pixel}$.
- **Resolution Limit Physics**:
  - 1D Single Slit first minimum ($1.00\lambda/a$).
  - 2D Circular Aperture Fourier optics and first zero of $J_1(\pi D \theta / \lambda)$ yielding the Airy disk radius ($\theta_{\rm res} = 1.22 \lambda/D$).
- **Interferometry**: Baseline path difference lag $\Delta L_1 = B\sin\theta_1, \Delta L_2 = B\sin\theta_2 \implies B\theta = \lambda \implies \theta_{\rm res} = \lambda/B$. Geodesic chords and VLBI arrays.
- **Nyquist-Shannon Sampling**: Critical sampling condition $\text{Pixel Scale} \le \theta_{\rm res}/2$ and undersampling analysis.
- **Atmospheric Seeing & Adaptive Optics**: Fried parameter ($r_0$), Moffat profile PSFs, Strehl ratio, and deformable mirrors.

### **Chapter 6: Gravitational Dynamics & The Two-Body Problem**
- **Keplerian Mechanics**: Center-of-mass reduction, angular momentum conservation, Laplace-Runge-Lenz ($\vec{A}$) vector, and exact orbit equations.
- **Kepler's Equation & Orbital Anomalies**: True ($\nu$), eccentric ($E$), and mean ($M$) anomalies, solved via Newton-Raphson iteration.
- **Binary Stars & Mass Functions**: Radial velocity curves, eclipsing binary light curves, and relativistic Rømer delays in binary pulsars.
- **Worked Problem Sets**: Full analytical step-by-step problem sets with diagrams.

### **Chapter 7: CCD Noise Modeling & Signal-to-Noise Ratio (SNR)**
- **Poisson Photon Counting Statistics**: Variance of Poisson distributions ($\sigma_N^2 = \mu$).
- **Noise Budget**: Source Poisson noise, sky background noise, dark current shot noise, read noise ($\sigma_{\rm RN}$), and quantization noise.
- **Master CCD SNR Equation**: Exact mathematical proof for $N_{\rm pix}$ aperture summation and $N_{\rm exp}$ exposures.
- **Observational Regimes**: Source-dominated, sky-dominated, and read-noise-dominated regimes with limit cases.

### **Chapter 8: The Interstellar Medium**
- Composition and phases, extinction and scattering regimes, line broadening, the 21 cm line, cloud types, planetary-nebula expansion, heating and cooling.

### **Chapter 9: Six Principles**
- The six principles every later result is built from: conservation (continuity and Euler equations), gravity of a sphere (Gauss's law, gravitational energy), counting states (pressure integral, ideal gas, photon gas, Planck spectrum), balance of rates (steady state, detailed balance), random walk (the √N law, diffusion flux), and comparing two scales.

### **Chapter 10: Self-Gravitating Gas**
- Hydrostatic equilibrium, the virial theorem by two routes and what it says about temperature, binding and the adiabatic index, negative heat capacity and the ensembles, the Jeans criterion by energy and by waves, free fall and the three clocks of a star, rotation and the end of collapse.

### **Chapter 11: Radiation in Matter**
- Specific intensity, the transfer equation and its formal solution, Kirchhoff's law and LTE, radiative diffusion, the Eddington luminosity, Einstein coefficients, the grey atmosphere.

### **Chapter 12: The Equations of a Star**
- The four structure equations in the mass coordinate, convection, mean molecular weight, degeneracy pressure, opacity, the Gamow peak, boundary conditions and how stars are computed (shooting, Henyey relaxation), polytropes and the isothermal sphere, Eddington's standard model, homology and the HR diagram.

### **Chapter 13: Degenerate and Compact Stars**
- Compactness, white dwarfs and the Chandrasekhar mass, the relativistic structure equations (TOV, Tolman–Ehrenfest), computing neutron stars, black holes.

---

## 🛠 Compilation Instructions

To compile the master document into a complete PDF:

```bash
pdflatex -interaction=nonstopmode AstroPhysics.tex
pdflatex -interaction=nonstopmode AstroPhysics.tex
```
*(Running twice ensures all cross-references, tables of contents, and figure references resolve properly.)*

### Prerequisites
- TeX Live (2022 or newer recommended) or MiKTeX
- Standard packages: `amsmath`, `physics`, `tikz`, `tcolorbox`, `listings`, `booktabs`, `wasysym`, `graphicx`, `hyperref`.

---

## 📂 Repository Structure

```
.
├── AstroPhysics.tex       # Master root LaTeX document
├── preamble.tex           # Packages, math shortcuts, color themes, and TikZ styles
├── AstroPhysics.pdf       # Compiled publication-ready PDF document
├── chapters/              # Modular chapter sources
│   ├── preface.tex
│   ├── ch1_time_systems.tex
│   ├── ch2_coordinates.tex
│   ├── ch3_astrometry.tex
│   ├── ch4_photometry.tex
│   ├── ch5_angular_resolution.tex
│   ├── ch6_two_body.tex
│   ├── ch7_ccd_noise.tex
│   ├── ch8_interstellar_medium.tex
│   ├── ch9_six_principles.tex
│   ├── ch10_self_gravitating_gas.tex
│   ├── ch11_radiation_in_matter.tex
│   ├── ch12_equations_of_a_star.tex
│   └── ch13_compact_stars.tex
├── fig_sources/           # Standalone TikZ sources of the figures
├── figs/                  # Compiled figures (make figs)
├── code/chNN/             # Python scripts, run on the cluster with tools/run.sh
├── results/chNN/          # Script outputs: data tables and LaTeX number macros
├── tools/                 # run.sh (cluster), wl.sh (Wolfram), limit_watchdog.sh
├── STYLE_GUIDE.md         # House rules for writing the notes
├── STYLE_CH6.md           # How chapter 6 organises calculations (the model)
├── NOTATION.md            # Notation register
├── PLAN_stellar_physics.md
├── WORKING.md             # Current state of the work
├── .gitignore
└── README.md
```

---
*Authored and maintained by Chandra Prakash (@lunar-photon).*

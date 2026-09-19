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
│   └── ch7_ccd_noise.tex
├── figs/                  # Figures, plots, and astronomical diagrams
│   ├── 3D_Spherical.png
│   ├── Binary_Star.png
│   ├── Two Body Problem.png
│   └── ... (20+ diagram assets)
├── .gitignore
└── README.md
```

---
*Authored and maintained by Chandra Prakash (@lunar-photon).*

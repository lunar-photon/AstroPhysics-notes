# How ch6 is written (extract, so agents need not read the chapter)

Ch6 (`chapters/ch6_two_body.tex`, ~3000 lines) is the owner's model for how calculations are organised. This file holds what to copy, with short real excerpts. It also lists what not to copy, since ch6 is a draft, and how it differs from the default habits of a model writer. The line-level form of a chain is the template's `\eqby` + `explain` (STYLE_GUIDE rule 11). Everything else about the flow comes from here.

Lecture photos, slides and problem sheets are sources of *topics* only, never of style. The owner's own writing is ch6.

## 1. Shape of a chapter

- **Sections follow the logic of the solution, one move per section.** Ch6 goes central force → separate the centre of mass → conserved quantities → orbit equation → Kepler orbits → E and L in terms of a, e → anomalies → third law → Kepler's equation → Runge–Lenz → perturbations. Each section title names the move or its result.
- **Variants are sibling subsections, not digressions.** "Elliptical orbits: eccentric anomaly" and then "Hyperbolic trajectories" uses the same steps with cosh in place of cos.
- **A "collecting results" block** gathers the formulas of a stretch in one `align` before moving on.
- **A problem set closes the chapter.** Each problem has **Problem Statement** (physical setup, numbers, parts (a)–(d)), then **Essential Ideas** (2–3 bullets with the governing equations), then **Detailed Solutions** (each part with a bold content heading, the formula, the numbers, and a boxed answer). The last part ends with one sentence on why the result matters ("Double-lined eclipsing binaries are valuable for exactly this reason…").

## 2. Shape of a derivation

1. **One line states the goal.** "We now want r(t) (and hence φ(t)), not just r(φ)." "To get the orbit *shape* r(φ) we change independent variable from t to φ."
2. **The general setup comes first.** "A central force … is a gradient of a scalar potential V(r)." Everything that does not need the form of V is derived before V = −GMμ/r is used.
3. **What is used is named before or at the step.** Ch6 does this as "using \eqref{…}–\eqref{…} to trade E, L for a, λ" or `\tag{using λ = a(1−e²)}`. In the new chapters this becomes the `\eqby` label and its `explain` item.
4. **Every intermediate expression is written out.** Ch6 writes d²r/dt² in full before substituting it.
5. **A substitution comes with its reason.** "Substitute r = a(1 − e cos u) … (this choice guarantees r > 0 throughout, since −1 ≤ cos u ≤ 1)."
6. **Evaluate where the algebra is simplest, and say why it is allowed.** "Since E is conserved, evaluate at periapsis (φ = ω), where r = a − ae and ṙ = 0 (turning point of r)."
7. **The result is boxed.** `\boxed{E = −GMμ/2a}`, `\boxed{n = √(GM/a³)}`.
8. **One or two sentences read it.** Usually this says what the result depends on, what it doesn't, or what the sign means. "So E is conserved for *any* central potential V(r), not just gravity." "Since λ > 0 always, the sign of E tracks e."

## 3. Devices to copy (with ch6 instances)

| Device | Ch6 instance |
|---|---|
| Matrix form for a coupled system | Centre-of-mass separation. The mass matrix is diagonalised by left-multiplying with an explicit 2×2 matrix. Frame rotations are products of explicit rotation matrices. |
| Count the constants or unknowns | "Six second-order ODEs ⇒ 12 constants", later shown as (R₀, V_CM) 6 + (a, e, i, Ω, ω, t_p) 6 = 12. |
| `\underbrace` names a known piece | (r × p) · L with r × p underbraced as L. |
| Generality statement | "valid for any central potential". "It follows purely from L being conserved … no dependence on the specific form of V(r)." |
| Second route to the same result | The conic r(φ) from the orbit equation, and again from x²/a² + y²/b² = 1 written about the focus. |
| Consistency check at special points | "At u = 0 and u = π, v = u, so periapsis and apoapsis coincide for the two anomalies, as they must by symmetry." |
| What new information a quantity carries | "Since e, Ω, ι are already determined by (E, L), the only *new* information in A is ω." |
| Ordering argument for an approximation | "Since the perturbing force is O(ε), the rates are O(ε) … the remaining quantities need only be evaluated at zeroth order." |
| Term defined in bold at first use, inline | "where u is the **eccentric anomaly**". "the **semi-latus rectum** λ ≡ L²/(GMμ²)". |
| A table of cases | e = 0 circle, 0 < e < 1 ellipse (E < 0), e = 1 parabola, e > 1 hyperbola. |
| Short content headings inside a section | `\paragraph{Angular momentum.}`, `\paragraph{Inverting for a, e.}`, `\paragraph{Direction and magnitude of A.}` |

Proportions in ch6 are 84 boxed results, 54 `\eqref` citations, 18 matrices, 7 underbraces, 9 paragraph headings and only 1 box environment. The equations carry the chapter, and the prose between displays is usually one sentence.

## 4. Do not copy (draft defects in ch6)

- **Skipped algebra.** "Substituting and simplifying (the terms cancel), one obtains", or "Differentiating the v–u relation …, one finds dv/du = …". Rule 12 (every line shown) wins.
- **Hard-coded references.** "(Chapter~3)", and a manual `\tag{65a}`. Use `\ref`/`\eqref`.
- **Notation drift.** The true anomaly appears as both ν and v, the inclination as both ι and i, and the polar angle as both θ and φ. One symbol per quantity (NOTATION.md).
- **Typos and grammar slips.** "doting", "constitutes four constant".
- **Code hygiene.** `\newcommand` inside a figure environment, a figure with no caption or label, a `tcolorbox` with no title.
- **Little or no opening story.** Ch6 starts straight on the problem. The new chapters add the template's 8-step opening (STYLE_GUIDE rule 20) in front, then proceed in ch6's manner.

## 5. Ch6 compared with a model's default writing

The default habits below are visible in ch8's collapse sections (lines 272–443), written in a model's voice. Each row says what to do instead.

| Default model habit | Ch6 way |
|---|---|
| Signposting transitions, e.g. "We now turn from radiative properties to self-gravitating dynamics", "The next section makes this … quantitative" | One goal line, then the math. No talk about sections. |
| Emphatic words, e.g. "precisely why", "dramatically shorter", "This is precisely what justifies" | A plain statement of what follows and from what. |
| Long sentences with dashes and semicolons that carry several ideas | One idea per sentence, mostly one sentence between displays. |
| Compressed algebra, e.g. "A standard identity … gives", "Integrating by parts and discarding the surface term" | Each step displayed, with the identity proved or cited by `\eqref`. |
| Prose explanation in place of an equation | The equation, then a one-line reading. |
| New names and abbreviations introduced freely (∇_ad, β, χ, …) | The fewest letters. Ch6 runs on μ, L, E, λ, e, a. |
| Key-result boxes and summary bullets everywhere | `\boxed{}` on the equation itself. Lists only for real cases or problem parts. |
| Interpretation inflated into a lesson at the end of each paragraph | Interpretation only where it adds a fact (sign, dependence, symmetry, new information). |
| Results quoted from memory | Results derived or cited to where they are derived, with a second route where one exists. |

## 6. A worked instance of the target (virial theorem)

The target style, with ch6 organisation and template chains:

```latex
\paragraph{Hydrostatic equilibrium, summed over the star.}
To see what hydrostatic equilibrium says about the star as a whole, we weight it by
$4\pi r^3$ and integrate from the centre to the surface (P1 + P2).
\begin{align}
  \int_0^R 4\pi r^3\,\dv{P}{r}\,dr
  &\eqby{1} \bigl[4\pi r^3P\bigr]_0^R - 3\int_0^R 4\pi r^2P\,dr \nonumber\\
  &\eqby{2} -3\int P\,dV, \nonumber\\
  \int_0^R 4\pi r^3\,\dv{P}{r}\,dr
  &\eqby{3} -\int_0^M \frac{Gm}{r}\,dm \eqby{4} U .
\end{align}
\begin{explain}
  \item Integration by parts.
  \item $r^3=0$ at the centre and $P=0$ at the surface; $dV=4\pi r^2dr$.
  \item Hydrostatic equilibrium \eqref{eq:hse}, and $dm=4\pi r^2\rho\,dr$.
  \item Definition of the gravitational energy $U$ \eqref{eq:U_def}.
\end{explain}
\[
  \boxed{3\int P\,dV + U = 0}
\]
Only gravity and the pressure enter, so this holds for any equation of state.
```

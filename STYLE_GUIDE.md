# House style for the Astrophysics notes

The one rulebook for these notes. Every writer and agent reads it before writing. Content plans live in `PLAN_stellar_physics.md`, symbols in `NOTATION.md`, and stage state in `WORKING.md`.

Origin tags on each rule:
- **[T]** taken from the template (`~/Documents/writing-templates/book-notes-template/STYLE_GUIDE.md`) unchanged.
- **[T→]** from the template, but changed for this project (the change is stated).
- **[N]** new for this project (from the owner's requests on 2026-10-15 or saved preferences).
- Rules marked "(owner, 2026-10-15)" were settled by the owner's answers on that date.

---

## 1. Purpose

1. **Six principles, used everywhere. [N]** (Placement, owner 2026-10-15: stated and derived once, up front, in ch9. Later chapters only apply them.) Every result is derived from six principles plus ordinary classical and quantum physics. P1 Conservation, P2 Gravity of a sphere, P3 Counting states, P4 Balance of rates, P5 Random walk, P6 Compare two scales. The reader remembers the principles, not the results. The notes show the same principles at work again and again, because that repetition is what removes the need to memorise.
2. **Not a summary, more detailed than the sources. [T]** Wherever a source says "it is easy to see", show it.
3. **First principles, then simplify. [T→]** The template says derive, never postulate. Added: the general form is written before any special case (saved preference).
4. **Spell out the insight. [N]** After a result, say what it means physically, and what it does and does not depend on (e.g. the virial theorem says gravity sets the temperature, using only M/R).
5. **Reader. [T→]** The template says self-contained and supplies anything the source assumes. Changed: the reader knows mechanics, electromagnetism, thermodynamics, statistical mechanics, quantum mechanics and GR. These are used, not recapped (e.g. TOV is quoted from the owner's GR notes).
6. **Selection. [T→]** The template says nothing in the source may be silently dropped. Changed: a topic goes in only if it is derived from the six principles and used in more than one place, or is needed for such a derivation. Catalogue facts and specialist machinery get one sentence or nothing.
7. **Length. [N]** About 400–500 pages for the whole notes, as a guide. Hard chapters get the pages they need. Unneeded material is cut, never explanation.
8. **Merge, never append. [N]** Lecture notes, slides, problem sets and side discussions (like the stellar-collapse PDF) are woven into the storyline where each point belongs. They are sources of *topics* only. Their order, notation and way of presenting are not followed (owner, 2026-10-15). The owner's own way of presenting is ch6.
9. **The existing chapters (ch1–8) are drafts. [N]** They get filled in and reworked to these rules so the whole set reads as one text, with the six principles threaded through them. Order (owner, 2026-10-15): the new block (ch9–13) is written first, so the style is settled on new text, and ch1–8 are reworked after it.

## 2. Presentation (the model is ch6, `chapters/ch6_two_body.tex`)

10. **General first, then the special case. [N]** Ch6 solves any central V(r) before setting V = −GMμ/r.
11. **Labelled equality chains. [T]** (owner, 2026-10-15, replaces an earlier answer) Every calculation is a multi-line chain in `align`. Every non-trivial `=` is `\eqby{1}`, `\eqby{2}`, … (restart at 1 in each chain), and `\relby{n}{\le}` for other relations. Immediately after the chain, an `explain` list gives one sentence per label. Trivial arithmetic may use a bare `=`. Each derivation also names the principles it combines (P1 + P2, …) before it starts [N].
11a. **Organise each calculation the way ch6 does. [N]** The chains above are the line-level form. Ch6 is the model for how a calculation is laid out from start to finish. Read `STYLE_CH6.md` (the extract, with excerpts, things not to copy, and a worked instance) instead of the chapter itself.
   - Write the general setup first, then specialise (any V(r) before gravity).
   - Split a long derivation into its natural moves, each under a short run-in heading that carries content ("Angular momentum.", "Inverting for a, e.").
   - Before each move, one line says what is about to be done and why ("To get the orbit shape r(φ) we change the independent variable from t to φ").
   - Evaluate where the algebra is simplest, and say so ("evaluate at periapsis, where ṙ = 0").
   - Write a coupled system as one matrix equation.
   - Use `\underbrace` to name a piece that is a known quantity.
   - Give key equations a `\label` and cite them by `\eqref` later, instead of restating them.
   - End on a `\boxed{}` result and read it in one or two sentences, including what it does and does not depend on.
12. **Every line of algebra shown. [T]** There is no "after some algebra" and no expert one-liner. A step the reader can't fill in is done on the spot or `\ref`'d to where it is done.
13. **Matrices for transformations. [N]** Rotations, frame changes and the centre-of-mass separation are written as explicit matrix–vector equations (saved preference).
14. **Count unknowns against equations. [N]** As ch6 counts 12 constants as 6 + 6.
15. **Box the result, then read it in one or two sentences. [N]**
16. **Cross-check by a second route when one exists. [N]** Related to the template's "check every assumption numerically" [T], which also holds. Each approximation is tested against the full calculation where it is used.
17. **Fewest symbols. [T→]** The template already says to add a new symbol only when it can't be avoided (§5.16). Strengthened: a principle comes with the minimum number of new letters, and everything else is written out. Before writing a section, list its symbols and justify each one.
18. **One notation, in a register. [T]** `NOTATION.md` is read before writing and updated with every new symbol, rename or write-out. It is how agents agree on notation.
19. **Re-anchor symbols. [T]** At first use in each subsection, say what a symbol is and where it came from.
20. **Section openings. [T]** (owner, 2026-10-15) Every section opens with the template's full 8-step shape, in simple language. (1) What the reader already has and what it handles. (2) Plainly, when that is not enough. (3) An everyday physical story that already contains the whole trick, before any symbol. (4) The same situation in the astrophysics, then the idea of the section in one sentence. (5) The story in symbols, the smallest example with numbers that match the story. (6) A picture in plain words. (7) One idea, many names, meaning where else the principle works (this is where the six principles get named and repeated). (8) One or two sentences on what the section develops. Never repeat a framing already given, never chain several section references in one sentence, no jargon before the story needs it. The worked instance is the template's `sources/clarity_exemplar_opening.tex`. Use its shape, never its text. After the opening, the section proceeds in ch6 style.
21. **No meta commentary. [T]** The text never talks about itself ("this section", "in what follows", "the next section makes…", "beyond the scope of this volume"). Grep for the banned phrases before reporting a part as done.
22. **Authorial "we", statements not instructions. [T]**
23. **No classifier labels. [T]** No "Set-up." or "Note." run-in headings. A `\paragraph{}` heading must carry content.
23a. **One home per derivation, no collisions. [T→]** The template says "connected, not repeated". Made strict (owner, 2026-10-15): every derivation is done exactly once, at the home listed in the plan's "Derivation homes" table. Anywhere else, the text says in one line that it was derived there (`\eqref`/`\ref`), uses the result, and moves on. No re-derivation, no shortened re-derivation, no second "for completeness" version. Before writing a section, check the homes table. If a needed derivation has no home yet, add it to the table first (like a symbol in `NOTATION.md`). A second *route* to the same result (rule 16) is allowed only at the home itself.
24. **A quantity met again is connected. [T]** Recall what the reader saw (with the earlier number) and say what is the same and what differs.
25. **Never type a chapter number. [T]** Always `\ref{ch:…}` (current drafts hard-code "Chapter~6" and need fixing).
26. **No summary at the end of a chapter. [T→]** (owner, 2026-10-15) The template's "Chapter summary" table and the per-part `recap` box are dropped, and so is any end-of-chapter ledger. The repetition of the six principles happens inside the text, where each derivation names the principles it combines, and in step 7 ("one idea, many names") of each section opening.

## 3. Writing

27. **Simple English. [T→]** The template says plain words. Strengthened (saved preference): short plain sentences, no colons in prose, no fancy words. Equations are unaffected.
28. **Humanize the prose. [N]** Load the `humanizing-writing` skill before drafting or revising prose. Be specific, say each thing once, use plain verbs, and no inflated or filler phrases.
29. **Boxes are rare. [T]** The main text carries the whole argument. A box holds only what a reader may want to find again. At most about 3 per section, never back to back, never first in a section.
30. **No lemma/theorem/proof environments. [T]**
31. **Working definitions with green `\unpack{}` brackets. [T→]** Changed (owner, 2026-10-15): brackets only inside the few working-definition boxes, never in running text. Each bracket is short, relevant to the passage, literally correct and has no semicolons [T]. Needs a `workdef` box and an `\unpack` macro in `preamble.tex`.
32. **Worked examples. [T→]** The template wants 2–3 per section. Changed (owner, 2026-10-15): one or two short worked examples in the text, where they show a principle at work (e.g. the Sun's virial temperature). Each chapter also ends with a problem set with full solutions, as the drafts already do.

## 4. Figures

33. **Geometry must be true, curves are computed. [T]**
34. **No labels on arrows, no congestion, aligned panels. [T]**
35. **Captions only describe what is shown. [T→]** The template says captions narrate the picture. Strengthened (saved preference): the explanation goes in the text, never in the caption.
36. **Build each new figure standalone first. [N]** Iterate in `test/`, merge into the chapter only once it renders correctly (saved preference). Sources go in `fig_sources/`, PDFs in `figs/`.
37. **Figures where they help. [T→]** The template says at least 2 per section. Changed (owner, 2026-10-15): a figure wherever a picture explains faster than words. Every chapter has several, and a short section may have none.

## 5. Computing

38. **Python only as SLURM jobs on padmanabha. [T→]** The template's `tools/run.sh` falls back to the laptop. Changed: `tools/.no_local` is set, so Python never runs on the laptop.
39. **No code on the login node. [T]** The login node is for file transfer, mkdir and job control (`sbatch`, `squeue`, `scancel`) only. The owner confirmed this on 2026-10-15 after a slip.
40. **Wolfram on the laptop for symbolic work. [T→]** `tools/wl.sh -c` for a one-off check, `-s <name>` for a step-by-step session, and cell-structured `.wls` scripts for anything the text cites. **[T→]** The template says no algebra in the head at all. Changed (owner, 2026-10-15): every integral, series, limit and non-obvious simplification is checked in Wolfram before it goes in the text. Plain one-line rearrangements are not.
41. **Numbers are never typed by hand. [T]** A number the text quotes from a computation is written to `results/chNN/` by the script and loaded as a macro.

## 6. Process

42. **`WORKING.md` is the stage memory. [N]** Read it at the start of a session. Log decisions as they happen.
43. **Build check. [T→]** The template uses `tools/testpart.sh`. Here, `make` (or `make quick`) must build without errors, and the changed pages are looked at.
44. **Commit or push only when the owner asks. [N]**

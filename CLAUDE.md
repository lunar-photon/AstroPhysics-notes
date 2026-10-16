# Astrophysics course notes

Read these before acting, in this order.
1. **`WORKING.md`**: where the work stands, the decisions and why, and the next steps. Log decisions as they happen (1–3 lines). At stage end, distill settled conclusions into long-term memory and reset the file.
2. **`STYLE_GUIDE.md`**: the one rulebook (purpose, presentation, writing, figures, computing, process). **`STYLE_CH6.md`** extracts how ch6 organises calculations. Read it instead of ch6 itself.
3. **`NOTATION.md`**: the notation register. Read it before writing, and log every new symbol, rename or write-out.
4. **`PLAN_stellar_physics.md`**: the content plan for the current block.

## Limit watchdog
- Keep `tools/limit_watchdog.sh` running as a background command (Bash `run_in_background`) for the whole session. It reads the exact reset time from a usage-limit error in this project's transcripts and exits at that moment, which wakes Claude. After it fires (output `LIMIT_RESET …`), read `WORKING.md`, resume the stopped work, and start the watchdog again. A second copy exits at once (`WATCHDOG_ALREADY_RUNNING`), so starting it is always safe.

## Build
- `make` builds `AstroPhysics.pdf` (two pdflatex passes). `make quick` does one pass. `make figs` compiles `fig_sources/*.tex` to `figs/*.pdf`.

## Computing
- Python runs only as SLURM jobs through `tools/run.sh code/chNN/script.py` (padmanabha, env `~/envs/cosmology`, remote dir `~/astrophysics_runs/Astro`). `tools/.no_local` blocks laptop runs. Nothing computes on the login node.
- Wolfram runs on the laptop through `tools/wl.sh`.

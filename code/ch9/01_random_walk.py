r"""Random walks in the plane: how far does a walker get after N unit steps?

Question. Section "Random walk" (P5) claims the root-mean-square distance after N steps of
length s in random directions is sqrt(N) s. This script checks it and draws the figure.

Computes
  - one example walk of N = 100 unit steps (directions uniform in angle),
  - the end points of 500 independent walks of N = 100 steps,
  - the measured rms end distance over 100 000 walks, to compare with sqrt(N) = 10.

Writes
  results/ch9/random_walk_path.dat     x y of the example walk (101 points)
  results/ch9/random_walk_ends.dat     x y of 500 end points
  results/ch9/random_walk.tex          LaTeX macros \NineRWsteps, \NineRWrms, \NineRWwalks
"""
import os
import numpy as np

N = 100                 # steps per walk
N_SHOWN = 500           # end points drawn in the figure
N_STATS = 100_000       # walks used for the rms check
rng = np.random.default_rng(20261015)

out = os.path.join("results", "ch9")
os.makedirs(out, exist_ok=True)


def walks(n_walks, n_steps):
    """Return positions after each step, shape (n_walks, n_steps + 1, 2)."""
    angles = rng.uniform(0.0, 2.0 * np.pi, size=(n_walks, n_steps))
    steps = np.stack([np.cos(angles), np.sin(angles)], axis=-1)
    start = np.zeros((n_walks, 1, 2))
    return np.concatenate([start, np.cumsum(steps, axis=1)], axis=1)


example = walks(1, N)[0]
ends = walks(N_SHOWN, N)[:, -1, :]
stats_ends = walks(N_STATS, N)[:, -1, :]
rms = float(np.sqrt(np.mean(np.sum(stats_ends**2, axis=1))))

np.savetxt(os.path.join(out, "random_walk_path.dat"), example, fmt="%.5f")
np.savetxt(os.path.join(out, "random_walk_ends.dat"), ends, fmt="%.5f")
with open(os.path.join(out, "random_walk.tex"), "w") as fh:
    fh.write(f"\\newcommand{{\\NineRWsteps}}{{{N}}}\n")
    fh.write(f"\\newcommand{{\\NineRWrms}}{{{rms:.2f}}}\n")
    fh.write(f"\\newcommand{{\\NineRWwalks}}{{{N_STATS:,}}}\n".replace(",", "\\,"))

print(f"N = {N}: rms end distance over {N_STATS} walks = {rms:.4f} (sqrt(N) = {np.sqrt(N):.4f})")
print(f"example walk ends at distance {np.hypot(*example[-1]):.3f}")

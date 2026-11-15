r"""Crossing times of the rungs of the cosmic hierarchy, compared with the age of the universe.

Question. Section "Groups, Clusters and the Cosmic Web" asks which structures have had time to
settle. A structure of size L (radius R = L / 2) and typical speed v needs t_cross = R / v (as in the section on stars as a gas that rarely collides) to cross itself once.
How does that compare with the age t_0 of the universe?

Reads   nothing (sizes in Mpc and speeds in km/s are the inputs listed below).
Computes t_cross = R / v = L / (2 v) in Gyr, t_cross / t_0, and H_0 R / v (the speed at which the expansion
         would pull the two ends of the structure apart, in units of the internal speed).
         t_0 is the age of the flat universe with H_0 = 67.4 and Omega_m = 0.315 (as 02_sdss_wedge.py).
Writes   results/ch14/hierarchy.tex  macros \FourteenH<Name>{Tcross,Ratio} for each row.
"""
import os
import numpy as np

H0, OM = 67.4, 0.315
MPC_KM, GYR_S = 3.0857e19, 3.15576e16
u = np.linspace(1e-6, 1.0, 200001)
a = u ** 2
f = 2 * u / (a * H0 * np.sqrt(OM / a ** 3 + 1 - OM))
t0 = np.sum(0.5 * (f[1:] + f[:-1]) * np.diff(u)) * MPC_KM / GYR_S

# name: (size L in Mpc, typical speed v in km/s)
rows = {"MW": (0.030, 220.0), "LG": (3.0, 100.0), "Virgo": (3.0, 700.0), "Coma": (3.0, 1000.0),
        "VSC": (30.0, 300.0), "Lan": (160.0, 600.0)}
fm = lambda v: f"{v:.0f}" if v >= 10 else f"{v:.2g}"   # no exponent in the macros
os.makedirs(os.path.join("results", "ch14"), exist_ok=True)
res = {}
with open(os.path.join("results", "ch14", "hierarchy.tex"), "w") as fh:
    for k, (L, v) in rows.items():
        R = L / 2
        tc = R * MPC_KM / v / GYR_S
        res[k] = (tc, tc / t0, H0 * R / v)
        fh.write(f"\\newcommand{{\\FourteenH{k}Tcross}}{{{fm(tc)}}}\n")
        fh.write(f"\\newcommand{{\\FourteenH{k}Ratio}}{{{fm(tc / t0)}}}\n")
        fh.write(f"\\newcommand{{\\FourteenH{k}Hubble}}{{{fm(H0 * R / v)}}}\n")
    fh.write(f"\\newcommand{{\\FourteenHHubbleTime}}{{{MPC_KM / H0 / GYR_S:.1f}}}\n")
    fh.write(f"\\newcommand{{\\FourteenHHzeroTzero}}{{{t0 * GYR_S * H0 / MPC_KM:.2f}}}\n")
for k, r in res.items():
    print(k, "t_cross %.3g Gyr  ratio %.3g  H0L/v %.3g" % r)
# t_cross / t_0 = (H_0 R / v) / (H_0 t_0), with H_0 t_0 about 0.95
for k, (tc, ra, hv) in res.items():
    assert abs(ra - hv / (H0 * t0 * GYR_S / MPC_KM)) < 1e-9
assert 13.6 < t0 < 14.0
assert res["Coma"][1] < 0.3 and res["Lan"][1] > 5 and res["MW"][1] < 0.02   # settled vs not
print("self-check ok")

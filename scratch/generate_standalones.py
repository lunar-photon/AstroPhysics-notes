import os
import glob
import re

STANDALONE_TEMPLATE = r"""\documentclass[tikz,border=6pt]{standalone}
\usepackage{amsmath,amssymb,mathtools,physics,bm,nicefrac,wasysym}
\usepackage{xcolor}

\definecolor{colone}{RGB}{180,60,60}
\definecolor{coltwo}{RGB}{60,110,180}
\definecolor{colthree}{RGB}{60,140,80}

\definecolor{accent}{HTML}{A13D2C}
\definecolor{accent2}{HTML}{2B5F6B}
\definecolor{muted}{HTML}{5A564F}
\definecolor{panel}{HTML}{F8F6F0}
\definecolor{linecol}{HTML}{D8D2C4}
\definecolor{ink}{HTML}{1E1C1A}
\definecolor{astroblue}{HTML}{1B4F72}
\definecolor{astrodark}{HTML}{17202A}
\definecolor{sunyellow}{HTML}{E8A33D}

\usetikzlibrary{calc,arrows.meta,positioning,decorations.pathreplacing,decorations.markings,angles,quotes,shapes.geometric}
\usepackage{tikz-3dplot}

\newcommand{\vecr}{\vec r}
\newcommand{\vecL}{\vec L}
\newcommand{\vecA}{\vec A}
\newcommand{\vecf}{\vec f}
\newcommand{\vecF}{\vec F}
\newcommand{\vecp}{\vec p}
\newcommand{\avg}[1]{\left\langle #1\right\rangle}
\newcommand{\vecx}{\vec x}
\newcommand{\hatn}{\hat n}
\newcommand{\rhat}{\hat r}
\newcommand{\phihat}{\hat\phi}
\newcommand{\thetahat}{\hat\theta}
\newcommand{\note}[1]{\textcolor{blue!60!black}{\textit{[#1]}}}

% Astronomical acronyms
\newcommand{\LST}{\mathrm{LST}}
\newcommand{\GST}{\mathrm{GST}}
\newcommand{\GMST}{\mathrm{GMST}}
\newcommand{\GAST}{\mathrm{GAST}}
\newcommand{\LMST}{\mathrm{LMST}}
\newcommand{\LAST}{\mathrm{LAST}}
\newcommand{\UT}{\mathrm{UT}}
\newcommand{\UTC}{\mathrm{UTC}}
\newcommand{\TAI}{\mathrm{TAI}}
\newcommand{\TT}{\mathrm{TT}}
\newcommand{\TDB}{\mathrm{TDB}}
\newcommand{\JD}{\mathrm{JD}}
\newcommand{\MJD}{\mathrm{MJD}}
\newcommand{\EoT}{\mathrm{EoT}}
\newcommand{\SNR}{\mathrm{SNR}}
\newcommand{\RON}{\mathrm{RON}}

% Helper commands for specific diagrams
\newcommand{\midlinelabel}[3]{
    \node (midlabel) at ($ (#1)!.5!(#2) $) {#3};
    \draw[stealth-] (#1) --  (midlabel);
    \draw[-stealth] (midlabel) -- (#2);
}
\newcommand{\midlinelabell}[3]{
    \node[fill = white, inner sep = 0.2pt, outer sep=3pt] (midlabel) at ($ (#1)!.5!(#2) $) {#3};
    \draw[stealth-] (#1) --  (midlabel);
    \draw[-stealth] (midlabel) -- (#2);
}
\newcommand{\midlinelabelll}[3]{
    \node[fill = white, inner sep = 0.2pt, outer sep=3pt,scale=0.6] (midlabel) at ($ (#1)!.5!(#2) $) {#3};
    \draw[stealth-] (#1) --  (midlabel);
    \draw[-stealth] (midlabel) -- (#2);
}

__EXTRA_PREAMBLE__

\begin{document}
__TIKZ_CODE__
\end{document}
"""

os.makedirs("fig_sources", exist_ok=True)
os.makedirs("figs", exist_ok=True)

chapters = [
    "chapters/ch1_time_systems.tex",
    "chapters/ch2_coordinates.tex",
    "chapters/ch3_astrometry.tex",
    "chapters/ch4_photometry.tex",
    "chapters/ch5_angular_resolution.tex",
    "chapters/ch6_two_body.tex",
    "chapters/ch8_interstellar_medium.tex"
]

fig_names = {
    # ch1
    ("ch1_time_systems", 1): "fig_ch1_orbit_sidereal",
    ("ch1_time_systems", 2): "fig_ch1_eot_decomposition",
    # ch2
    ("ch2_coordinates", 1): "fig_ch2_ra_dec_polar_grid",
    ("ch2_coordinates", 2): "fig_ch2_lst_meridian_schematic",
    ("ch2_coordinates", 3): "fig_ch2_lst_meridian_schematic_later",
    ("ch2_coordinates", 4): "fig_ch2_horizontal_coords",
    # ch3
    ("ch3_astrometry", 1): "fig_ch3_parallax_geometry",
    # ch4
    ("ch4_photometry", 1): "fig_ch4_spectral_filters_bands",
    # ch5
    ("ch5_angular_resolution", 1): "fig_ch5_earth_geodetic_vector",
    ("ch5_angular_resolution", 2): "fig_ch5_vlbi_chord_geometry",
    ("ch5_angular_resolution", 3): "fig_ch5_interferometer_two_sources",
    ("ch5_angular_resolution", 4): "fig_ch5_cassegrain_geometry",
    ("ch5_angular_resolution", 5): "fig_ch5_telescope_ray_diagram",
    ("ch5_angular_resolution", 6): "fig_ch5_huygens_superposition_principle",
    ("ch5_angular_resolution", 7): "fig_ch5_n_slit_geometry",
    ("ch5_angular_resolution", 8): "fig_ch5_rayleigh_sparrow_comparison",
    ("ch5_angular_resolution", 9): "fig_ch5_rayleigh_diffraction_sinc",
    # ch6
    ("ch6_two_body", 1): "fig_ch6_orbital_frame_3d",
    ("ch6_two_body", 2): "fig_ch6_conic_sections_geometry",
    ("ch6_two_body", 3): "fig_ch6_vis_viva_geometry",
    ("ch6_two_body", 4): "fig_ch6_orbital_elements_3d",
    ("ch6_two_body", 5): "fig_ch6_effective_potential_well",
    ("ch6_two_body", 6): "fig_ch6_hohmann_transfer_ellipse",
    ("ch6_two_body", 7): "fig_ch6_sb2_schematic",
    ("ch6_two_body", 8): "fig_ch6_sb2_rvcurve",
    ("ch6_two_body", 9): "fig_ch6_slingshot_classic",
    # ch8
    ("ch8_interstellar_medium", 1): "fig_ch8_line_profile_voigt",
    ("ch8_interstellar_medium", 2): "fig_ch8_expanding_shell_geometry",
}

for ch_path in chapters:
    ch_base = os.path.splitext(os.path.basename(ch_path))[0]
    with open(ch_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pos = 0
    idx = 1
    
    while True:
        start = content.find(r"\begin{tikzpicture}", pos)
        if start == -1:
            break
        end = content.find(r"\end{tikzpicture}", start)
        if end == -1:
            break
        end += len(r"\end{tikzpicture}")
        
        fig_key = (ch_base, idx)
        figname = fig_names.get(fig_key, f"fig_{ch_base}_{idx}")
        tikz_code = content[start:end]
        
        extra_preamble = ""
        preceding_text = content[max(0, start-200):start]
        tdplot_match = re.search(r'(\\tdplotsetmaincoords\{[^}]+\}\{[^}]+\})', preceding_text)
        if tdplot_match:
            extra_preamble = tdplot_match.group(1)
        
        standalone_tex = STANDALONE_TEMPLATE.replace("__EXTRA_PREAMBLE__", extra_preamble).replace("__TIKZ_CODE__", (extra_preamble + "\n" if extra_preamble else "") + tikz_code)
        
        tex_path = os.path.join("fig_sources", f"{figname}.tex")
        with open(tex_path, "w", encoding="utf-8") as f_out:
            f_out.write(standalone_tex)
        
        print(f"Generated standalone: {tex_path}")
        idx += 1
        pos = end

print("All standalone tex files written.")

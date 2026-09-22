import os
import glob
import re

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

chapters = [
    "chapters/ch1_time_systems.tex",
    "chapters/ch2_coordinates.tex",
    "chapters/ch3_astrometry.tex",
    "chapters/ch4_photometry.tex",
    "chapters/ch5_angular_resolution.tex",
    "chapters/ch6_two_body.tex",
    "chapters/ch8_interstellar_medium.tex"
]

for ch_path in chapters:
    ch_base = os.path.splitext(os.path.basename(ch_path))[0]
    with open(ch_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    pos = 0
    idx = 1
    new_pieces = []
    last_end = 0
    
    while True:
        start = content.find(r"\begin{tikzpicture}", pos)
        if start == -1:
            new_pieces.append(content[last_end:])
            break
        end = content.find(r"\end{tikzpicture}", start)
        if end == -1:
            new_pieces.append(content[last_end:])
            break
        end += len(r"\end{tikzpicture}")
        
        fig_key = (ch_base, idx)
        figname = fig_names[fig_key]
        
        # Keep everything before the tikzpicture
        new_pieces.append(content[last_end:start])
        
        # Replacement code: \includegraphics{figs/figname.pdf}
        # or \includegraphics{figname.pdf} (since \graphicspath{{figs/}} is loaded in preamble)
        # Using figs/figname.pdf ensures both direct and graphicspath resolution work seamlessly
        new_pieces.append(f"\\includegraphics{{{figname}.pdf}}")
        
        last_end = end
        pos = end
        idx += 1
    
    new_content = "".join(new_pieces)
    # Also clean up any leftover \usetikzlibrary or local helper macros if they were just before the figure and now unused
    # (e.g., in ch6 lines 698-713 where \midlinelabel was defined before tikzpicture)
    if ch_base == "ch6_two_body":
        # Remove leftover \tdplotsetmaincoords right before \resizebox if redundant, or leave it
        pass
    
    with open(ch_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"Updated {ch_path} with {idx-1} standalone figure inclusions.")

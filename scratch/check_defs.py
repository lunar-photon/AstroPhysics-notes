import os
import glob
import re

files = sorted(glob.glob("chapters/*.tex"))

for fn in files:
    with open(fn, "r", encoding="utf-8") as f:
        text = f.read()
    
    # search for \newcommand or \def before \begin{tikzpicture}
    matches = re.finditer(r'(\\begin\{figure\}.*?\\end\{figure\})', text, re.DOTALL)
    for m in matches:
        block = m.group(1)
        if r'\begin{tikzpicture}' in block:
            # check for \newcommand or \def outside \begin{tikzpicture}
            outside_tikz = re.sub(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}', '', block, flags=re.DOTALL)
            defs = re.findall(r'(\\(?:newcommand|def|renewcommand)\\[a-zA-Z]+(?:\[[^\]]*\])?\{[^}]*\})', outside_tikz)
            if defs:
                print(f"File {fn} has definitions inside figure environment:")
                for d in defs:
                    print("  ", d)

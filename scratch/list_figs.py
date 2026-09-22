import os
import glob
import re

files = sorted(glob.glob("chapters/*.tex"))
all_figs = []

for fn in files:
    with open(fn, "r", encoding="utf-8") as f:
        text = f.read()
    
    pos = 0
    fig_idx = 1
    while True:
        start = text.find(r"\begin{tikzpicture}", pos)
        if start == -1:
            break
        end = text.find(r"\end{tikzpicture}", start)
        if end == -1:
            break
        end += len(r"\end{tikzpicture}")
        
        tikz_code = text[start:end]
        
        before = text[max(0, start-500):start]
        after = text[end:min(len(text), end+500)]
        
        label_match = re.search(r"\\label\{([^}]+)\}", after) or re.search(r"\\label\{([^}]+)\}", before)
        label = label_match.group(1) if label_match else f"{os.path.splitext(os.path.basename(fn))[0]}_fig{fig_idx}"
        
        caption_match = re.search(r"\\caption\{([^}]+)\}", after) or re.search(r"\\caption\{([^}]+)\}", before)
        caption = caption_match.group(1) if caption_match else ""
        
        all_figs.append({
            "file": fn,
            "chapter": os.path.splitext(os.path.basename(fn))[0],
            "idx": fig_idx,
            "label": label,
            "start": start,
            "end": end,
            "code": tikz_code,
            "caption": caption[:60]
        })
        fig_idx += 1
        pos = end

print(f"Total figures found: {len(all_figs)}")
for fig in all_figs:
    chap = fig["chapter"]
    idx = fig["idx"]
    lbl = fig["label"]
    clen = len(fig["code"])
    print(f"{chap} #{idx} | label: {lbl} | len: {clen}")

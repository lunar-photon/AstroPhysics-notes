import os
import glob
import re

files = sorted(glob.glob("chapters/*.tex"))
fig_num = 0

for fn in files:
    with open(fn, "r", encoding="utf-8") as f:
        content = f.read()
    
    pos = 0
    while True:
        start = content.find(r"\begin{tikzpicture}", pos)
        if start == -1:
            break
        end = content.find(r"\end{tikzpicture}", start)
        if end == -1:
            break
        end += len(r"\end{tikzpicture}")
        
        fig_num += 1
        code = content[start:end]
        
        # inspect 200 chars before and after
        before = content[max(0, start-200):start]
        after = content[end:min(len(content), end+200)]
        
        print(f"=== FIG #{fig_num} in {os.path.basename(fn)} ===")
        print("BEFORE:\n", before.strip()[-100:])
        print("FIRST 3 LINES:\n", "\n".join(code.splitlines()[:3]))
        print("LAST 2 LINES:\n", "\n".join(code.splitlines()[-2:]))
        print("AFTER:\n", after.strip()[:100])
        print("="*40)
        
        pos = end

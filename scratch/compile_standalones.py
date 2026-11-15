import os
import glob
import subprocess
from concurrent.futures import ThreadPoolExecutor

os.makedirs("figs", exist_ok=True)
tex_files = sorted(glob.glob("fig_sources/*.tex"))

def compile_fig(tex_file):
    base = os.path.splitext(os.path.basename(tex_file))[0]
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory=figs",
        tex_file
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    pdf_path = os.path.join("figs", f"{base}.pdf")
    success = (res.returncode == 0) and os.path.exists(pdf_path) and (os.path.getsize(pdf_path) > 0)
    return base, success, res.stdout

print(f"Compiling {len(tex_files)} standalone figures...")
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(compile_fig, tex_files))

failed = []
for base, success, stdout in results:
    if success:
        pdf_path = os.path.join("figs", f"{base}.pdf")
        sz = os.path.getsize(pdf_path)
        print(f"✓ {base}.pdf ({sz} bytes)")
    else:
        print(f"✗ FAILED: {base}")
        # print last 15 lines of log
        lines = stdout.splitlines()
        print("\n".join(lines[-20:]))
        failed.append(base)

if failed:
    print(f"\n{len(failed)} figures failed to compile!")
    exit(1)
else:
    print("\nAll 28 standalone figures compiled successfully to figs/!")

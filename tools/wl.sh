#!/usr/bin/env bash
# Run one Wolfram Language script (.wls) for SYMBOLIC work only (no numerics: those are Python on the cluster) on the laptop (owner's standing exception to the
# cluster-only rule, 2026-10-10: the cluster has no usable Wolfram licence). Everything else still goes through
# tools/run.sh / tools/rr.sh on the cluster.
#
# Usage (from the project root):   tools/wl.sh code/t01_reference.wls [args...]
# Options via environment:   WL_TIMEOUT=600   seconds before the job is stopped (default 10 min: symbolic simplification should not take longer)
#                            WL_NICE=10       niceness (default 10, so the laptop stays usable)
#                            WL_SLOTS=3       kernels allowed at once (1 to 3; callers beyond that queue)
#                            WL=<path>        wolframscript binary (default: PATH, then the standard install)
#
# The script reads and writes paths relative to the project root, exactly like the Python scripts:
#   Export["results/tNN.m", expr] / Get["data/x.m"] / Export["figures/x.pdf", plot].
# Console output goes to build/runs/<name>.out (the tail is echoed); each run is logged in logs/runtimes.tsv
# (date, script, elapsed s, exit) and in logs/runs.log, like the cluster runs.
set -u
cd "$(dirname "$0")/.." || exit 2
if [ "${1:-}" = "-s" ]; then
  # session: tools/wl.sh -s <name> '<expr>'  -- evaluates <expr> with everything defined earlier in the same session
  # One session per flow (a derivation whose steps build on each other), named after it.
  # (state kept in build/sessions/<name>.mx; each call is a fresh kernel, so none lingers), prints the result, and appends
  # In/Out to build/sessions/<name>.log.  tools/wl.sh -s <name> --end  closes the session (state deleted, log kept).
  name="${2:-}"; [ -n "$name" ] && [ -n "${3:-}" ] || { echo "usage: tools/wl.sh -s <name> '<expr>' | --end"; exit 2; }
  mkdir -p build/sessions; mx="build/sessions/$name.mx"; lg="build/sessions/$name.log"
  if [ "$3" = "--end" ]; then rm -f "$mx"; echo "[wl] session $name closed; log: $lg"; exit 0; fi
  script="build/sessions/$name.call.wls"
  printf 'If[FileExistsQ["%s"], Get["%s"]];\nwlSession$out = (\n%s\n);\nPrint[ToString[wlSession$out, InputForm]];\nDumpSave["%s", "Global`"];\n' "$mx" "$mx" "$3" "$mx" > "$script"
  printf 'In:  %s\n' "$3" >> "$lg"; WL_SESSION_LOG="$lg"; shift 3; WL_TIMEOUT=${WL_TIMEOUT:-120}
elif [ "${1:-}" = "-c" ]; then
  # quick check: tools/wl.sh -c 'Simplify[...]' -- the command is saved as build/runs/quick_<time>.wls (logged like any run)
  # and the value of its last expression is printed; default limit 120 s. Anything the text cites as a check goes in a script.
  [ -n "${2:-}" ] || { echo "usage: tools/wl.sh -c '<Wolfram expression>'"; exit 2; }
  mkdir -p build/runs; script="build/runs/quick_$(date +%Y%m%d_%H%M%S)_$$.wls"
  printf 'Print[ToString[(\n%s\n), InputForm]]\n' "$2" > "$script"; shift 2; WL_TIMEOUT=${WL_TIMEOUT:-120}
else
  script="${1:-}"; shift || true
fi
[ -f "$script" ] || { echo "no such script: $script"; exit 2; }
case "$script" in *.wls|*.wl) ;; *) echo "wl.sh runs Wolfram scripts (.wls) only; Python goes through tools/run.sh"; exit 2 ;; esac
WL=${WL:-$(command -v wolframscript || true)}
[ -n "$WL" ] || for p in /usr/local/Wolfram/Wolfram/*/Executables/wolframscript /usr/local/Wolfram/WolframEngine/*/Executables/wolframscript; do
  [ -x "$p" ] && WL=$p; done
[ -n "$WL" ] && [ -x "$WL" ] || { echo "[wl] wolframscript not found: set WL=/path/to/wolframscript"; exit 2; }
n=$(basename "$script"); n=${n%.*}
mkdir -p build/runs logs results data figures
o=build/runs/$n.out
t0=$(date +%s)
echo "[wl] laptop (nice ${WL_NICE:-10}, limit ${WL_TIMEOUT:-600}s): $script"
# at most WL_SLOTS Wolfram kernels at once (default 3; owner, 2026-10-11: the licence has no kernel limit, the
# laptop has 14 cores): each run holds one of the slot locks build/.wl.lock.N, further callers wait for a free slot;
# the time limit applies to the run itself, not to the wait
slots=${WL_SLOTS:-3}; [ "$slots" -gt 3 ] && slots=3
while :; do
  for i in $(seq 0 $((slots - 1))); do
    exec 9> "build/.wl.lock.$i"
    flock -n 9 && break 2
    exec 9>&-
  done
  sleep 2
done
t0=$(date +%s)
nice -n "${WL_NICE:-10}" timeout "${WL_TIMEOUT:-600}" "$WL" -file "$script" "$@" > "$o" 2>&1; rc=$?
exec 9>&-
el=$(( $(date +%s) - t0 ))
[ "$rc" = 124 ] && echo "[wl] stopped after ${WL_TIMEOUT:-600}s (raise WL_TIMEOUT only after telling the owner)"
printf '%s\t%s\t%s\t%s\n' "$(date '+%F %T')" "$script" "$el" "$rc" >> logs/runtimes.tsv
echo "$(date '+%F %T') wl $script $* exit=$rc ${el}s" >> logs/runs.log
tail -n 40 "$o"
if [ -n "${WL_SESSION_LOG:-}" ]; then { printf 'Out: '; /usr/bin/grep -v '^\[wl\]' "$o"; echo; } >> "$WL_SESSION_LOG"; fi
echo "[wl] finished (exit $rc, ${el}s); output: $o"
exit "$rc"

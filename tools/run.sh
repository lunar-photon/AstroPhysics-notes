#!/usr/bin/env bash
# Run one of the notes' scripts on the IISER TVM cluster (so the laptop stays cool),
# then copy its figures/results/cached data back. Falls back to a low-priority local run
# if the cluster cannot be reached.
#
# Usage (from the Notes directory):   tools/run.sh code/ch08/03_masks.py [args...]
# Options via environment:   RUN_LOCAL=1  force local;   RUN_MIN=30  SLURM time limit in minutes
#                            RUN_CPUS=4   cores;          RUN_MEM=8G  memory
#
# Same code, same seeds (common.rng_for), so the outputs are identical wherever it runs.
set -u
cd "$(dirname "$0")/.." || exit 2
script="$1"; shift || true
[ -f "$script" ] || { echo "no such script: $script"; exit 2; }
HOST=chandra26@padmanabha.iisertvm.ac.in
RDIR=astrophysics_runs/Astro
PY='~/envs/cosmology/bin/python'
# one shared ssh connection for all concurrent runs (many parallel logins get refused)
SSHO="-o BatchMode=yes -o ConnectTimeout=20 -o LogLevel=ERROR -o ControlMaster=auto -o ControlPath=$HOME/.ssh/cm-astro -o ControlPersist=15m"
SSH=(ssh $SSHO "$HOST")
ch=$(echo "$script" | sed -n 's#^code/\(ch[0-9T]*[0-9]*\)/.*#\1#p')

run_local() {
  if [ -f tools/.no_local ]; then   # owner switch: no book code on the laptop at all
    echo "[run] NOT run: the cluster could not be used and laptop runs are paused by the owner (tools/.no_local). Use the cluster (retry later); RUN_LOCAL is disabled too."; exit 3
  fi
  echo "[run] local (nice 19): $script"
  OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 MKL_NUM_THREADS=4 nice -n 19 python3 "$script" "$@"
}

reach() { for t in 1 2 3 4; do timeout 30 "${SSH[@]}" "test -x $PY" 2>/dev/null && return 0; sleep $((t*10)); done; return 1; }
if [ "${RUN_LOCAL:-0}" = 1 ] || ! reach; then
  [ "${RUN_LOCAL:-0}" = 1 ] || echo "[run] cluster unreachable or env missing -> local"
  run_local "$@"; exit $?
fi

# 1. push code and cached inputs (data/ is incremental; results/figures are outputs only)
"${SSH[@]}" "mkdir -p $RDIR/figures $RDIR/results $RDIR/data" 2>/dev/null
rsync -az -e "ssh $SSHO" code "$HOST:$RDIR/" 2>/dev/null
rsync -az -e "ssh $SSHO" data/ "$HOST:$RDIR/data/" 2>/dev/null

# 2. one small SLURM job (never on the login node). If it has not STARTED within RUN_QUEUE_MAX
#    minutes (busy queue), cancel it and run locally at low priority instead.
args=$(printf ' %q' "$@")
tag=$(date +%s%N)
job="cd \$HOME/$RDIR && export SEED_SALT=${SEED_SALT:-} OMP_NUM_THREADS=${RUN_CPUS:-4} OPENBLAS_NUM_THREADS=${RUN_CPUS:-4} MKL_NUM_THREADS=${RUN_CPUS:-4} MPLBACKEND=Agg && $PY $script$args; echo \$? > .done_$tag; sync"
PART=${RUN_PART:-medium}
echo "[run] cluster (sbatch $PART, ${RUN_CPUS:-4} cpus): $script"
jid=$("${SSH[@]}" "sbatch --parsable -p $PART --qos=6node_qos -A iisertvm -c ${RUN_CPUS:-4} --mem=${RUN_MEM:-8G} -t ${RUN_MIN:-30} -J astro_$(basename "$script" .py) -o $RDIR/.slurm_%j.log --wrap $(printf %q "$job")" 2>&1 | tail -1 | tr -cd '0-9')
if [ -z "$jid" ]; then echo "[run] submission failed -> local"; run_local "$@"; exit $?; fi
waited=0; state=PENDING
# Live state from squeue (sacct has returned stale COMPLETED for running jobs). The job is finished
# when its done-marker appears, or when squeue no longer lists it and the marker then shows up.
rc=""
while :; do
  out=$("${SSH[@]}" "cat $RDIR/.done_$tag 2>/dev/null; echo '|'; squeue -h -j $jid -o %T 2>/dev/null; echo END" 2>/dev/null)
  rc=$(printf '%s' "${out%%|*}" | tr -cd '0-9')
  [ -n "$rc" ] && break
  case "$out" in *END*) ;; *) sleep 15; waited=$((waited+15)); continue ;; esac   # ssh hiccup: ask again
  state=$(printf '%s' "${out#*|}" | sed 's/END//' | tr -d ' \n')
  case "$state" in
    PENDING) if [ $waited -ge $(( ${RUN_QUEUE_MAX:-10} * 60 )) ]; then
               "${SSH[@]}" "scancel $jid" 2>/dev/null; echo "[run] job $jid still queued after ${RUN_QUEUE_MAX:-10} min -> cancelled"
               run_local "$@"; exit $?; fi ;;
    "") # left the queue: give the shared filesystem up to 5 min to show the marker
        for i in $(seq 1 30); do
          rc=$("${SSH[@]}" "cat $RDIR/.done_$tag 2>/dev/null" 2>/dev/null | tr -cd '0-9'); [ -n "$rc" ] && break; sleep 10
        done
        break ;;
  esac
  sleep 15; waited=$((waited+15))
done
"${SSH[@]}" "cat $RDIR/.slurm_$jid.log 2>/dev/null; rm -f $RDIR/.slurm_$jid.log $RDIR/.done_$tag" 2>/dev/null
if [ -z "$rc" ]; then
  echo "[run] job $jid ended without its done-marker (killed, timed out or out of memory): see the log above. Nothing copied back."; exit 1
fi

# 3. pull outputs back (only this chapter's outputs, plus any cached data it wrote)
if [ -n "${SEED_SALT:-}" ]; then
  # seed test: outputs went to build/seedtest_<salt>/; never touch the book's results, figures or data
  mkdir -p "build/seedtest_$SEED_SALT"
  rsync -az -e "ssh $SSHO" "$HOST:$RDIR/build/seedtest_$SEED_SALT/" "build/seedtest_$SEED_SALT/" 2>/dev/null
  echo "[run] job $jid finished (exit $rc); seed-test outputs copied to build/seedtest_$SEED_SALT"
  exit "${rc:-1}"
elif [ -n "$ch" ]; then
  mkdir -p "figures/$ch" "results/$ch" "data/$ch"
  rsync -azu -e "ssh $SSHO" "$HOST:$RDIR/figures/$ch/" "figures/$ch/" 2>/dev/null
  rsync -azu -e "ssh $SSHO" "$HOST:$RDIR/results/$ch/" "results/$ch/" 2>/dev/null
  rsync -azu -e "ssh $SSHO" "$HOST:$RDIR/data/$ch/" "data/$ch/" 2>/dev/null
else
  rsync -azu -e "ssh $SSHO" "$HOST:$RDIR/figures/" figures/ 2>/dev/null
  rsync -azu -e "ssh $SSHO" "$HOST:$RDIR/results/" results/ 2>/dev/null
fi
echo "[run] job $jid finished (exit $rc); outputs copied back"
exit "${rc:-1}"

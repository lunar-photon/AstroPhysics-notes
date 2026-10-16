#!/usr/bin/env bash
# Limit watchdog. Its only job is to wake Claude at the moment a usage limit resets.
#
# Claude starts it as a background command (Bash run_in_background). It watches this project's
# session transcripts (main session and subagents). When a usage-limit error appears, it reads the
# exact reset moment that the error carries ("quotaLimits":{"resetsAt":<unix time>}), waits until
# the wall clock reaches that moment, and exits. The exit is what wakes Claude.
#
# It does not poll on an hourly schedule and does not sleep for a fixed number of minutes. It waits
# for an absolute time, checking the wall clock in short steps so a laptop suspend cannot delay it.
#
# Usage:   tools/limit_watchdog.sh [transcript_dir]
# Env:     WD_MARGIN=20   seconds after resetsAt before waking (the limit must really be lifted)
#          WD_TICK=5      seconds between transcript checks when inotifywait is not installed
set -u
DIR=${1:-$HOME/.claude/projects/-home-lunarphoton-Downloads-Astrophysics-Kepler-Notes-Astro}
MARGIN=${WD_MARGIN:-20}
TICK=${WD_TICK:-5}
cd "$(dirname "$0")/.." || exit 2
PIDF=tools/.limit_watchdog.pid
STATE=$(mktemp -d)                       # per-file byte offsets, so each line is read once
trap 'rm -rf "$STATE"; [ "$(cat $PIDF 2>/dev/null)" = "$$" ] && rm -f $PIDF' EXIT

# one watchdog per project: a second copy exits at once
if [ -f $PIDF ] && kill -0 "$(cat $PIDF)" 2>/dev/null; then
  echo "WATCHDOG_ALREADY_RUNNING pid $(cat $PIDF)"; exit 0
fi
echo $$ > $PIDF
command -v jq >/dev/null || { echo "WATCHDOG_ERROR jq not found"; exit 2; }

key() { printf '%s' "$1" | md5sum | cut -c1-16; }

# Print "resetsAt type" for every usage-limit error in the given text. Only real error entries
# count: top-level "isApiErrorMessage": true and "error": "rate_limit". Text that merely quotes
# such an entry (a tool result, a message) is a string inside another entry, so it never matches.
limits_in() {   # each input line is parsed on its own, so a cut or partial line is just skipped
  jq -rR 'fromjson? | select(type=="object" and .isApiErrorMessage==true and .error=="rate_limit")
          | [(.quotaLimits.resetsAt // empty), (.quotaLimits.rateLimitType // "unknown")] | @tsv' \
     2>/dev/null
}

best_reset=0; best_type=""; best_file=""
note() {  # keep the latest reset moment seen (a later limit, e.g. weekly, wins)
  local at=$1 ty=$2 f=$3
  if [ "$at" -gt "$best_reset" ]; then best_reset=$at; best_type=$ty; best_file=$f; fi
}

# Read only the bytes appended to each transcript since the last look.
scan_new() {
  local f k off size
  while IFS= read -r -d '' f; do
    k="$STATE/$(key "$f")"; off=$(cat "$k" 2>/dev/null || echo 0)
    size=$(stat -c %s "$f" 2>/dev/null || echo 0)
    [ "$size" -lt "$off" ] && off=0            # file was replaced
    if [ "$size" -gt "$off" ]; then
      # take only complete lines; a line still being written is read on the next look
      tail -c +"$((off+1))" "$f" | head -c "$((size-off))" > "$STATE/chunk"
      partial=0
      [ "$(tail -c1 "$STATE/chunk" | od -An -c | tr -d ' ')" != '\n' ] && partial=$(tail -n1 "$STATE/chunk" | wc -c)
      done_bytes=$((size - off - partial))
      while IFS=$'\t' read -r at ty; do
        [ -n "$at" ] && note "$at" "$ty" "$f"
      done < <(head -c "$done_bytes" "$STATE/chunk" | limits_in)
      echo "$((off + done_bytes))" > "$k"
    fi
  done < <(find "$DIR" -name '*.jsonl' -type f -print0 2>/dev/null)
}

# Start: a limit that is already active (hit just before the watchdog started) counts too.
# Older errors, whose reset is already past, are ignored.
now=$(date +%s)
while IFS= read -r -d '' f; do
  while IFS=$'\t' read -r at ty; do
    [ -n "$at" ] && [ "$at" -gt "$now" ] && note "$at" "$ty" "$f"
  done < <(tail -c 200000 "$f" | limits_in)
  stat -c %s "$f" > "$STATE/$(key "$f")"
done < <(find "$DIR" -name '*.jsonl' -type f -mmin -720 -print0 2>/dev/null)
while IFS= read -r -d '' f; do
  [ -f "$STATE/$(key "$f")" ] || stat -c %s "$f" > "$STATE/$(key "$f")"
done < <(find "$DIR" -name '*.jsonl' -type f -print0 2>/dev/null)

echo "WATCHDOG_STARTED pid $$, watching $DIR ($(command -v inotifywait >/dev/null && echo 'file events' || echo "size check every ${TICK}s"))"

# 1. Wait for a limit error to appear.
while [ "$best_reset" -le "$(date +%s)" ]; do
  best_reset=0
  if command -v inotifywait >/dev/null; then
    inotifywait -qq -r -e modify -e create --include '\.jsonl$' -t 600 "$DIR" 2>/dev/null
  else
    sleep "$TICK"
  fi
  scan_new
done
fire=$((best_reset + MARGIN))
echo "LIMIT_HIT type=$best_type resets=$(date -d @"$best_reset" '+%F %T %Z') wake=$(date -d @"$fire" '+%F %T %Z') source=${best_file##*/}"

# 2. Wait until the wall clock reaches the reset moment. Short steps, so a suspend cannot
#    push the wake-up late, and so a later limit reported meanwhile extends the target.
while :; do
  now=$(date +%s)
  [ "$now" -ge "$fire" ] && break
  left=$((fire - now)); sleep $(( left < 15 ? left : 15 ))
  scan_new
  if [ $((best_reset + MARGIN)) -gt "$fire" ]; then
    fire=$((best_reset + MARGIN))
    echo "LIMIT_EXTENDED type=$best_type wake=$(date -d @"$fire" '+%F %T %Z')"
  fi
done
echo "LIMIT_RESET at $(date '+%F %T %Z'): the usage limit has reset. Read WORKING.md and resume."
exit 0

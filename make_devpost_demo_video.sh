#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
out="$root/devpost-demo-output"
tts="${TTS_BIN:-$(command -v edge-tts || true)}"
ffmpeg="${FFMPEG_BIN:-$(command -v ffmpeg || true)}"
ffprobe="${FFPROBE_BIN:-$(command -v ffprobe || true)}"
font="${FONT_FILE:-/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf}"
voice="${VOICE:-en-US-AvaMultilingualNeural}"
durations=(14 15 16 16 16 16 15 14)

for executable in "$tts" "$ffmpeg" "$ffprobe"; do
  test -n "$executable" && test -x "$executable" || {
    echo "missing required executable; install edge-tts and ffmpeg or set TTS_BIN/FFMPEG_BIN/FFPROBE_BIN" >&2
    exit 1
  }
done
test -f "$font" || { echo "missing font: $font (override with FONT_FILE)" >&2; exit 1; }

mkdir -p "$out/frames" "$out/audio"
rm -f "$out/frames/concat.txt" "$out/audio/concat.txt"

scene() {
  local number="$1" kicker="$2" title="$3" body="$4" footer="$5"
  convert -size 1920x1080 xc:'#07111f' \
    -fill '#55d6be' -draw 'rectangle 0,0 1920,14' \
    -fill '#55d6be' -font "$font" -pointsize 30 -annotate +108+100 "$kicker" \
    -fill '#f4f8fb' -font "$font" -pointsize 58 -annotate +108+205 "$title" \
    -fill '#102238' -stroke '#28435f' -strokewidth 2 \
    -draw 'roundrectangle 92,270 1828,890 28,28' \
    -stroke none -fill '#d9f7f1' -font "$font" -pointsize 32 \
    -interline-spacing 16 -annotate +145+355 "$body" \
    -fill '#9eb3c8' -font "$font" -pointsize 25 -annotate +108+1015 "$footer" \
    "$out/frames/scene-$number.png"
}

scene 01 'COCKROACHDB x AWS · AGENTIC MEMORY' 'Opportunity Memory Agent' \
  'A durable operations agent for long-running work

Remember every deadline, review, blocker, and next action.' \
  'Open source · Auditable · Evidence grounded'

scene 02 'THE PROBLEM' 'Long-running agents lose operational context' \
  'Organizer replies arrive across many platforms
Deadlines and review states keep changing
Stateless assistants repeat work or miss follow-ups
Simulated results can be mistaken for real progress' \
  'The missing primitive is durable decision memory'

scene 03 'COCKROACHDB MEMORY' 'Append events; never overwrite history' \
  'CREATED      initial facts and deadline
REVIEW       organizer decisions
PROGRESS     completed evidence
BLOCKER      explicit human or technical boundary
SUBMISSION   verified delivery state

The complete timeline survives service restarts.' \
  'CockroachDB is the system of record'

scene 04 'DETERMINISTIC PRIORITY' 'Act on what is urgent and executable' \
  'Opportunity A   $5,000 · due in 7 days
Opportunity B     $250 · due tomorrow

Ranking combines deadline pressure,
status, confidence, and blocker state.

Result: B becomes the next action.' \
  'High reward alone does not control the queue'

scene 05 'HUMAN BOUNDARIES' 'Automation stops at accountable decisions' \
  'Automated:
  read status · run tests · prepare evidence

Human required:
  identity · legal terms · payments · verification

Boundaries become explicit blocker events.' \
  'Safe automation is measurable automation'

scene 06 'GROUNDED GEMINI BRIEF' 'Generation is bounded by stored facts' \
  'Gemini receives only the ten highest-ranked records.

The system prompt forbids invented:
  eligibility · progress · rewards

Missing evidence stays visibly unknown.' \
  'Useful synthesis without fictional status'

scene 07 'REPRODUCIBLE DELIVERY' 'Local proof and an AWS deployment path' \
  'docker compose up --build
python scripts/seed_demo.py
pytest

CockroachDB persistence
AWS App Runner source configuration
Python 3.11 and 3.12 CI
MIT license' \
  'Cloud claims remain pending until independently verified'

scene 08 'OPPORTUNITY MEMORY AGENT' 'Remember why the agent acts' \
  'Persistent memory
Explainable ranking
Grounded generation
Explicit human handoffs

github.com/ILoveBuns/opportunity-memory-agent' \
  'CockroachDB x AWS Agentic Memory'

for number in $(seq 1 8); do
  index="$(printf '%02d' "$number")"
  duration="${durations[$((number - 1))]}"
  "$tts" --voice "$voice" --rate='+5%' \
    --file "$root/devpost_demo_narration/$index.txt" \
    --write-media "$out/audio/raw-$index.mp3"
  "$ffmpeg" -y -v error -i "$out/audio/raw-$index.mp3" \
    -af "loudnorm=I=-16:TP=-1.5:LRA=11,apad=pad_dur=$duration,atrim=duration=$duration" \
    -ar 48000 -ac 2 "$out/audio/scene-$index.wav"
  printf "file 'scene-%s.png'\nduration %s\n" "$index" "$duration" >> "$out/frames/concat.txt"
  printf "file 'scene-%s.wav'\n" "$index" >> "$out/audio/concat.txt"
done
printf "file 'scene-08.png'\n" >> "$out/frames/concat.txt"

"$ffmpeg" -y -v error -f concat -safe 0 -i "$out/frames/concat.txt" \
  -vf 'fps=24,format=yuv420p' -c:v libx264 -preset ultrafast -crf 23 "$out/video-only.mp4"
"$ffmpeg" -y -v error -f concat -safe 0 -i "$out/audio/concat.txt" \
  -c:a aac -b:a 160k "$out/narration.m4a"
"$ffmpeg" -y -v error -i "$out/video-only.mp4" -i "$out/narration.m4a" \
  -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k \
  -shortest -movflags +faststart "$out/opportunity-memory-agent-devpost-1080p.mp4"

"$ffprobe" -v error -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$out/opportunity-memory-agent-devpost-1080p.mp4"

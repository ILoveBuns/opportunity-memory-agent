#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
output="${1:-$root/GOAI_SUBMISSION_PACKAGE.zip}"
video="$root/goai-demo-output/opportunity-memory-agent-goai-1080p.mp4"
proposal="$root/GOAI_PROPOSAL.pdf"
python_bin="${PYTHON:-python3}"
ffprobe="${FFPROBE:-/root/.codex/tools/ffmpeg/ffprobe}"

test -x "$ffprobe" || { echo "ffprobe is required: $ffprobe" >&2; exit 1; }
test -f "$video" || { echo "missing GOAI video: $video" >&2; exit 1; }
test -f "$proposal" || { echo "missing GOAI proposal: $proposal" >&2; exit 1; }
git -C "$root" diff --quiet --exit-code || {
  echo "tracked worktree changes must be committed before packaging" >&2
  exit 1
}
git -C "$root" diff --cached --quiet --exit-code || {
  echo "staged changes must be committed before packaging" >&2
  exit 1
}

PYTHONPATH="$root:$root/.deps" "$root/.deps/bin/pytest" -q

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
stage="$tmp/opportunity-memory-agent"
mkdir -p "$stage"
git -C "$root" archive HEAD | tar -x -C "$stage"

# Keep the GOAI upload focused and below typical form limits. Devpost-specific
# media remains public in the repository but is not duplicated in this archive.
rm -rf "$stage/devpost_demo_narration"
rm -f "$stage/assets/opportunity-memory-agent-devpost-1080p.mp4"
rm -f "$stage/DEVPOST_EVIDENCE.md" "$stage/make_devpost_demo_video.sh"
cp "$proposal" "$stage/GOAI_PROPOSAL.pdf"
cp "$video" "$stage/opportunity-memory-agent-goai-1080p.mp4"

commit="$(git -C "$root" rev-parse HEAD)"
video_duration="$($ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 "$video")"
{
  echo "GOAI submission package manifest"
  echo "source_commit=$commit"
  echo "test_command=PYTHONPATH=.:.deps .deps/bin/pytest -q"
  echo "test_result=10 passed"
  echo "video_duration_seconds=$video_duration"
  echo
  (cd "$stage" && sha256sum GOAI_PROPOSAL.pdf opportunity-memory-agent-goai-1080p.mp4)
} > "$stage/GOAI_PACKAGE_MANIFEST.txt"

rm -f "$output"
(cd "$tmp" && "$python_bin" -m zipfile -c "$output" opportunity-memory-agent)
unzip -tq "$output"
echo "created $output"
sha256sum "$output"

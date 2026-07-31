#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
out="$root/goai-demo-output"
tts="/root/.local/bin/edge-tts"
ffmpeg="/root/.codex/tools/ffmpeg/ffmpeg"
ffprobe="/root/.codex/tools/ffmpeg/ffprobe"
font="/root/.local/share/fonts/NotoSansCJKsc-Regular.otf"
mono="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
voice="zh-CN-XiaoxiaoNeural"
durations=(14 16 16 17 17 17 16 15)

for executable in "$tts" "$ffmpeg" "$ffprobe"; do
  test -x "$executable" || { echo "missing executable: $executable" >&2; exit 1; }
done
test -f "$font" || { echo "missing CJK font: $font" >&2; exit 1; }

mkdir -p "$out/frames" "$out/audio"
rm -f "$out/frames/concat.txt" "$out/audio/concat.txt"

scene() {
  local number="$1" kicker="$2" title="$3" body="$4" footer="$5"
  convert -size 1920x1080 xc:'#07111f' \
    -fill '#55d6be' -draw 'rectangle 0,0 1920,14' \
    -fill '#55d6be' -font "$font" -pointsize 30 -annotate +108+100 "$kicker" \
    -fill '#f4f8fb' -font "$font" -pointsize 60 -annotate +108+205 "$title" \
    -fill '#102238' -stroke '#28435f' -strokewidth 2 \
    -draw 'roundrectangle 92,270 1828,890 28,28' \
    -stroke none -fill '#d9f7f1' -font "$font" -pointsize 34 \
    -interline-spacing 16 -annotate +145+355 "$body" \
    -fill '#9eb3c8' -font "$font" -pointsize 25 -annotate +108+1015 "$footer" \
    "$out/frames/scene-$number.png"
}

scene 01 'GOAI 2026 · BOUNDLESS AGENTS' '机会不会消失，记忆不该丢失' \
  'Opportunity Memory Agent

面向跨周、跨平台机会管理的
可审计长期记忆智能体' \
  '开源 · 可复现 · 明确人机边界'

scene 02 '真实问题' '普通智能体会忘记流程状态' \
  '主办方回复散落在不同平台
截止时间与审核状态持续变化
重复报名与重复跟进浪费时间
模拟结果可能被误认成真实成绩

长期任务需要持久、可追溯的事实' \
  '不是更多聊天记录，而是结构化决策记忆'

scene 03 '事件溯源式记忆' '每次变化只追加，不覆盖历史' \
  'CREATED    创建机会与第一条事实
REVIEW     记录主办方审核结果
PROGRESS   保存已完成证据
BLOCKER    明确当前阻塞与下一步
SUBMISSION 关联真实提交状态

CockroachDB 保存完整时间线' \
  '重启服务后，历史与状态仍然存在'

scene 04 '证据优先排序' '可执行的临期任务先行动' \
  '机会 A   奖金 5,000 美元 · 截止 7 天
机会 B   奖金   250 美元 · 截止 1 天

系统综合：
  截止压力 · 当前状态 · 置信度

结果：机会 B 进入队列首位' \
  '高奖金但不可执行的任务不会挤占行动队列'

scene 05 '显式人机边界' '自动化不会偷偷越权' \
  '可以自动：
  读取公开状态 · 运行测试 · 整理材料

必须人工：
  身份验证 · 协议确认 · 付款与验证码

边界本身也成为可追溯的阻塞事件' \
  '安全不是暂停自动化，而是准确界定自动化'

scene 06 '受约束的生成层' 'Gemini 只基于数据库事实生成摘要' \
  '输入范围：已排序的前十条结构化记录

系统约束：
  不虚构资格
  不虚构进展
  不虚构奖励
  缺少证据时明确说未知' \
  '生成能力建立在可核查事实之上'

scene 07 '可复现工程证据' '从本地演示到云端部署' \
  'docker compose up --build
python scripts/seed_demo.py
pytest

6 项自动化测试通过
CockroachDB 持久化
AWS App Runner 部署配置
MIT 开源许可证' \
  '核心流程不依赖 Gemini 密钥也能运行'

scene 08 'OPPORTUNITY MEMORY AGENT' '让长期智能体记住为什么行动' \
  '持久记忆
可解释排序
事实约束
人机协作

github.com/ILoveBuns/opportunity-memory-agent' \
  'GOAI 2026 · Boundless Agents'

for number in $(seq 1 8); do
  index="$(printf '%02d' "$number")"
  duration="${durations[$((number - 1))]}"
  "$tts" --voice "$voice" --rate='+8%' \
    --file "$root/goai_demo_narration/$index.txt" \
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
  -shortest -movflags +faststart "$out/opportunity-memory-agent-goai-1080p.mp4"

"$ffprobe" -v error -show_entries format=duration,size \
  -show_entries stream=index,codec_type,codec_name,width,height \
  -of json "$out/opportunity-memory-agent-goai-1080p.mp4"

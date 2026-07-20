"""Generate the README terminal demo GIF (docs/assets/svgap-demo.gif).

Replays the recorded outputs of real runs on the public reset_release
witness pair (temp paths shortened): the supplied testbench passes, six
intent lines are declared, the same design now fails REF-RDC-001, and the
safe witness passes both checks. Pure Pillow; no capture tooling needed.

Usage: python scripts/gen_readme_demo_gif.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 10)
HAIR = (42, 51, 28)
TEXT = (236, 242, 230)
MUTED = (152, 161, 144)
DIM = (85, 94, 69)
GREEN = (118, 185, 0)
LTGREEN = (168, 217, 92)
GOLD = (229, 179, 60)
RED = (249, 97, 103)

W, H = 900, 372
PAD_X, PAD_Y = 26, 46
LINE_H = 22
FONT_SIZE = 14

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets" / "svgap-demo.gif"

# (color, text); None = clear the screen for the next beat.
# Terminal lines are verbatim from recorded runs; temp paths shortened.
SCRIPT: list[tuple | None] = [
    (DIM, "# an AI-generated candidate, scored the way benchmarks score"),
    (LTGREEN, "$ iverilog -g2012 -o build/sim.vvp design.sv ../tb.sv && vvp build/sim.vvp"),
    (GREEN, "FUNCTIONAL_PASS reset_release count=0"),
    (DIM, "# the benchmark verdict: this candidate is finished"),
    "HOLD",
    None,
    (DIM, "# declare the reset intent the task never carried: six lines"),
    (LTGREEN, "$ svgap check manifest.toml"),
    (MUTED, "candidate   reset-release-unsafe"),
    (GREEN, "functional  pass"),
    (GOLD, "structural  fail        gap member  yes"),
    (RED, "ERROR   REF-RDC-001: raw asynchronous reset reaches an"),
    (RED, "        unmarked state element although synchronous"),
    (RED, "        deassertion is required"),
    (DIM, "# same design, same testbench: now it is evidence"),
    "HOLD",
    None,
    (DIM, "# the safe witness, same interface, same testbench"),
    (LTGREEN, "$ svgap check ../safe/manifest.toml"),
    (GREEN, "functional  pass"),
    (GREEN, "structural  pass"),
    (MUTED, "unknown and tool_error never count as pass"),
    (DIM, "# github.com/shsridhar-beep/svgap : svgap demo replays this"),
    "HOLD",
    "HOLD",
]


def font():
    for path in ("/System/Library/Fonts/Menlo.ttc",
                 "/System/Library/Fonts/Monaco.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"):
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except OSError:
            continue
    return ImageFont.load_default()


def frame(lines: list[tuple]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([4, 4, W - 5, H - 5], radius=12, outline=HAIR, width=2)
    for i, (cx, cy) in enumerate([(24, 22), (44, 22), (64, 22)]):
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5],
                  fill=[RED, GOLD, GREEN][i])
    d.text((W - 24, 22), "svgap demo · replaying recorded runs",
           font=font(), fill=DIM, anchor="rm")
    y = PAD_Y + 14
    f = font()
    for color, text in lines:
        d.text((PAD_X, y), text, font=f, fill=color)
        y += LINE_H
    return img


def main() -> int:
    frames: list[Image.Image] = []
    durations: list[int] = []
    visible: list[tuple] = []
    for item in SCRIPT:
        if item is None:
            visible = []
            continue
        if item == "HOLD":
            frames.append(frame(visible))
            durations.append(1900)
            continue
        visible.append(item)
        frames.append(frame(visible))
        durations.append(650 if item[1].startswith("$") else 260)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUT, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KiB, {len(frames)} frames)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

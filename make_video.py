"""Metinden ücretsiz video üretici.

Kullanım:
    python make_video.py                     # sessiz video
    python make_video.py --voice             # Türkçe sesli anlatım (edge-tts)
    python make_video.py --scenes my.json --out video.mp4
"""
import argparse
import asyncio
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from moviepy import AudioFileClip, ImageClip, concatenate_videoclips

W, H = 1280, 720
FONT_CANDIDATES = [
    "DejaVuSans-Bold.ttf",
    "arialbd.ttf",
    "Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def load_font(size):
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def render_slide(text, path, index, total):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    # dikey gradyan arka plan
    for y in range(H):
        t = y / H
        draw.line([(0, y), (W, y)], fill=(int(20 + 30 * t), int(24 + 40 * t), int(60 + 90 * t)))
    font = load_font(56)
    lines = textwrap.wrap(text, width=32)
    line_h = 76
    y = (H - line_h * len(lines)) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((W - w) / 2, y), line, font=font, fill="white")
        y += line_h
    small = load_font(26)
    draw.text((40, H - 50), f"{index}/{total}", font=small, fill=(180, 190, 220))
    img.save(path)


async def make_voice(text, path, voice):
    import edge_tts
    await edge_tts.Communicate(text, voice).save(str(path))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--scenes", default="scenes.json")
    p.add_argument("--out", default="video.mp4")
    p.add_argument("--voice", action="store_true", help="sesli anlatım ekle")
    p.add_argument("--voice-name", default="tr-TR-AhmetNeural")
    p.add_argument("--default-seconds", type=float, default=3.0)
    args = p.parse_args()

    scenes = json.loads(Path(args.scenes).read_text(encoding="utf-8"))
    tmp = Path("_tmp")
    tmp.mkdir(exist_ok=True)

    clips = []
    for i, scene in enumerate(scenes, 1):
        img_path = tmp / f"slide_{i}.png"
        render_slide(scene["text"], img_path, i, len(scenes))
        duration = scene.get("seconds", args.default_seconds)
        clip = ImageClip(str(img_path))
        if args.voice:
            audio_path = tmp / f"voice_{i}.mp3"
            asyncio.run(make_voice(scene["text"], audio_path, args.voice_name))
            audio = AudioFileClip(str(audio_path))
            clip = clip.with_duration(audio.duration + 0.5).with_audio(audio)
        else:
            clip = clip.with_duration(duration)
        clips.append(clip)

    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(args.out, fps=24, codec="libx264", audio_codec="aac")
    print(f"Hazır: {args.out}")


if __name__ == "__main__":
    main()

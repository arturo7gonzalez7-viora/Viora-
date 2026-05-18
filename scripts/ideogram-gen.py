#!/usr/bin/env python3
"""
Ideogram image generator for OpenClaw.
Usage: python3 ideogram-gen.py --prompt "your prompt" [options]

Outputs image path to stdout for easy integration.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

API_URL = "https://api.ideogram.ai/generate"

ASPECT_RATIOS = [
    "ASPECT_1_1", "ASPECT_16_9", "ASPECT_9_16",
    "ASPECT_4_3", "ASPECT_3_4", "ASPECT_3_2", "ASPECT_2_3",
    "ASPECT_16_10", "ASPECT_10_16"
]

STYLE_TYPES = ["GENERAL", "REALISTIC", "DESIGN", "RENDER_3D", "ANIME"]

MODELS = ["V_2", "V_2_TURBO"]


def generate(prompt, model="V_2", aspect_ratio="ASPECT_1_1", style_type="AUTO",
             magic_prompt="AUTO", negative_prompt=None, count=1, out_dir=None):
    api_key = os.environ.get("IDEOGRAM_API_KEY")
    if not api_key:
        # Try reading from .env file
        env_path = os.path.expanduser("~/.openclaw/.env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("IDEOGRAM_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip("'\"")
                        break
    if not api_key:
        print("Error: IDEOGRAM_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    if out_dir is None:
        out_dir = os.path.expanduser("~/.openclaw/workspace/output/ideogram")
    os.makedirs(out_dir, exist_ok=True)

    image_request = {
        "prompt": prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "magic_prompt_option": magic_prompt,
    }

    if style_type != "AUTO":
        image_request["style_type"] = style_type

    if negative_prompt:
        image_request["negative_prompt"] = negative_prompt

    payload = json.dumps({"image_request": image_request}).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Api-Key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"API error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    paths = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, item in enumerate(result.get("data", [])):
        url = item.get("url")
        if not url:
            continue

        ext = "png"
        filename = f"ideogram_{timestamp}_{i}.{ext}"
        filepath = os.path.join(out_dir, filename)

        img_req = urllib.request.Request(url)
        with urllib.request.urlopen(img_req, timeout=60) as img_resp:
            with open(filepath, "wb") as f:
                f.write(img_resp.read())

        paths.append(filepath)
        # Print metadata
        print(json.dumps({
            "file": filepath,
            "prompt": item.get("prompt", prompt),
            "seed": item.get("seed"),
            "resolution": item.get("resolution"),
            "style": item.get("style_type"),
            "safe": item.get("is_image_safe"),
        }), file=sys.stderr)

    # Print file paths to stdout (one per line) for easy piping
    for p in paths:
        print(p)

    return paths


def main():
    parser = argparse.ArgumentParser(description="Generate images via Ideogram API")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt")
    parser.add_argument("--model", "-m", default="V_2", choices=MODELS,
                        help="Model version (default: V_2)")
    parser.add_argument("--aspect", "-a", default="ASPECT_1_1", choices=ASPECT_RATIOS,
                        help="Aspect ratio (default: ASPECT_1_1)")
    parser.add_argument("--style", "-s", default="AUTO",
                        choices=["AUTO"] + STYLE_TYPES,
                        help="Style type (default: AUTO)")
    parser.add_argument("--magic", default="AUTO", choices=["AUTO", "ON", "OFF"],
                        help="Magic prompt enhancement (default: AUTO)")
    parser.add_argument("--negative", "-n", default=None,
                        help="Negative prompt (things to avoid)")
    parser.add_argument("--out-dir", "-o", default=None,
                        help="Output directory")

    args = parser.parse_args()
    generate(
        prompt=args.prompt,
        model=args.model,
        aspect_ratio=args.aspect,
        style_type=args.style,
        magic_prompt=args.magic,
        negative_prompt=args.negative,
        out_dir=args.out_dir,
    )


if __name__ == "__main__":
    main()

import subprocess, os

RAW = '/root/.openclaw/workspace/casa-mariachi/footage/raw'
OUT = '/root/.openclaw/workspace/casa-mariachi/footage/output'

# Color grade filter - warm, vibrant, sharp
GRADE = "eq=brightness=0.03:saturation=1.4:contrast=1.08,unsharp=5:5:1.0,curves=r='0/0 0.5/0.58 1/1':g='0/0 0.5/0.52 1/1':b='0/0 0.5/0.45 1/1'"

# Step 1: Build the split-screen intro (3 glasses stacked vertically in frame)
print("Building split-screen intro...")
result = subprocess.run([
    'ffmpeg', '-y',
    '-ss', '1', '-t', '2.5', '-i', f'{RAW}/DJI_20260423155352_0126_D.MP4',
    '-ss', '0.5', '-t', '2.5', '-i', f'{RAW}/DJI_20260423155432_0128_D.MP4',
    '-ss', '1', '-t', '2.5', '-i', f'{RAW}/DJI_20260423160026_0140_D.MP4',
    '-filter_complex',
    "[0:v]scale=1080:640," + GRADE + "[top];"
    "[1:v]scale=1080:640," + GRADE + "[mid];"
    "[2:v]scale=1080:640," + GRADE + "[bot];"
    "[top][mid][bot]vstack=inputs=3[stacked];"
    "[stacked]scale=1080:1920,"
    "drawtext=text='Mezcalita Time':fontcolor=white:fontsize=90:"
    "x=(w-text_w)/2:y=h*0.42:"
    "shadowcolor=black:shadowx=3:shadowy=3:"
    "alpha='if(lt(t\\,0.3)\\,t/0.3\\,if(lt(t\\,2.0)\\,1\\,if(lt(t\\,2.5)\\,(2.5-t)/0.5\\,0)))'[vout]",
    '-map', '[vout]',
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
    '-an', f'{OUT}/intro.mp4'
], capture_output=True, text=True)
if result.returncode != 0:
    print("INTRO ERROR:", result.stderr[-2000:])
    exit(1)
print("Intro done!")

# Step 2: Fast-cut clips (2s each, best shots)
clips = [
    ('DJI_20260423155501_0129_D.MP4', '0.5', '2'),
    ('DJI_20260423155527_0130_D.MP4', '0', '2'),
    ('DJI_20260423155610_0133_D.MP4', '0.5', '2'),
    ('DJI_20260423155548_0132_D.MP4', '0.5', '2'),
    ('DJI_20260423155748_0136_D.MP4', '0.5', '2'),
    ('DJI_20260423155810_0137_D.MP4', '0.5', '2'),
    ('DJI_20260423155843_0138_D.MP4', '0.5', '2'),
    ('DJI_20260423155856_0139_D.MP4', '0.5', '2'),
    ('DJI_20260423160026_0140_D.MP4', '0.5', '2.5'),
]

print("Processing fast-cut clips...")
processed = []
for i, (fname, ss, dur) in enumerate(clips):
    out_clip = f'{OUT}/clip_{i:02d}.mp4'
    r = subprocess.run([
        'ffmpeg', '-y',
        '-ss', ss, '-t', dur,
        '-i', f'{RAW}/{fname}',
        '-vf', f'scale=1080:1920,{GRADE}',
        '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-an', out_clip
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  Clip {i+1} ERROR:", r.stderr[-500:])
    else:
        print(f"  Clip {i+1}/{len(clips)} done")
    processed.append(out_clip)

# Step 3: Concatenate
print("Concatenating final reel...")
concat_list = f'{OUT}/concat.txt'
with open(concat_list, 'w') as f:
    f.write(f"file '{OUT}/intro.mp4'\n")
    for p in processed:
        f.write(f"file '{p}'\n")

r = subprocess.run([
    'ffmpeg', '-y',
    '-f', 'concat', '-safe', '0', '-i', concat_list,
    '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    '-an', f'{OUT}/mezcalita_reel_v2.mp4'
], capture_output=True, text=True)

if r.returncode != 0:
    print("CONCAT ERROR:", r.stderr[-2000:])
else:
    size = os.path.getsize(f'{OUT}/mezcalita_reel_v2.mp4') / 1024/1024
    print(f"DONE! {OUT}/mezcalita_reel_v2.mp4 ({size:.1f} MB)")

"""Regenerate checked-in WebP delivery assets; originals remain unchanged.

Run locally with cwebp installed. Cloudflare builds use the committed outputs,
so they do not require an image codec or download dependencies.
"""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'dist' / 'assets'
codec = shutil.which('cwebp')
if not codec:
    raise SystemExit('Install the WebP tools (cwebp) before regenerating images.')

sources = {f'product/{name}.png': (1000, 88) for name in
           ('home', 'questions', 'nutrition', 'ingredients', 'strength', 'weight')}
sources['brand/iphone-duo-star-white-outer-closed-portrait.png'] = (1200, 88)
sources['product/cor-app-icon.png'] = (256, 88)
for name in ('HvjQmDxRBTKIbqDxNzJ0cUAK4fU', 'H8sG3UXknbtlYDaq7sAodIzbnI',
             '7eX4TRQB9ImxpRvIjFUsm5MYYI', 'tMaKfYWjAnAWOIq0SI15iAwub4',
             'O4R9JTspTUUYe3YUs6qsV3HZ09k', 'CgUIeltv0Dq9CmMfit3NI4VHzY',
             '0S91gIGvUFBixLMM13HRQUucNwc', 'gm6Geusoczh1lGedoY46WeMIBZs',
             'RMrVeVtxfeVSJDV0ASPBXMU9U'):
    sources[f'{name}.png'] = (720, 84)
for name in ('ziqnaAZl9BEB8LHz3OJRKFSQHns', '8dpa8kNyDtN8d94QcwTKwrFqDc',
             'OWVbgfPGBp82YqONIRrRoiqZSw'):
    sources[f'{name}.png'] = (180, 84)

manifest = {}
for source, (width, quality) in sources.items():
    destination = Path('optimized') / Path(source).with_suffix('.webp')
    output = ASSETS / destination
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([codec, '-quiet', '-m', '6', '-q', str(quality), '-sharp_yuv',
                    '-resize', str(width), '0', '-metadata', 'none',
                    str(ASSETS / source), '-o', str(output)], check=True)
    manifest[source] = destination.as_posix()
    print(f'{source}: {(ASSETS / source).stat().st_size:,} → {output.stat().st_size:,} bytes')
(ROOT / 'image-variants.json').write_text(json.dumps(manifest, indent=2) + '\n')

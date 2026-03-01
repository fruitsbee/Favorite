import os
import shutil
import re

src_dir = "zip_contents/extracted"
dest_dir = "assets"
os.makedirs(dest_dir, exist_ok=True)

bg = None
middle = None
sprites = []

for root, _, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.png'):
            path = os.path.join(root, file)
            path_lower = path.lower()
            if 'environment' in path_lower:
                if 'back.png' in path_lower: bg = path
                elif 'middle.png' in path_lower: middle = path
            elif 'sprite' in path_lower or 'characters' in path_lower or 'props' in path_lower or 'items' in path_lower:
                if 'idle' in path_lower or '1.png' in path_lower or '-1' in path_lower:
                    sprites.append(path)

# Fallback pattern if none found
if not sprites:
    for root, _, files in os.walk(src_dir):
        sprites.extend([os.path.join(root, f) for f in files if f.endswith('.png')])

sprites = list(set(sprites))
selected_sprites = sprites[:8]

if bg: shutil.copy(bg, os.path.join(dest_dir, 'bg.png'))
if middle: shutil.copy(middle, os.path.join(dest_dir, 'clouds.png'))
for i, sp in enumerate(selected_sprites):
    shutil.copy(sp, os.path.join(dest_dir, f'sprite_{i}.png'))

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = """                <div class="preset-container" id="sprite-presets">\\n                    <!-- High quality Ansimuz sprites -->"""

for i in range(len(selected_sprites)):
    cls = "preset-sprite selected" if i == 0 else "preset-sprite"
    replacement += f'\\n                    <img src="assets/sprite_{i}.png" class="{cls}" onclick="window.selectSprite(this, \\'assets/sprite_{i}.png\\')">'

replacement += f'\\n                </div>\\n                <input type="hidden" id="bm-icon" value="assets/sprite_0.png">'

target_block = re.search(r'<div class="preset-container" id="sprite-presets">.*?<input type="hidden" id="bm-icon".*?>', html, flags=re.DOTALL)
if target_block:
    html = html.replace(target_block.group(0), replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"window\.selectSprite\(firstSprite, '.*?'\);", r"window.selectSprite(firstSprite, 'assets/sprite_0.png');", js)
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()
    
# Extreme CSS safety: Find active game-container logic and replace backgrounds directly
css = re.sub(r"url\('.*?giphy\.gif'\)", "url('assets/bg.png')", css)
css = re.sub(r"url\('data:image/svg\+xml.*?'\)", "url('assets/clouds.png')", css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Assets organized and files updated!")

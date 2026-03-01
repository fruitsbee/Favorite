import os
import shutil

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

if not sprites:
    for root, _, files in os.walk(src_dir):
        sprites.extend([os.path.join(root, f) for f in files if f.endswith('.png')])

sprites = list(set(sprites))
selected_sprites = sprites[:8]

if bg: shutil.copy(bg, os.path.join(dest_dir, 'bg.png'))
if middle: shutil.copy(middle, os.path.join(dest_dir, 'clouds.png'))
for i, sp in enumerate(selected_sprites):
    shutil.copy(sp, os.path.join(dest_dir, f'sprite_{i}.png'))

print("Assets purely organized into assets/ folder.")

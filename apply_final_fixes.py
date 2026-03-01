import os
import re

# 1. Slice the new 3x1 sprite sheet
try:
    from PIL import Image
    src_img = "C:/Users/korya/.gemini/antigravity/brain/c0a55d3a-2492-4f75-82f8-f42b4785486b/cat_bicycle_motorcycle_sprites_1772370127488.png"
    img = Image.open(src_img).convert("RGBA")
    
    # Optional: Make white transparent
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] > 230 and item[1] > 230 and item[2] > 230:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    
    w, h = img.size
    cw = w // 3 # 3x1 grid
    
    for i in range(3):
        box = (i * cw, 0, (i + 1) * cw, h)
        cropped = img.crop(box)
        # remove grid lines/padding
        cropped = cropped.crop((20, 20, cw - 20, h - 20))
        # Save as 16, 17, 18
        cropped.save(f'assets/sprite_{i+16}.png')
    print("Sliced new assets!")
except Exception as e:
    print(f"PIL error: {e}")

# 2. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Add lock asset CSS
lock_css = """
    .draggable-asset.locked {
        border-color: #4CAF50 !important;
        background: rgba(76, 175, 80, 0.1) !important;
    }
    .draggable-asset.locked .sprite-icon {
        pointer-events: none;
    }
    .lock-asset {
        position: absolute;
        top: -8px;
        left: -8px;
        background: #4CAF50;
        color: white;
        border: 2px solid #fff;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        font-size: 14px;
        line-height: 20px;
        text-align: center;
        cursor: pointer;
        display: none;
        z-index: 10;
    }
    .draggable-asset:hover .lock-asset,
    .draggable-asset.locked .lock-asset {
        display: block;
    }
"""
if ".lock-asset" not in css:
    css = css.replace(".delete-asset {", lock_css + "\\n    .delete-asset {")

# Append/Replace Mobile CSS
mobile_css = """
    /* Improved Mobile Layout */
    @media (max-width: 768px) {
        body { overflow-y: auto !important; }
        #game-container {
            display: block !important;
            height: auto !important;
            min-height: 100vh;
        }
        #desktop {
            position: relative;
            height: 60vh;
            width: 100%;
            overflow: hidden;
            border-bottom: 4px solid #fff;
        }
        #sidebar {
            position: relative !important;
            top: 0 !important;
            right: 0 !important;
            width: 100% !important;
            max-height: none !important;
            border: none !important;
            padding: 15px !important;
        }
    }
"""
# Strip old @media (max-width: 768px) if exists
css = re.sub(r'@media \(max-width: 768px\)\s*\{.*?\}(?=\s*(?:\n\}|\n@media|\Z))', '', css, flags=re.DOTALL)
css += mobile_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update index.html for 19 sprites
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

replacement = """                <div class="preset-container" id="sprite-presets">
                    <!-- 19 AI Generated City Pop Objects -->"""

for i in range(19):
    cls = "preset-sprite selected" if i == 0 else "preset-sprite"
    line = f"""
                    <img src="assets/sprite_{i}.png" class="{cls}" onclick="window.selectSprite(this, 'assets/sprite_{i}.png')">"""
    replacement += line

replacement += """
                </div>"""

target_block = re.search(r'<div class="preset-container" id="sprite-presets">.*?</div>', html, flags=re.DOTALL)
if target_block:
    html = html.replace(target_block.group(0), replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied CSS, HTML and Sprite patches!")

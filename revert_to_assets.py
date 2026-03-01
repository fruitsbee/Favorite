import sys
import os

print("Restoring index.html to use simple asset links")
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
replacement = """                <div class="preset-container" id="sprite-presets">
                    <!-- Reliable local pixel art sprites -->
                    <img src="assets/mario.png" class="preset-sprite selected" onclick="window.selectSprite(this, 'assets/mario.png')">
                    <img src="assets/ash.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/ash.png')">
                    <img src="assets/pokeball.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/pokeball.png')">
                    <img src="assets/bulbasaur.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/bulbasaur.png')">
                    <img src="assets/squirtle.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/squirtle.png')">
                    <img src="assets/charmander.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/charmander.png')">
                    <img src="assets/kirby.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/kirby.png')">
                    <img src="assets/snes.png" class="preset-sprite" onclick="window.selectSprite(this, 'assets/snes.png')">
                </div>
                <input type="hidden" id="bm-icon" value="assets/mario.png">"""

target_block = re.search(r'<div class="preset-container" id="sprite-presets">.*?<input type="hidden" id="bm-icon".*?>', html, flags=re.DOTALL)
if target_block:
    html = html.replace(target_block.group(0), replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


print("Restoring script.js")
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()
js = re.sub(r"window\.selectSprite\(firstSprite, '.*?'\);", r"window.selectSprite(firstSprite, 'assets/mario.png');", js)
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Restored!")

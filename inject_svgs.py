import base64
import re

colors = {
    '0': None,
    '1': '#000000',
    'W': '#ffffff',
    'L': '#cbcbcb',
    'D': '#747474',
    'R': '#d95763',
    'G': '#99e550',
    'U': '#5b6ee1',
    'Y': '#fbf236',
    'O': '#df7126',
    'P': '#76428a',
    'N': '#8f563b',
    'M': '#d77bba'
}

RAW_SPRITES = {
    "sword": [
        "0000000000000010",
        "00000000000001L1",
        "0000000000001L10",
        "000000000001L100",
        "00000000001L1000",
        "0011000001L10000",
        "01NN10001L100000",
        "1YNNY101L1000000",
        "01NN111L10000000",
        "001101L100000000",
        "00001L1000000000",
        "0000010000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "potion": [
        "0000000110000000",
        "0000001LL1000000",
        "0000000110000000",
        "0000001RR1000000",
        "000001RRRR100000",
        "00001RRRRRR10000",
        "0001RRWRRRRR1000",
        "0001RWRRRRRR1000",
        "0001RRRRRRRR1000",
        "00001RRRRRR10000",
        "0000011111100000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "coin": [
        "0000001111000000",
        "000001YYYY100000",
        "00001YYWWYY10000",
        "0001YYWYYYYY1000",
        "0001YYWYYYYY1000",
        "0001YYYYYYYY1000",
        "0001YYYYYYYY1000",
        "00001YYYYYY10000",
        "000001YYYY100000",
        "0000001111000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "shield": [
        "0000111111110000",
        "00001LULLLL10000",
        "00001LUULLL10000",
        "00001LUUULL10000",
        "00001LUUULL10000",
        "000001LUUL100000",
        "000001LUUL100000",
        "0000001LL1000000",
        "0000000110000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "heart": [
        "0000011001100000",
        "00001RR11RR10000",
        "0001RWRRRRRR1000",
        "0001RRRRRRRR1000",
        "00001RRRRRR10000",
        "000001RRRR100000",
        "0000001RR1000000",
        "0000000110000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "star": [
        "0000000110000000",
        "0000001YY1000000",
        "000001YYYY100000",
        "00011YYYYYY11000",
        "001YYYYYYYYYY100",
        "0001YYYYYYYY1000",
        "00001YYYYYY10000",
        "00001YY11YY10000",
        "0001YY1001YY1000",
        "0001110000111000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "key": [
        "0000001111000000",
        "000001YYYY100000",
        "00001YYWWYY10000",
        "00001YYYYYY10000",
        "000001YY11000000",
        "0000001YY1000000",
        "0000001YY1000000",
        "0000001YY1100000",
        "0000001YYYY10000",
        "0000000111100000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ],
    "chest": [
        "0000111111110000",
        "0001NNNNNNNN1000",
        "0001NLNLNLNN1000",
        "0001111YY1111000",
        "0001NNN11NNN1000",
        "0001NNNNNNNN1000",
        "0000111111110000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"
    ]
}

def to_svg(sprite_name):
    grid = RAW_SPRITES[sprite_name]
    rects = []
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != '0':
                rects.append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="{colors[char]}"/>')
    svg = f'<svg viewBox="0 0 16 16" width="32" height="32" xmlns="http://www.w3.org/2000/svg">{"".join(rects)}</svg>'
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode('utf-8')).decode('utf-8')

b64_map = {name: to_svg(name) for name in RAW_SPRITES}

html_sprite_block = '                <div class="preset-container" id="sprite-presets">\\n'
first = True
first_b64 = ""
for name, b64 in b64_map.items():
    cls = "preset-sprite selected" if first else "preset-sprite"
    html_sprite_block += f'                    <img src="{b64}" class="{cls}" onclick="window.selectSprite(this, \'{b64}\')">\\n'
    if first:
        first_b64 = b64
        first = False
html_sprite_block += '                </div>\\n'
html_sprite_block += f'                <input type="hidden" id="bm-icon" value="{first_b64}">'

# Rewrite index.html completely bypassing regex issues
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the block strictly from <div class="preset-container"... down to <input type="hidden" id="bm-icon"...">
target_block = re.search(r'<div class="preset-container" id="sprite-presets">.*?<input type="hidden" id="bm-icon".*?>', html, flags=re.DOTALL)
if target_block:
    html = html.replace(target_block.group(0), html_sprite_block)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Rewrite script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"window\.selectSprite\(firstSprite, '.*?'\);", f"window.selectSprite(firstSprite, '{first_b64}');", js)
with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Injected strictly valid SVG base64 strings exactly into HTML and JS!")

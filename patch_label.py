import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_label = r'\.draggable-asset \.label \{[\s\S]*?max-width: 100%;\s*\}'
new_label = """.draggable-asset .label {
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-50%);
        margin-top: 5px;
        background: rgba(0, 0, 0, 0.8);
        color: #fff;
        padding: 4px 6px;
        font-size: 12px;
        border: 2px solid #fff;
        white-space: nowrap;
        width: max-content;
        z-index: 12;
        pointer-events: none;
    }"""

if re.search(old_label, css):
    css = re.sub(old_label, new_label, css)
    with open('style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Patched label CSS!")
else:
    print("Could not find the target CSS block to replace.")

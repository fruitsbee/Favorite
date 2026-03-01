import re

# 1. Fix Rogue CSS
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Completely eliminate any orphaned .delete-asset block that enforces display block
css = re.sub(r'\\n\s*\.delete-asset\s*\{\s*display:\s*block;\s*\}', '', css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. Make script.js use responsive percentages instead of absolute pixels
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix appendBookmarkElement mapping
# Target block starting from `div.setAttribute('data-x'`
old_append_logic = r"div\.setAttribute\('data-x', bm\.x \|\| 0\);\s*div\.setAttribute\('data-y', bm\.y \|\| 0\);\s*div\.style\.transform = `translate\(\$\{bm\.x \|\| 0\}px, \$\{bm\.y \|\| 0\}px\)`;"

new_append_logic = """
    // Use valid responsive percentages, default to center (50%) if invalid/huge pixel values
    let safeX = parseFloat(bm.x) || 50;
    let safeY = parseFloat(bm.y) || 50;
    if (safeX > 100 || safeX < -50) safeX = 50; // Legacy pixel cleanup
    if (safeY > 100 || safeY < -50) safeY = 50;
    
    // Position using percentages so they stick visually relative to the background
    div.style.left = safeX + '%';
    div.style.top = safeY + '%';
    div.style.transform = 'translate(-50%, -50%)'; // Center pivot
    
    div.setAttribute('data-px', safeX);
    div.setAttribute('data-py', safeY);
"""
if re.search(r"div\.setAttribute\('data-x'", js):
    js = re.sub(old_append_logic, new_append_logic, js)

# Fix interact move listener
old_move_listener = r"function dragMoveListener\(event\) \{[\s\S]*?target\.setAttribute\('data-y', y\)\n\s*\}"

new_move_listener = """function dragMoveListener(event) {
    let target = event.target;
    if (target.classList.contains('locked')) return;
    
    let parent = target.parentElement.getBoundingClientRect();
    
    // Get current percent values
    let currentPX = parseFloat(target.getAttribute('data-px')) || 50;
    let currentPY = parseFloat(target.getAttribute('data-py')) || 50;
    
    // Add pixel movement converted to percentage of parent bounds
    let newPX = currentPX + (event.dx / parent.width) * 100;
    let newPY = currentPY + (event.dy / parent.height) * 100;
    
    // Apply new percentage
    target.style.left = newPX + '%';
    target.style.top = newPY + '%';
    
    // Update attribute cache
    target.setAttribute('data-px', newPX);
    target.setAttribute('data-py', newPY);
}"""
if "function dragMoveListener(event) {" in js:
    js = re.sub(old_move_listener, new_move_listener, js)

# Fix interact end listener (saving to GAS)
old_end_listener = r"let x = parseFloat\(target\.getAttribute\('data-x'\)\) \|\| 0;\s*let y = parseFloat\(target\.getAttribute\('data-y'\)\) \|\| 0;"
new_end_listener = """let x = parseFloat(target.getAttribute('data-px')) || 50;
                    let y = parseFloat(target.getAttribute('data-py')) || 50;
                    // Round percentages to 2 decimal places to save space
                    x = Math.round(x * 100) / 100;
                    y = Math.round(y * 100) / 100;"""
js = re.sub(old_end_listener, new_end_listener, js)

# Fix saving new bookmark
old_save_bm = r"let x = 50;\s*let y = 50;"
new_save_bm = "let x = 50;\n    let y = 50; // Percentages"
js = re.sub(old_save_bm, new_save_bm, js)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Applied responsive logic and CSS cleanup!")

import re

# 1. Fix CSS Hanging Bracket
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# The specific hanging bracket before Universal Button Visibility
css = re.sub(r'/\* === Responsive Design \(Mobile & Tablet\) === \*/\s*\}\s*/\* Universal Button Visiblity \*/', 
             r'/* === Responsive Design (Mobile & Tablet) === */\n\n    /* Universal Button Visiblity */', css)
             
# Or more generally if the above didn't match perfectly:
css = css.replace("/* === Responsive Design (Mobile & Tablet) === */\n    \n}\n\n    \n    \n    /* Universal Button Visiblity */", 
                  "/* === Responsive Design (Mobile & Tablet) === */\n\n    /* Universal Button Visiblity */")
                  
# Fallback cleanup of that exact structure
css = re.sub(r'\}\s*/\* Universal Button Visiblity \*/', '/* Universal Button Visiblity */', css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)


# 2. Add Cross-Device Lock Sync via X coordinate encoding
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix parsing of X in appendBookmarkElement
old_parse = r"let safeX = parseFloat\(bm\.x\) \|\| 50;\s*let safeY = parseFloat\(bm\.y\) \|\| 50;\s*if \(safeX > 100 \|\| safeX < -50\) safeX = 50; // Legacy pixel cleanup"
new_parse = """let safeX = parseFloat(bm.x) || 50;
    let safeY = parseFloat(bm.y) || 50;
    let isLockedBackend = false;
    
    // Decode lock state from X coordinate (+1000 means locked)
    if (safeX >= 1000) {
        isLockedBackend = true;
        safeX -= 1000;
    } else if (safeX > 100 || safeX < -50) {
        safeX = 50; // Legacy pixel cleanup
    }
"""
js = re.sub(old_parse, new_parse, js)

# Ensure localState falls back to backend state if no local locked property exists
old_local = r"if \(localState\.locked\) \{"
new_local = "if (localState.locked || isLockedBackend) {"
js = re.sub(old_local, new_local, js)

# Fix toggleLock to also sync to backend
old_toggle = r"localState\.locked = !isLocked;\s*localStorage\.setItem\('state_' \+ id, JSON\.stringify\(localState\)\);"
new_toggle = """localState.locked = !isLocked;
    localStorage.setItem('state_' + id, JSON.stringify(localState));
    
    // Sync to backend
    let currentPX = parseFloat(el.getAttribute('data-px')) || 50;
    let currentPY = parseFloat(el.getAttribute('data-py')) || 50;
    let syncX = localState.locked ? currentPX + 1000 : currentPX; // Encode lock
    gasApiCall({ action: 'saveBookmarkPosition', id: id, x: Math.round(syncX * 100) / 100, y: Math.round(currentPY * 100) / 100 })
        .catch(console.error);
"""
js = re.sub(old_toggle, new_toggle, js)

# Fix interact.js end dragging to preserve lock state if it was locked (even though dragging shouldn't happen if locked, resizes might? or just in case)
old_end = r"let x = parseFloat\(target\.getAttribute\('data-px'\)\) \|\| 50;\s*let y = parseFloat\(target\.getAttribute\('data-py'\)\) \|\| 50;\s*// Round percentages to 2 decimal places to save space\s*x = Math\.round\(x \* 100\) / 100;"
new_end = """let x = parseFloat(target.getAttribute('data-px')) || 50;
                    let y = parseFloat(target.getAttribute('data-py')) || 50;
                    if (target.classList.contains('locked')) {
                        x += 1000; // Preserve lock state
                    }
                    // Round percentages to 2 decimal places to save space
                    x = Math.round(x * 100) / 100;"""
js = re.sub(old_end, new_end, js)

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Applied strict hovering and cross-device sync hacks!")

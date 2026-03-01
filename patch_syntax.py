import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Clean literal '\n' sequences that invalidate CSS rules
css = css.replace(r'\n', '\n')

# 2. Fix the missing comma for hover/locked which also corrupted CSS
css = css.replace(".draggable-asset:hover \n    .draggable-asset.locked", ".draggable-asset:hover, \n    .draggable-asset.locked")

# 3. Strip any old hover lock/delete rules to avoid duplicates
css = re.sub(r'\.draggable-asset:hover \.lock-asset\s*\{\s*display:\s*block;\s*\}', '', css)
css = re.sub(r'\.draggable-asset:hover \.delete-asset\s*\{\s*display:\s*block;\s*\}', '', css)

# 4. Append a clean hover rule at the very end (before Mobile Media query)
hover_rules = """
    /* Universal Button Visiblity */
    .draggable-asset:hover .lock-asset,
    .draggable-asset:hover .delete-asset {
        display: block !important;
    }
"""

# Insert before @media
if "/* Improved Mobile Layout */" in css:
    css = css.replace("/* Improved Mobile Layout */", hover_rules + "\n    /* Improved Mobile Layout */")
else:
    css += hover_rules

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Sanitized style.css!")

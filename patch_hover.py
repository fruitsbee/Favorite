import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the specific hover rules that force display on .locked
old_rule1 = r'\.draggable-asset:hover \.lock-asset,\s*\.draggable-asset\.locked \.lock-asset\s*\{\s*display:\s*block;\s*\}'
new_rule = """.draggable-asset:hover .lock-asset {
        display: block;
    }"""
css = re.sub(old_rule1, new_rule, css)

old_rule2 = r'\.draggable-asset:hover \.delete-asset,\s*\.draggable-asset\.locked \.delete-asset\s*\{\s*display:\s*block;\s*\}'
new_rule2 = """.draggable-asset:hover .delete-asset {
        display: block;
    }"""
css = re.sub(old_rule2, new_rule2, css)

# Make sure delete-asset is only visible on hover in general
old_rule3 = r'\.draggable-asset:hover \.delete-asset\s*\{\s*display:\s*block;\s*\}'
css = re.sub(old_rule3, new_rule2, css)

# Wait, there's a `.delete-asset { display: block; }` hanging at the very end of line 318
old_hanging = r'\.delete-asset\s*\{\s*display:\s*block;\s*\}'
# We should probably remove it.
css = re.sub(old_hanging, '', css)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("CSS updated! Buttons only display on hover.")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the clouds div completely
html = re.sub(r'<div class="clouds"></div>', '', html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
    
print("Clouds removed from HTML!")

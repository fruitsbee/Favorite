import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

menu_btn = '<button type="button" class="nes-btn is-primary mobile-menu-btn" onclick="window.toggleMobileMenu()" style="z-index: 999;">☰</button>'
if 'mobile-menu-btn' not in html:
    html = html.replace('<div id="desktop"></div>', menu_btn + '\\n        <div id="desktop"></div>')

close_btn = '<button type="button" class="nes-btn is-error mobile-close-btn" onclick="window.toggleMobileMenu()">×</button>'
if 'mobile-close-btn' not in html:
    html = html.replace('<div id="sidebar">', '<div id="sidebar">\\n            ' + close_btn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

btn_css = """
    .mobile-menu-btn, .mobile-close-btn {
        display: none;
    }
"""
if '.mobile-menu-btn' not in css:
    css = css.replace('/* === Responsive Design (Mobile & Tablet) === */', btn_css + '\\n    /* === Responsive Design (Mobile & Tablet) === */')

new_mobile_css = """
    /* Improved Mobile Layout */
    @media (max-width: 768px) {
        body { overflow: hidden !important; }
        #game-container {
            display: flex !important;
            height: 100vh !important;
            overflow: hidden !important;
        }
        #desktop {
            position: relative;
            height: 100vh !important;
            width: 100%;
            overflow: hidden;
            border-bottom: none !important;
        }
        .mobile-menu-btn {
            display: block;
            position: absolute;
            top: 20px;
            right: 20px;
            z-index: 100;
            padding: 5px 12px;
            font-size: 20px;
        }
        .mobile-close-btn {
            display: block;
            align-self: flex-end;
            margin-bottom: 10px;
            padding: 2px 8px;
        }
        #sidebar {
            position: fixed !important;
            top: 0 !important;
            right: -350px !important;
            width: 320px !important;
            height: 100vh !important;
            max-height: 100vh !important;
            border-left: 4px solid #fff !important;
            border-top: none !important;
            background: rgba(11, 15, 25, 0.95) !important;
            transition: right 0.3s ease-in-out !important;
            z-index: 1000 !important;
            padding: 15px !important;
            overflow-y: auto !important;
        }
        #sidebar.open {
            right: 0 !important;
        }
    }
"""
css = css.split('/* Improved Mobile Layout */')[0]
css += new_mobile_css

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update script.js
with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

toggle_js = """
// === MOBILE MENU ===
window.toggleMobileMenu = function() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
};
"""
if 'toggleMobileMenu' not in js:
    js += toggle_js

with open('script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Mobile Hamburger Menu applied successfully!")

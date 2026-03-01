import urllib.request
import json
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

os.makedirs('assets', exist_ok=True)

def get_git_tree(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
         with urllib.request.urlopen(req, context=ctx) as r:
             return json.loads(r.read())['tree']
    except Exception as e:
         print("Error:", e)
         return []

tree = get_git_tree("ansimuz", "sunny-land")
pngs = [t['path'] for t in tree if t['path'].endswith('.png')]

if not pngs:
    print("NO PNGS FOUND! Using fallback URLs.")
    fallbacks = {
        "assets/bg.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/environment/back.png",
        "assets/clouds.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/environment/middle.png",
        "assets/sprite_0.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/cherry/cherry-1.png",
        "assets/sprite_1.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/gem/gem-1.png",
        "assets/sprite_2.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/frog/idle/frog-idle-1.png",
        "assets/sprite_3.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/opossum/opossum-1.png",
        "assets/sprite_4.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/eagle/eagle-1.png",
        "assets/sprite_5.png": "https://raw.githubusercontent.com/ansimuz/sunny-land/master/assets/sprites/player/idle/player-idle-1.png",
        "assets/sprite_6.png": "https://raw.githubusercontent.com/ansimuz/getting-started-make-a-game/master/assets/images/sprites/cherry/cherry-1.png",
        "assets/sprite_7.png": "https://raw.githubusercontent.com/ansimuz/getting-started-make-a-game/master/assets/images/sprites/gem/gem-1.png",
    }
    for file, url in fallbacks.items():
        print(f"Downloading {file} from {url}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ctx) as r:
                with open(file, 'wb') as f:
                    f.write(r.read())
        except Exception as e:
            print(f"Error {e}")
    print("Done")
    exit(0)

bg_candidates = [p for p in pngs if 'environment/back.png' in p or 'environment/bg' in p or 'back.png' in p.lower()]
middle_candidates = [p for p in pngs if 'environment/middle.png' in p or 'middle.png' in p]

bg = bg_candidates[0] if bg_candidates else pngs[0]
middle = middle_candidates[0] if middle_candidates else bg

target_sprites = ['cherry', 'gem', 'frog', 'opossum', 'eagle', 'player']
sprites = []
for p in pngs:
    if 'sprites/' in p and any(x in p for x in target_sprites) and ('-1.png' in p or '/1.png' in p):
        sprites.append(p)
        
if len(sprites) < 8:
    sprites.extend([p for p in pngs if 'sprites/' in p and p not in sprites])

dl_map = {}
dl_map["assets/bg.png"] = f"https://raw.githubusercontent.com/ansimuz/sunny-land/master/{bg}"
dl_map["assets/clouds.png"] = f"https://raw.githubusercontent.com/ansimuz/sunny-land/master/{middle}"

for i in range(min(8, len(sprites))):
    dl_map[f"assets/sprite_{i}.png"] = f"https://raw.githubusercontent.com/ansimuz/sunny-land/master/{sprites[i]}"

for local, remote in dl_map.items():
    print(f"Downloading {remote} to {local}")
    try:
        req = urllib.request.Request(remote, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as r:
            with open(local, 'wb') as f:
                f.write(r.read())
    except Exception as e:
        print(f"Failed {remote}: {e}")

print("Downloaded all assets.")

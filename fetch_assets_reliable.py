import urllib.request
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

os.makedirs('assets', exist_ok=True)

def download_file(url, local_path):
    print(f"Downloading {url} to {local_path}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as r:
            with open(local_path, 'wb') as f:
                f.write(r.read())
        return True
    except Exception as e:
        print(f"Failed {url}: {e}")
        return False

# Try passiomatic
urls = {
    "assets/bg.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/environment/back.png",
    "assets/clouds.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/environment/middle.png",
    "assets/sprite_0.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/cherry/cherry-1.png",
    "assets/sprite_1.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/gem/gem-1.png",
    "assets/sprite_2.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/frog/idle/frog-idle-1.png",
    "assets/sprite_3.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/opossum/opossum-1.png",
    "assets/sprite_4.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/eagle/eagle-1.png",
    "assets/sprite_5.png": "https://raw.githubusercontent.com/passiomatic/sunny-land/master/assets/sprites/player/idle/player-idle-1.png"
}

all_success = True
for local, url in urls.items():
    if not download_file(url, local):
        all_success = False

if all_success:
    print("Success via passiomatic")
    exit(0)
    
# Try mstill3
print("Falling back to mstill3 repo...")
urls_mstill = {
    "assets/bg.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Environment/back.png",
    "assets/clouds.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Environment/middle.png",
    "assets/sprite_0.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Items/cherry/cherry-1.png",
    "assets/sprite_1.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Items/gem/gem-1.png",
    "assets/sprite_2.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Enemies/frog/idle/frog-idle-1.png",
    "assets/sprite_3.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Enemies/opossum/opossum-1.png",
    "assets/sprite_4.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Enemies/eagle/eagle-1.png",
    "assets/sprite_5.png": "https://raw.githubusercontent.com/mstill3/SunnyLand/master/Assets/Sprites/Player/idle/player-idle-1.png"
}
for local, url in urls_mstill.items():
    download_file(url, local)

print("Finished attempting downloads.")

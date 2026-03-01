import urllib.request
import zipfile
import os
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://github.com/ansimuz/getting-started-make-a-game/archive/refs/heads/master.zip"
zip_path = "ansimuz.zip"

print(f"Downloading {url}...")
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx) as r:
        with open(zip_path, 'wb') as f:
            f.write(r.read())
            
    print("Unzipping...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall("temp_assets")
    print("Extract successful!")
except Exception as e:
    print(f"Error: {e}")

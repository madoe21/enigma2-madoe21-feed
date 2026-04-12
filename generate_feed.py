import requests
import os

PLUGINS = [
    "enigma2-fakehls-plugin",
    "enigma2-fritzcall",
    "enigma2-fritzhome",
    "enigma2-fritzmon",
    "enigma2-homematic",
    "enigma2-lotto",
    "enigma2-openliga-db",
    "enigma2-spritpreise-checker",
    "enigma2-stocks",
    "enigma2-weather",
    "enigma2-wireguard",
]
GITHUB_USER = "madoe21"  # ggf. anpassen
DOWNLOAD_DIR = "ipks"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_latest_release(user, repo):
    url = f"https://api.github.com/repos/{user}/{repo}/releases/latest"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def download_asset(asset_url, dest):
    r = requests.get(asset_url, stream=True)
    if r.status_code == 200:
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True
    return False

def main():
    for plugin in PLUGINS:
        release = get_latest_release(GITHUB_USER, plugin)
        if not release:
            print(f"No release found for {plugin}")
            continue
        for asset in release.get("assets", []):
            if asset["name"].endswith(".ipk"):
                dest = os.path.join(DOWNLOAD_DIR, asset["name"])
                print(f"Downloading {asset['name']}...")
                if download_asset(asset["browser_download_url"], dest):
                    print(f"Downloaded: {dest}")
                else:
                    print(f"Failed to download {asset['name']}")

if __name__ == "__main__":
    main()

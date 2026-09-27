"""Writes bucket/nib.json for nib's latest release, from its archive's
.sha256 file. Run by .github/workflows/update.yml; `python3 update.py`
does the same by hand.
"""
import json
import os
import pathlib
import urllib.request

REPO = "nib-editor/nib"
TARGET = "x86_64-pc-windows-msvc"


def get(url):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token := os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request) as response:
        return response.read().decode()


def latest():
    """The latest release's tag and the sha256 of the Windows archive."""
    release = json.loads(get(f"https://api.github.com/repos/{REPO}/releases/latest"))
    tag = release["tag_name"]
    assets = {a["name"]: a["browser_download_url"] for a in release["assets"]}
    return tag, get(assets[f"nib-{tag}-{TARGET}.zip.sha256"]).split()[0]


def manifest(tag, sha256):
    name = f"nib-{tag}-{TARGET}"
    return {
        "version": tag.removeprefix("v"),
        "description": "Modal editor made of WebAssembly plugins, the Helix-style keymap included",
        "homepage": f"https://github.com/{REPO}",
        "license": "MIT|Apache-2.0",
        "architecture": {
            "64bit": {
                "url": f"https://github.com/{REPO}/releases/download/{tag}/{name}.zip",
                "hash": sha256,
                "extract_dir": name,
            }
        },
        "bin": "nib.exe",
        # For `scoop update` on its own, besides this bucket's workflow.
        "checkver": {"github": f"https://github.com/{REPO}"},
        "autoupdate": {
            "architecture": {
                "64bit": {
                    "url": f"https://github.com/{REPO}/releases/download/v$version/nib-v$version-{TARGET}.zip",
                    "hash": {"url": "$url.sha256"},
                    "extract_dir": f"nib-v$version-{TARGET}",
                }
            }
        },
    }


if __name__ == "__main__":
    tag, sha256 = latest()
    path = pathlib.Path(__file__).parent / "bucket" / "nib.json"
    path.write_text(json.dumps(manifest(tag, sha256), indent=4) + "\n")
    print(f"wrote {path} for {tag}")

# scoop-bucket

> nib's first release comes with 1.0.0. Until then there is nothing here to install; build nib from source as its README says.

The [Scoop](https://scoop.sh) bucket for [nib](https://github.com/nib-editor/nib), a modal editor made of WebAssembly plugins.

```powershell
scoop bucket add nib-editor https://github.com/nib-editor/scoop-bucket
scoop install nib
```

`bucket/nib.json` installs the prebuilt binary from nib's latest release. A [workflow](.github/workflows/update.yml) rewrites it from the release daily, and can be run by hand; `python3 update.py` does the same locally.

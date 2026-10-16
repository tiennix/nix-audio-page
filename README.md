# NIX Audio — website

Source of https://tiennix.github.io/nix-audio-page/ (documentation, FAQ, changelog and support for the
NIX Audio Unity package). Built with MkDocs Material and deployed by GitHub Actions on every push to `main`.

```bash
pip install -r requirements.txt
mkdocs serve        # preview at http://127.0.0.1:8000
```

The pages under `docs/docs/` are generated from `NixAudio/Documentation/NixAudio-Manual.md` in the package.
After editing the manual, regenerate them and copy the changelog:

```bash
python3 tools/split_manual.py <path>/Assets/NixAudio/Documentation/NixAudio-Manual.md docs/docs
cp <path>/Assets/NixAudio/CHANGELOG.md docs/changelog.md
mkdocs build --strict
```

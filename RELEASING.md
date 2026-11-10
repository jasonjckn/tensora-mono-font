# Releasing a new version

Requirements: `fontforge`, `uv`, `harfbuzz` (hb-view), `imagemagick`.

1. Copy the previous `src/TensoraMono_vN-1.sfd` and `src/TensoraMono_N_vN-1.sfd` to `_vN.sfd`, and edit them in FontForge or with a script. Then build both OTFs and both TTFs into `font_releases/<YYYY-MM-DD>-vN/` with `build/build.sh N <YYYY-MM-DD>`, and check all four with `uv run --python 3.13 --with fonttools python -I build/check.py font_releases/<YYYY-MM-DD>-vN/*.{otf,ttf}`. `build/compare.py OLD.otf NEW.otf` lists what changed between two releases.
2. Write the new release's preview text to `assets/tensora-mono-vN-<topic>.txt`.
3. Render **every** PNG again with the new fonts: `scripts/render-all.sh`. It picks the newest `font_releases/` directory and renders:
   - each release preview, `assets/tensora-mono-v*-*.txt` to `.png` (`scripts/preview.sh`: HarfBuzz at 320 px, downsampled with Lanczos to 160 px, white on black);
   - the README's banner, code samples, character set and variants (`scripts/readme-images.py`: drawn at 4x, downsampled with Lanczos to 2x for HiDPI screens, in a dark and a light version for GitHub's `prefers-color-scheme`; the code samples are the files in `assets/readme/code/`).

   Old releases' previews are redrawn too, so the README always shows the current font.
4. Update `README.md`: add the new preview under "Unicode coverage", and add the release's new glyphs to the list there.
5. Commit and push, then publish a GitHub release tagged `vN` with both OTFs, both TTFs and the new preview PNG (`gh release create vN --target main ...`).
6. Install the new OTFs in both places:
   - `~/Library/Fonts/` (then `fc-cache -f ~/Library/Fonts`)
   - `~/.local/share/init/fonts/`

   Running Emacs sessions keep the old font until they restart.

# Releasing a new version

1. Save the sources as `src/TensoraMono_vN.sfd` and `src/TensoraMono_N_vN.sfd`, and build both OTFs into `font_releases/<YYYY-MM-DD>-vN/`.
2. Write the preview text to `assets/tensora-mono-vN-<topic>.txt` and render it with `scripts/preview.sh font_releases/<dir>/TensoraMonoN.otf assets/tensora-mono-vN-<topic>.txt assets/tensora-mono-vN-<topic>.png` (`hb-view` at 160 px, white on black, so it stays sharp when zoomed). Show it inline in `README.md` under "Unicode coverage", with the other releases.
3. Render the README's banner, code samples, character set and variants again with the new font: `uv run --with pillow --with pygments python scripts/readme-images.py`. It draws at 4x and downsamples with Lanczos to 2x, in a dark and a light version for GitHub's `prefers-color-scheme`. The code samples are the files in `assets/readme/code/`.
4. Commit and push, then publish a GitHub release tagged `vN` with both OTFs and the PNG from step 2 (`gh release create vN --target main ...`).
5. Install the new OTFs in both places:
   - `~/Library/Fonts/` (then `fc-cache -f ~/Library/Fonts`)
   - `~/.local/share/init/fonts/`

   Running Emacs sessions keep the old font until they restart.

# ![image-20240114200542770](assets/image-20240114200542770.png)



#### Tensora Mono (nerd font), a font intended for programming languages. 

2 variants available 

* 'Tensora Mono'

  ![image-20240114201001166](assets/image-20240114201001166.png)

* 'Tensora Mono N' - identical to the above, but has a small caps 'N'
  ![image-20240114201028168](assets/image-20240114201028168.png)

#### v14: Claude Code's symbols

![Tensora Mono N v14 symbols](assets/tensora-mono-v14-symbols.png)

#### v15: combining marks

![Tensora Mono N v15 combining marks](assets/tensora-mono-v15-marks.png)

#### v15: small capitals, circled and math letters

![Tensora Mono N v15 small capitals, circled and math letters](assets/tensora-mono-v15-letters.png)

#### v16: superscripts and subscripts

![Tensora Mono N v16 superscripts and subscripts](assets/tensora-mono-v16-superscripts.png)

#### Releasing a new version

1. Save the sources as `src/TensoraMono_vN.sfd` and `src/TensoraMono_N_vN.sfd`, and build both OTFs into `font_releases/<YYYY-MM-DD>-vN/`.
2. Write the preview text to `assets/tensora-mono-vN-<topic>.txt` and render it with `scripts/preview.sh font_releases/<dir>/TensoraMonoN.otf assets/tensora-mono-vN-<topic>.txt assets/tensora-mono-vN-<topic>.png` (`hb-view` at 160 px, white on black, so it stays sharp when zoomed). Show it inline in this README, above this section, with the other releases.
3. Commit and push, then publish a GitHub release tagged `vN` with both OTFs and that same PNG (`gh release create vN --target main ...`).
4. Install the new OTFs in both places:
   - `~/Library/Fonts/` (then `fc-cache -f ~/Library/Fonts`)
   - `~/.local/share/init/fonts/`
   
   Running Emacs sessions keep the old font until they restart.

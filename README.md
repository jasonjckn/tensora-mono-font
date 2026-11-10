# ![image-20240114200542770](assets/image-20240114200542770.png)



#### Tensora Mono (nerd font), a font intended for programming languages. 

2 variants available 

* 'Tensora Mono'

  ![image-20240114201001166](assets/image-20240114201001166.png)

* 'Tensora Mono N' - identical to the above, but has a small caps 'N'
  ![image-20240114201028168](assets/image-20240114201028168.png)

#### Releasing a new version

1. Save the sources as `src/TensoraMono_vN.sfd` and `src/TensoraMono_N_vN.sfd`, and build both OTFs into `font_releases/<YYYY-MM-DD>-vN/`.
2. Commit and push, then publish a GitHub release tagged `vN` with both OTFs and a preview image (`gh release create vN --target main ...`).
3. Install the new OTFs in both places:
   - `~/Library/Fonts/` (then `fc-cache -f ~/Library/Fonts`)
   - `~/.local/share/init/fonts/`
   
   Running Emacs sessions keep the old font until they restart.

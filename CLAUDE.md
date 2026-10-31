# 3m-video

T3M's HyperFrames videos. Each top-level folder is one video project; `brand/` holds the T3M logo and colours; `sfx-library/` holds the shared sound effects.

## Sound effects: use `sfx-library/` first

`sfx-library/` has 715 CC0 sound effects (Saoud SFX Pack) as MP3 in 9 folders: `transitions`, `impacts`, `risers`, `ui-clicks`, `chimes-tones`, `alerts`, `sci-fi`, `foley`, `jingles`. `sfx-library/manifest.json` lists every sound with its `duration`, `peak_at` (seconds from the file's start to its loudest point) and a `description` of where it fits.

When a video needs sound effects:

1. Choose them from `sfx-library/manifest.json` before Openverse or the media-use bundled library. Use those only when nothing here fits.
2. Copy each chosen file into the video project's `assets/sfx/` and reference it from there. Compositions must not point at `../sfx-library`, because the render only sees files inside the project.
3. Time each sound so its `peak_at` lands one frame after the picture it belongs to: `data-start = visual time − peak_at + 1/fps`. A riser ends on its hit: `data-start = hit time − duration`.
4. Follow the HyperFrames sound rules (`/hyperframes`, `references/sound.md`): few, exact effects, each with a cause on screen; volume about 0.35 under voice and music; and rotate two or three takes of a repeated sound (for example `swipe_03`, `swipe_07`, `whoosh_fast_02`) rather than the same file on every cut.
5. `jingles/` are short music stings for an end card or logo, not effects. Don't play one over a music bed.
6. Everything in `sfx-library/` is CC0, so no credit is needed in the video, the caption or a `CREDITS.md`.

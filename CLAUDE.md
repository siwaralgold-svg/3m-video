# 3m-video

## Wait for the voiceover

Do not build, time or render a narrated video until the user has sent its voiceover file. When they send only a script, do only what they asked with the script (for example, tune its wording), then stop and wait for the recording. Never build a draft on estimated timing: it costs the user tokens and gets redone.

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

## The cartoon art style (from `edison-stole/`)

When a video should look like the Edison video, reuse its art style, not its story. The story, structure and setting are new each time; only the look carries over. The rules are in `edison-stole/STYLE.md`, and the drawing code is `edison-stole/assets/kit.js`.

1. Copy `edison-stole/assets/kit.js`, `assets/fonts/` (Lalezar, Noto Kufi Arabic), `assets/vendor/gsap.min.js` and `assets/brand/` into the new project.
2. Draw people with `EK.put(slot, prefix, who)`. Add a new person as one entry in the `WHO` table in `kit.js` (skin, suit, hair path, beard, moustache, glasses). Act with `EK.mood`, `EK.blink`, `EK.look` and `EK.idle`.
3. Draw every new prop and background the same way: flat fills, a #0c1a30 outline at 6–8 px, no gradients, no glow.
4. Build a new background for the new story. The courtroom belongs to the Edison video only.
5. `dostoevsky-trial/` is the second video in this style. Its `tools/build.py` writes the scene times, captions and sound-effect starts from the voiceover's word times, and its scenes anchor every beat to a script word with `w(<word index>)`. Use that setup for a narrated video so a new voiceover retimes the whole film.

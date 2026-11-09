# Review — draft 1 (no voice yet)

- Built storyline A (the trial). B (museum) and C (desk) are in STORYLINES.md, not built.
- Timing is estimated from the script. Every scene's anchors are in its `const T = {…}` line; retime to the voice's word times when `assets/voiceover.mp3` arrives, then rebuild the `<audio>` starts in index.html (start = picture time − peak_at + 1/30).
- Still to add once the voice exists: the voiceover clip, burned-in captions at y 1180–1320, and a music bed (no music source in this session).
- Measured: `check` passes; draft render 66.1 s; sound hits land within 1–2 frames of their picture; −20.3 LUFS with effects only, no clipping. Sound was measured, not heard.
- Looked at: frames at ~35 times across all seven scenes.
- Weakest shot: s5 between the cheque and the tear (5.3–8.6 s) is carried only by the dynamo spinning.
- Kept warning: `#court` holds an inline SVG at root level (the shared courtroom background).

# Review — draft 1 (no voice yet)

- The script was given, so no storylines were written. The frame is the "محاكمة" series, but the courtroom is not reused: a library desk, the snow square and one-off rooms.
- Timing is estimated (tools/estimate.py, about 2 words a second, 126.7 s). When the voiceover arrives: save it as assets/voiceover.mp3, transcribe it to assets/transcript.json (228 entries, one per script word, same order), run `python3 tools/build.py`. Scenes, captions and sound effects retime themselves; then check each scene's holds.
- Measured: `check` passes with no errors or warnings. Draft render 126.7 s; sound hits land about one frame after their picture; −24.4 LUFS with effects only, peak −6.2 dB, no clipping. Sound was measured, not heard.
- Looked at: about 110 frames across all thirteen scenes, plus the review sheets.
- Script note: he was 27 on the night of the letter and 28 on the square. The film shows "٢٨ سنة" where the script says it.
- Weakest shots: s4 and s2's candle room, where three busts share the frame and each is small; the lower third of the snow scenes is empty white under the captions.
- The friend's breakdown (s8) is played still: small pupils, a slow tilt, then he fades. No joke on it.
- No music bed: no music source in this session.

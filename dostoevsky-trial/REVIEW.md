# Review — cut 2 (voice in)

- Voice: ElevenLabs (Hijazi voice), 114.5 s, read from the tagged script; SCRIPT.md holds the same words without tags.
- Word times: whisper small (219 words) aligned to the 228 script words by letters (tools/align.py); whisper's digits (849, 27, 22, 28) are mapped to the spelled-out numbers. One word ("هو") is interpolated. Captions use the script's spelling.
- To retime after a new recording: replace assets/voiceover.mp3, transcribe to assets/transcript.whisper.json, run `python3 tools/align.py` and `python3 tools/build.py`.
- Script change: the first age is "سبعة وعشرين" (he was 27 when he read the letter, 28 on the square); the s2 card says ٢٧.
- Measured: `check` passes with no errors or warnings. Loudness of the render is in the delivery note. Sound was measured, not heard.
- Looked at: the review sheets on the voice timing, plus about 110 frames from the first build.
- Weakest shots: s4 and the candle room in s2, where three busts share the frame; the empty snow under the captions.
- No music bed: no music source in this session.

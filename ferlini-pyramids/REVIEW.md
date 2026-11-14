# Review — cut 1 (built on the voiceover)

- Voice: ElevenLabs (Hijazi voice), 83.6 s. SCRIPT.md holds the same words without emotion tags.
- Word times: whisper small (163 words) aligned to the 168 script words (tools/align.py); whisper's digits (1834, 40)
  are mapped to the spelled-out numbers, and a word that whisper starts inside a pause is moved to the end of the pause
  (ffmpeg silencedetect).
- To retime after a new recording: replace assets/voiceover.mp3, transcribe to assets/transcript.whisper.json,
  run `python3 tools/align.py` and `python3 tools/build.py`.
- `check` passes with no errors or warnings.
- Looked at: 52 frames across all thirteen scenes. Sound was measured, not heard.
- Weakest shots: s10's museums are small with empty ground under the captions; the arm that holds the permit (s4)
  and the bracelet (s9) is a plain tube.
- No music bed.

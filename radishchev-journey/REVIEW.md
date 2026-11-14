# Review notes

- Voice: `assets/voiceover.mp3` (ElevenLabs, 96.6 s). Whisper small transcript (196 words) aligned to the 194 script words by `tools/align.py`; none interpolated. Captions use the script's spelling.
- To retime after a new recording: replace the mp3, transcribe to `assets/transcript.whisper.json`, run `python3 tools/align.py`, `python3 tools/scenes.py`, `python3 tools/build.py`.
- Scenes are written by `tools/scenes.py`; edit that file, not `compositions/*.html`.
- Art: the Edison kit (`assets/kit.js`) with a new cast (censor, Radishchev, Catherine) and new backgrounds. Five props are Lottie files, listed in `assets/lottie/SOURCES.md`.
- No Lottie fitted the stamp, candle, dock, printing press, crown, calendar or the people, so those are drawn in the kit.
- The death sentence is shown as a word on a sheet of paper; the auction as "for sale" tags. No violence on screen.
- `check` passes with one craft warning: the unsigned cover in s6 is on screen 0.87 s (the line it belongs to is that short).
- No music bed: no music source in this session. Sound was measured, not heard.

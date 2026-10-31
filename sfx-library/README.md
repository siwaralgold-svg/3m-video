# مكتبة المؤثرات الصوتية (SFX Library)

715 مؤثر صوتي من **Saoud SFX Pack** (@saoudalajme)، محوّلة لـ MP3 وجاهزة لكل فيديوهات الهايبر فريم في هذا الـ repo.

الرخصة **CC0**: مجانية للاستخدام التجاري، وما تحتاج تكتب credit في الفيديو أو الكابشن. التفاصيل في `LICENSE.txt`.

| Folder | العدد | إيش فيه |
| --- | --- | --- |
| `transitions/` | 55 | swipe و whoosh بأنواعها (fast, soft, air, deep) للانتقالات بين المشاهد |
| `impacts/` | 122 | hit و boom و bass drop و stinger، وضربات خشب ومعدن وزجاج |
| `risers/` | 28 | riser قبل لحظة الذروة، و downlifter و reverse swell |
| `ui-clicks/` | 149 | pop و click و tick وصوت كتابة وفتح وإغلاق وكاميرا |
| `chimes-tones/` | 41 | ding و chime و sparkle ونغمات رقمية |
| `alerts/` | 8 | صوت خطأ، للحظة "لا تسوي كذا" |
| `sci-fi/` | 103 | glitch و laser و zap وأصوات تقنية |
| `foley/` | 124 | خطوات وأبواب وكتب وكروت وفلوس وعملات |
| `jingles/` | 85 | جنقلز موسيقية قصيرة للـ end card أو اللوقو |

## For Claude

- `manifest.json` lists every sound: `file`, `category`, `duration`, `peak_at` (seconds from the file's start to its loudest point) and a `description` of where it fits. Search it by description or name.
- All files are MP3, 48 kHz stereo, peak-normalised to −1 dBFS. Timing was checked against the original WAVs (decoded peaks match within a frame).
- Copy the sounds a video uses into that project's `assets/sfx/`; compositions reference only files inside their own project.
- The full rules are in the repo's root `CLAUDE.md`.

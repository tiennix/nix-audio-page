# FFmpeg (optional)

## 12. FFmpeg (optional)

FFmpeg is **not included** in NIX Audio. Install it yourself (https://ffmpeg.org/download.html, Homebrew,
winget, apt…), then open Audio Studio › **Integrations** and press **Detect** (searches PATH and the usual
install folders) or **Browse…**. NIX Audio runs FFmpeg only after you set its path there, only from the
editor, and only on local files; it never downloads anything.

| Feature | FFmpeg capability | Without FFmpeg |
|---|---|---|
| Volume › **Normalize LUFS** | `loudnorm` filter | Use Gain or Normalize peak. |
| Speed › **Keep pitch (time-stretch)**, high quality | `rubberband` filter | Use *Follows speed (resample)*. |
| Speed › **Keep pitch (time-stretch)**, basic | `atempo` filter | Same as above. |
| Save edits as **OGG** (same format as source) | `libvorbis` encoder | Saved as WAV. |
| Save edits as **MP3** | `libmp3lame` encoder | Saved as WAV. |
| Save edits as **FLAC** | `flac` encoder | Saved as WAV. |
| Save edits as **AIFF** | any FFmpeg build | Saved as WAV. |
| Read (preview waveform / edit) **compressed or streaming** clips (OGG, MP3, FLAC, AIFF whose Load Type is not *Decompress On Load*) | decoder | Set the clip's Load Type to *Decompress On Load*, or use WAV sources. |

The Integrations tab shows which of these the installed build supports; locked features link to it.

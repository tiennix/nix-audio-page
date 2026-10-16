# Limitations and tests

## 16. Known limitations

- Marker precision is one frame (callbacks run in `Update`).
- A voice is placed once at `Play(clip, position)`; it does not follow a moving object.
- Analysis (`GetSpectrum`, `GetOutput`, `GetLevel`, bands, `AudioReactive`, `BeatDetector`) uses Unity's
  `GetSpectrumData` / `GetOutputData`, which return no data on **WebGL**; meters read zero there. Playback,
  libraries and markers work on every platform.
- Audio Studio edits WAV natively; other formats need FFmpeg (see [§12](ffmpeg.md#12-ffmpeg-optional)).
- One `AudioPlayer` per running game (singleton).

## 17. Tests

EditMode tests in `Tests/Editor/` (*Window › General › Test Runner*). They compile only when the Test
Framework package is installed and cover the metadata registry, WAV codec, timeline and debug viewport maths,
Trim / Volume / Speed edits, library editing, analysis, bands and beat detection.

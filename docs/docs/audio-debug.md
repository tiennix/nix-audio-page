# Audio Debug

## 11. Audio Debug window

*Window › NIX Audio › Audio Debug* records the Audio Player every frame in Play Mode, up to 36,000 frames (about
10 minutes at 60 fps).

- **Charts**: Voices (with pool size, stolen and skipped counts), Audio CPU (Unity's audio counter, or the time
  of the `NixAudio.AudioPlayer.Update` profiler marker), Audio memory, Markers per frame. Mouse wheel zooms,
  Shift + wheel pans, **Fit** shows everything.
- **Tables** for the selected frame: voices (a clip started 4+ times within 0.6 s is highlighted — set
  Max instances or Cooldown) and clips in memory with their runtime size. **Unload idle** unloads every listed
  clip that is not playing. Double-click a row to open the clip in Audio Studio.
- Close the window when measuring with the Unity Profiler: it samples every voice each frame.

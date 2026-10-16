# Performance and recipes

## 14. Memory and performance

- Steady state allocates nothing per frame; `Play` allocates nothing either (the handle is a struct, voices
  come from a stack-based pool prewarmed on load). Callbacks you pass to `OnMarker` / `OnComplete` are
  delegates: for sounds played very often, keep them in fields instead of writing a new lambda each time.
- A library keeps a reference to every clip it lists. The sample **data** follows each clip's *Preload Audio
  Data* import flag; turn it off for large clips and use `Load(library, preloadAudioData: true)`.
- Split libraries by scene or feature. `Release` unloads data only for clips no longer referenced by any
  loaded library.
- Set **Max Voices**, and **Max instances** / **Cooldown** on sounds that can be spammed.
- Spectrum reads are cached per frame and shared by every `AudioReactive` and band read on the same source.

## 15. Recipes

```csharp
// Footsteps with variation: set Pitch to 0.92 – 1.08 in Audio Studio, then
player.Play(footstep, feet.position);

// Music with sections
_music = player.Play(battleLoop)
    .OnMarker("drop", () => SpawnEliteWave())
    .OnMarker("outro", () => _canFadeOut = true);

// Stop a loop safely
private void OnDisable() => _engineHum.Stop();

// Music / SFX sliders
player.SetBusVolume(AudioBus.MUSIC, musicSlider.value);
player.SetBusVolume(AudioBus.SFX, sfxSlider.value);
```

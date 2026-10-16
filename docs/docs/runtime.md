# Runtime API

## 4. Concepts

| Type | What it is |
|---|---|
| `AudioLibrary` | ScriptableObject holding a list of `AudioClipMeta`. Create it from Audio Studio (**+ New Library**) or *Create › NIX Audio › Audio Library*, then edit it in Audio Studio. |
| `AudioClipMeta` | Settings for one clip: `Clip`, `Output`, `Volume`, `PitchRange`, `SpatialBlend`, `Loop`, `MaxInstances`, `Cooldown`, `Markers`. Read-only at runtime. |
| `AudioMarker` | `Name` + `Time` (seconds). Stored in seconds, so it stays correct when the import sample rate changes. |
| `AudioPlayer` | Scene singleton (`AudioPlayer.Instance`, from `AudioPlayer.prefab`): load/release libraries, play clips, read the mix, global marker event. |
| `AudioVoicePool` | The child `Voices` object of the player: keeps the pooled voices. |
| `AudioHandle` | Small struct returned by `Play`; chain callbacks on it, stop it, query it. |

A clip that is **not** in any loaded library still plays, with neutral defaults: volume 1, pitch 1, 2D,
no loop, default output, no markers.

## 5. Setup and lifecycle

1. Drag **`Runtime/Prefabs/AudioPlayer.prefab`** into your first scene (or use *Tools › NIX Audio › Create Audio
   Player Prefab* if it is missing). With **Dont Destroy On Load** on (default), one instance survives scene
   changes; any later `AudioPlayer` destroys itself.
2. Configure it in the Inspector:
   - **Voice Pool** — the child `Voices` object (`AudioVoicePool`):
     - **Prefab** — `AudioVoice.prefab` (an `AudioSource` + `AudioVoice`). Edit it to change AudioSource
       defaults such as 3D rolloff.
     - **Initial Capacity** (default 32) — voices created when the player wakes up, so gameplay never
       instantiates. Keep it equal to *Max Voices*.
     - **Max Capacity** (default 64) — hard limit on the voices the pool creates.
   - **Max Voices** (default 32) and **Steal When Full** — the most sounds that play at once. When the limit is
     reached, a new play stops the oldest non-looping voice (no `OnComplete`), or is skipped and returns
     `AudioHandle.None` when stealing is off or every voice loops.
   - **Default Output** — mixer group for clips whose metadata has no Output (the bundled mixer's **SFX** group).
   - **Mixer** + **Buses** — the bundled `AudioMixer` and the exposed volume parameters the player restores on
     start (`BGM`, `SFX`). Route music to the BGM group with the clip's Output in Audio Studio.
   - **Click Clip** — what `PlayClick()` plays.
   - **Load On Awake** (+ *Preload On Awake*) — libraries loaded automatically.
3. From code, use `AudioPlayer.Instance`:

```csharp
var player = AudioPlayer.Instance;
player.Load(library);                              // make its metadata available
player.Load(library, preloadAudioData: true);      // ...and load the sample data now
player.Release(library);                           // undo one Load
player.ReleaseAll();                               // stop everything, release every library
player.SetDefaultOutput(sfxGroup);
```

| Member | Notes |
|---|---|
| `Load(AudioLibrary library, bool preloadAudioData = false)` | **Reference counted.** Loading the same library twice needs two `Release` calls. When two loaded libraries contain the same clip, the one loaded last wins. `preloadAudioData: true` calls `AudioClip.LoadAudioData()` for clips whose data is not loaded yet, so the first play has no hitch. |
| `Release(AudioLibrary library)` | Undoes one `Load`. When a clip is no longer referenced by any loaded library, its audio data is unloaded — right away, or as soon as its last voice finishes. Loading it again before that cancels the unload. Releasing a library that is not loaded logs a warning. |
| `ReleaseAll()` | `StopAll()`, then releases every library and unloads idle clip data. |
| `IsLoaded(AudioLibrary library)` | `true` while at least one `Load` is not released. |
| `SetDefaultOutput(AudioMixerGroup output)` | Changes the default output at runtime. |
| `SetMaxVoices(int maxVoices, bool stealWhenFull)` | Changes the voice limit at runtime. |
| `SetBusVolume(string bus, float volume)`, `GetBusVolume(bus)` | 0..1 volume of a mixer bus (`AudioBus.MUSIC` = "BGM", `AudioBus.SFX` = "SFX"), converted to dB on the mixer's exposed parameter and saved in PlayerPrefs. |
| `SetBusMuted(string bus, bool muted)`, `IsBusMuted(bus)` | Mutes a bus without losing its volume; saved in PlayerPrefs. |
| `PlayClick()` | Plays the **Click Clip**; `AudioHandle.None` when none is set. |

### Where to call Load / Release

- **One global library** (UI sounds, common SFX): put it in *Load On Awake*.
- **Per scene / per feature**: `Load` in the scene's bootstrap (`Start`), `Release` in `OnDestroy`. Use `Start`
  rather than `Awake` so the player has finished its own `Awake`.
- **Addressables**: load the library asset through Addressables, then `Load(library)`; call `Release` before
  releasing the Addressables handle. Keep a library and its clips in the same "world" (both built-in or both
  in the same Addressables group); otherwise the clip you play is a different instance from the one in the
  library and its metadata is not found.

## 6. Playing

```csharp
AudioHandle handle = player.Play(clip);
AudioHandle hit = player.Play(explosion, transform.position);
```

| Member | Notes |
|---|---|
| `Play(AudioClip clip)` | Plays with the clip's metadata (or defaults) at the player's position. Returns `AudioHandle.None` and logs a warning for a `null` clip. |
| `Play(AudioClip clip, Vector3 position)` | Same, with the voice placed at `position`. Only audible as 3D when the clip's **Spatial blend** is above 0. The voice does not follow a moving object. |
| `StopAll()` | Stops every voice. `OnComplete` callbacks are **not** called. |
| `TryGetMeta(AudioClip clip, out AudioClipMeta meta)` | Reads the metadata the player will use. `false` means defaults. |
| `ActiveVoiceCount`, `LoadedClipCount`, `PooledVoiceCount`, `MaxVoices`, `DefaultOutput` | Diagnostics. |
| `StolenVoiceCount`, `SkippedPlayCount`, `PendingUnloadCount` | Voices stopped to make room, plays skipped by a limit or cooldown (both since start), clips waiting to unload. |
| `CollectVoices(List<AudioVoiceInfo>)` | Snapshot of every active voice. Used by Audio Debug. |
| `CollectLoadedClips(List<AudioClip>)`, `CollectLibraries(List<AudioLibrary>)`, `GetLoadCount(library)` | What is loaded and how many `Load` calls each library has. |

What the metadata does on each play:

- **Volume** → `AudioSource.volume`.
- **Pitch range** → a random pitch between min and max (same value for a fixed pitch). Good for footsteps or hits.
- **Spatial blend** → 0 = 2D, 1 = fully 3D.
- **Loop** → loops until stopped; markers fire on every loop.
- **Output** → `AudioMixerGroup`; empty uses the player's **Default Output**.
- **Max instances** (0 = no limit) → when that many copies of the clip already play, the new play replaces the oldest copy.
- **Cooldown** (seconds, 0 = off) → a play closer than this to the previous play of the same clip is skipped and returns `AudioHandle.None`.

## 7. Markers and callbacks

Markers are placed in Audio Studio (press **M** while the clip plays). At runtime you can listen in three ways.

```csharp
// One playback, by name
player.Play(swordSwing)
    .OnMarker("windup", OnWindupEvent)
    .OnMarker("hit", OnSwordHitEvent)
    .OnComplete(OnSwingFinishedEvent);

// One playback, every marker
player.Play(bossIntro).OnMarker(marker =>
{
    if (marker.Name == "camera_cut") CutCamera();
});

// Globally, for every clip
private void OnEnable() => player.onMarkerReached += OnMarkerReachedEvent;
private void OnDisable() => player.onMarkerReached -= OnMarkerReachedEvent;
private void OnMarkerReachedEvent(AudioClip clip, AudioMarker marker) { /* … */ }
```

Behaviour you can rely on:

- Callbacks run on the main thread from the player's `Update`, so precision is one frame (about 16 ms at 60 fps). The position is read from `AudioSource.timeSamples`.
- Several markers crossed in one frame fire in order.
- Looping clips fire their markers again on each loop, including a marker at `0`.
- Markers placed after the end of the clip never fire (Audio Studio warns about them).
- An exception thrown by your callback is logged and does not stop the other callbacks.
- While `AudioListener.pause` is true, playback and markers wait.

## 8. AudioHandle

| Member | Notes |
|---|---|
| `OnMarker(string name, Action callback)` | Fires when the marker with this exact name (case-sensitive) is reached. Returns the handle for chaining. |
| `OnMarker(Action<AudioMarker> callback)` | Fires for every marker. |
| `OnComplete(Action callback)` | Fires when a non-looping clip finishes on its own. Not called by `Stop`/`StopAll`. |
| `Stop()` | Stops this playback only. Safe to call on an old or `None` handle. |
| `Pause()`, `Resume()`, `IsPaused` | Pauses this playback; markers and `OnComplete` wait. A paused voice still counts toward Max Voices. |
| `SetVolume(float volume)`, `Volume` | 0..1 multiplier on the clip's metadata volume. |
| `IsValid` | `false` once the playback ended or was stopped. Voices are pooled, so an old handle never controls a newer playback. |
| `IsPlaying` | `IsValid` and the source is playing. |
| `Clip`, `Time`, `Length`, `Progress` | The clip (or `null`), position in seconds, clip length, position as 0..1. |
| `GetSpectrum`, `GetOutput`, `GetLevel`, `GetBand`, `GetBandLevel` | Analysis of this playback only — see [§9](#9-reading-sound-waves-spectrum-waveform-level). |
| `AudioHandle.None` | The empty handle (also `default`). |

## 9. Reading sound waves (spectrum, waveform, level)

Use these to drive visualizers, lip-flap, lights that pulse with the music, or loudness meters. Call them
every frame with arrays you allocate once.

```csharp
private readonly float[] _spectrum = new float[1024];   // power of two, 64–8192
private readonly float[] _bands = new float[32];

private void Update()
{
    player.GetSpectrum(_spectrum);                       // everything the AudioListener hears
    AudioAnalysis.ToBands(_spectrum, _bands, AudioSettings.outputSampleRate);
    var loudness = AudioAnalysis.ToMeter(player.GetLevel());
}
```

| Member | Returns |
|---|---|
| `player.GetSpectrum(float[] spectrum, FFTWindow window = BlackmanHarris)` | Magnitude per frequency bin of **everything heard**. Bin `i` covers `i × sampleRate / 2 / length` Hz. |
| `player.GetOutput(float[] samples)` | The latest output samples (-1..1). |
| `player.GetLevel()` | RMS loudness (0..1) of the last 256 output samples. |
| `handle.GetSpectrum / GetOutput / GetLevel` | Same, for that playback only (first channel). Returns `false` / 0 when the handle is no longer valid. |
| `GetBand(AudioBand band)`, `GetBandLevel(band, floorDb = -60)` | Energy of one band, raw or as 0..1. One FFT per frame is shared by all band reads. |

Helpers in `AudioAnalysis`: `ToBands`, `ToMeter`, `ToDecibels`, `Rms`, `Peak`, `Smooth`, `BandFrequency`, `BandEnergy`.

| `AudioBand` | Range | Good for |
|---|---|---|
| `SUB` | 20–60 Hz | rumble |
| `KICK` | 40–100 Hz | kick drum hits (use with `BeatDetector`) |
| `BASS` | 60–250 Hz | bass line level |
| `VOICE` | 300–3400 Hz | singing / dialogue |
| `SNARE` | 1.8–5 kHz | snare and claps |
| `HI_HAT` | 6–16 kHz | hi-hats, cymbals |

`new AudioBand("Pad", 200f, 800f)` defines your own range. `BeatDetector` reports a beat when the band energy
is `sensitivity` times (default 1.5×) its average over the last second, at most once per `cooldown`.

### AudioReactive component (no code)

*Add Component › NIX Audio › Audio Reactive*: pick a **Band**, a **Mode** (*Beat* pulses on each hit, *Level*
follows loudness), **Attack / Release**, and what to drive: **Scale amount**, **Move amount**, renderer **Tint**
and **Emission**. It reads the whole mix by default; `reactive.Follow(handle)` follows one playback.

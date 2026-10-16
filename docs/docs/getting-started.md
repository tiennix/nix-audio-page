# Getting started

## 1. Requirements and dependencies

| What | Needed for | Notes |
|---|---|---|
| Unity 2022.3 LTS or newer (Unity 6 supported) | everything | |
| Built-in Unity modules: Audio, UI Toolkit (Editor), JSON | everything | Enabled by default. |
| **TextMeshPro** (`com.unity.textmeshpro` on 2022.3, part of `com.unity.ugui` on Unity 6) + **TMP Essential Resources** | demo scenes only | Import the essentials once with *Window › TextMeshPro › Import TMP Essential Resources*, otherwise the demo text is invisible. |
| **Unity UI** (`com.unity.ugui`) | demo scenes only | |
| Input System (`com.unity.inputsystem`) | optional, demo only | Used automatically when the project's Active Input Handling is *Input System Package (New)*. |
| Test Framework (`com.unity.test-framework`) | optional | The EditMode tests compile only when it is installed. |
| **FFmpeg** (not included) | optional, Audio Studio only | Extra features listed in [§12](ffmpeg.md#12-ffmpeg-optional). Everything else works without it. |

Render pipelines: the runtime and the editor tools do not render anything and work with Built-in, URP and
HDRP. The demo speaker picks the materials of the active pipeline when the scene plays; see [§13](demo.md#13-demo-scenes).

The runtime has **no dependency on other Asset Store packages** and does not use the network.

Enter Play Mode Options: the runtime supports *Enter Play Mode* with **Domain Reload disabled**; static state
(`AudioPlayer.Instance`, the shared spectrum cache) is reset on every Play.

## 2. Quick start

1. Drag `NixAudio/Runtime/Prefabs/AudioPlayer.prefab` into your first scene.
2. Open *Window › NIX Audio › Audio Studio*, press **+ New Library**, then **+ Add ▾ › Add Folder…** and pick
   the folder with your clips.
3. Select a clip, set its volume / pitch / loop in the **Metadata** tab, press **M** while it plays to add a
   marker, then **Save** (Ctrl/Cmd + S).
4. In code:

```csharp
using NixAudio;
using UnityEngine;

public sealed class Sword : MonoBehaviour
{
    [SerializeField] private AudioLibrary _library;
    [SerializeField] private AudioClip _swing;

    private void Start() => AudioPlayer.Instance.Load(_library);
    private void OnDestroy() => AudioPlayer.Instance?.Release(_library);

    public void Attack()
    {
        AudioPlayer.Instance.Play(_swing, transform.position).OnMarker("hit", ApplyDamage);
    }

    private void ApplyDamage() { /* … */ }
}
```

To see everything working first, open `NixAudio/Demo/NIXAudioDemo_Landscape.unity` and press Play.

## 3. Folder structure and assemblies

```
Assets/NixAudio/
├── Runtime/                    NixAudio.Runtime.asmdef            namespace NixAudio
│   ├── Data/                   AudioLibrary, AudioClipMeta, AudioMarker
│   ├── Playback/               AudioPlayer, AudioVoicePool, AudioVoice, AudioHandle, AudioBus, registry
│   ├── Analysis/               AudioAnalysis, AudioBand, BeatDetector, AudioReactive, shared FFT cache
│   ├── Mixer/                  AudioMixer.mixer (Master › BGM, SFX; exposed parameters BGM, SFX)
│   └── Prefabs/                AudioPlayer.prefab (+ Voices pool), AudioVoice.prefab
├── Editor/                     NixAudio.Editor.asmdef (Editor only) namespace NixAudio.Studio
│   ├── Window/                 Audio Studio window, menus, AudioStudio.uss (styles for both windows)
│   ├── Views/                  clip browser, timeline, ruler, waveform, markers, transport, tool panels
│   ├── State/                  window state, settings asset, library editing, source index, snapping
│   ├── Processing/             WAV codec, Trim / Volume / Speed edits, writer, backups
│   ├── FFmpeg/                 optional FFmpeg detection and runner
│   ├── Preview/, Waveform/     edit-mode preview playback, cached waveform peaks
│   ├── Debug/                  Audio Debug window (recorder, charts, viewport)
│   └── Setup/                  package paths, AudioPlayer / AudioVoice prefab builder
├── Demo/                       NixAudio.Demo.asmdef               namespace NixAudio.Demo
│   ├── Editor/                 NixAudio.Demo.Editor.asmdef        DemoSceneBuilder
│   ├── Audio/                  five demo clips (48 kHz / 24-bit WAV)
│   └── Materials/              speaker materials: URP/Lit, and Standard copies in Built-in/
├── Tests/Editor/               NixAudio.Tests.Editor.asmdef       EditMode tests
└── Documentation/              this manual
```

- Editor code never reaches a player build (`NixAudio.Editor` and `NixAudio.Demo.Editor` are Editor-only).
- `NixAudio.Demo` is not auto-referenced: deleting the `Demo` folder never breaks your project.
- You can move the `NixAudio` folder anywhere under `Assets`; the editor tools find it through
  `Runtime/Playback/AudioPlayer.cs`.

Files NIX Audio creates **outside** its folder:

| Path | What | Commit it? |
|---|---|---|
| `Assets/Settings/NixAudio/NixAudioStudioSettings.asset` | Audio Studio sources, default library, snap mode, WAV format. Created the first time Audio Studio opens. You can move it; it is found by type. | Yes — the team shares the same setup. |
| `Library/NIXAudioBackup/` | Backups of clips overwritten by Trim / Volume / Speed. | No (Library is local). |
| `Temp/NIXAudioStudio/` | Temporary files of FFmpeg jobs, deleted after each job. | No. |
| EditorPrefs `NixAudio.Studio.*` | FFmpeg path, *Follow selection*. | Per machine. |
| PlayerPrefs `nix.audio.bus.*` | Bus volume and mute, at runtime. | In the player's save data. |

### Menus

| Menu | What it does |
|---|---|
| *Window › NIX Audio › Audio Studio* | Opens the editor window. |
| *Window › NIX Audio › Audio Debug* | Opens the Play Mode profiler. |
| *Assets › NIX Audio › Open in Audio Studio* | Opens a selected clip, or adds a selected folder as a source. |
| *Tools › NIX Audio › Create Audio Player Prefab* | (Re)creates `Runtime/Prefabs/AudioPlayer.prefab` and `AudioVoice.prefab` if they are missing. |
| *Tools › NIX Audio › Rebuild Demo Scene* | Rebuilds the open demo scene with the speaker materials of the active render pipeline. |
| *Create › NIX Audio › Audio Library* | New `AudioLibrary` asset. |
| *Add Component › NIX Audio › Audio Player / Audio Reactive* | The two runtime components. |

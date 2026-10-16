# Demo scenes

## 13. Demo scenes

Two scenes in `NixAudio/Demo/`, same content, different layout:

| Scene | Aspect |
|---|---|
| `NIXAudioDemo_Landscape.unity` | 16:9 (reference 1920×1080) |
| `NIXAudioDemo_Portrait.unity` | 9:16 (reference 1080×1920) |

Before the first run: import **TMP Essential Resources** (*Window › TextMeshPro › Import TMP Essential
Resources*), then set the Game view to the matching aspect.

- **Middle**: an audio-reactive speaker made of primitives and `AudioReactive` components.
- **Left**: "Try it" cards — each shows the exact code its buttons run (library loading, music loop with
  section markers, named markers, random pitch, the global marker event, 3D position, a clip without metadata, stopping).
- **Right**: band meters with beat dots, a 40-band spectrum, the waveform, the level meter and the event log.

The demo clips are synthetic (48 kHz / 24-bit WAV); their metadata lives in `Demo/DemoAudioLibrary.asset`.

### Render pipeline of the demo materials

Each speaker material ships twice: **URP/Lit** in `Demo/Materials/` and **Standard (Built-in)** in
`Demo/Materials/Built-in/`. The `DemoSpeakerRig` component on *Demo Speaker* lists both and, **when the scene
plays**, gives every speaker renderer the version of the project's active render pipeline:

| Active pipeline | Speaker in Play Mode |
|---|---|
| Built-in | the Standard materials |
| URP | the URP/Lit materials |
| HDRP or a custom SRP | materials created at runtime from the pipeline's default shader, with the same colors |

Nothing is written to disk: the saved scene and the material assets stay as they are.

The saved scenes reference the URP materials, so in a Built-in or HDRP project the speaker looks pink **in
edit mode only**. To make the Scene view match too, open a demo scene and run *Tools › NIX Audio › Rebuild Demo
Scene*: it rebuilds the open scene with the materials of the current pipeline (Built-in → the Standard copies).
Rebuilding also recreates the scene's UI, so local changes to a demo scene are lost.

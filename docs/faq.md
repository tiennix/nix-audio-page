# FAQ

??? question "Does the runtime need FFmpeg?"
    No. FFmpeg is only used by the Audio Studio editor window for a few extra features (LUFS normalize,
    time-stretch, saving edits as OGG / MP3 / FLAC, reading compressed clips). Everything else, and the whole
    runtime, works without it. See [FFmpeg](docs/ffmpeg.md).

??? question "Which render pipelines are supported?"
    Built-in, URP and HDRP. The runtime and the editor windows do not render anything. The demo speaker
    switches to the materials of your pipeline when the scene plays; to make the Scene view match, run
    *Tools › NIX Audio › Rebuild Demo Scene*. See [Demo scenes](docs/demo.md).

??? question "The demo text is invisible."
    Import TextMeshPro's essentials once: *Window › TextMeshPro › Import TMP Essential Resources*.

??? question "Does it work with Enter Play Mode Options (Domain Reload disabled)?"
    Yes. Static state is reset on every Play, and this is covered by tests on Unity 2022.3 and Unity 6.

??? question "Does it work on WebGL?"
    Playback, libraries and markers do. The analysis functions (spectrum, bands, `AudioReactive`) rely on
    Unity's `GetSpectrumData` / `GetOutputData`, which return no data on WebGL, so meters read zero there.

??? question "Can I use it with Addressables?"
    Yes. Load the `AudioLibrary` through Addressables, then call `AudioPlayer.Instance.Load(library)`, and
    keep the library and its clips in the same Addressables group. See
    [Where to call Load / Release](docs/runtime.md#where-to-call-load-release).

??? question "Will Audio Studio change my audio files?"
    Only when you apply a Trim, Volume or Speed edit. *Back up original* is on by default and copies the file
    to `Library/NIXAudioBackup/`; **Restore latest backup** brings it back. Metadata and markers live in the
    library asset and never touch the audio file.

??? question "Can I delete the Demo folder?"
    Yes. Nothing outside `NixAudio/Demo` depends on it.

??? question "How precise are markers?"
    One frame: callbacks run in the player's `Update` (about 16 ms at 60 fps).

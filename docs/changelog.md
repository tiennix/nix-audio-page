# Changelog

All notable changes to NIX Audio are documented here.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versions follow [SemVer](https://semver.org/).

## [1.0.0] - 2026-10-16
### Added
- AudioPlayer scene singleton (AudioPlayer.prefab) that plays an AudioClip directly, with a prewarmed stack-based voice pool, Max Voices and voice stealing
- AudioLibrary / AudioClipMeta metadata per clip: output, volume, pitch range, spatial blend, loop, max instances, cooldown, markers
- AudioHandle: OnMarker, OnComplete, Stop, Pause, Resume, SetVolume, time and progress
- Mixer buses: SetBusVolume / SetBusMuted saved in PlayerPrefs (BGM and SFX in the bundled AudioMixer), PlayClick
- Analysis: spectrum, waveform, level, frequency bands, BeatDetector and the AudioReactive component
- Audio Studio editor window: libraries, markers, metadata, trim / volume / speed edits with backups, Undo for library and source changes, optional FFmpeg
- Audio Debug window: Play Mode charts and tables for voices, CPU, memory and markers
- Demo scenes (16:9 and 9:16) with 48 kHz / 24-bit demo clips; the speaker uses the materials of the active render pipeline (Built-in, URP, HDRP) when the scene plays
- Assembly definitions for Runtime, Editor, Demo and Tests; support for Enter Play Mode with Domain Reload disabled

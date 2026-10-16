# Audio Studio

## 10. Audio Studio (editor)

*Window › NIX Audio › Audio Studio*. Everything it writes is either the **library asset** (metadata and
markers), the **clip's `.meta`** (import settings) or, for Trim / Volume / Speed, the **audio file** itself.

| Area | Contents |
|---|---|
| Toolbar | **Library** field, **+ New Library**, **Follow** (show the clip selected in the Project window), **Ping Clip**, **Save**. |
| Left: clip browser | Search, **+ Add ▾** (add a folder or clip as a source), clips grouped by folder with marker count and length. Drag folders or clips from the Project window onto the list. |
| Middle: timeline | Ruler, waveform, marker lane, transport (to start, play/stop, loop, previous / add / next marker, snap, time). Zoom with − / + / Fit or Ctrl/Cmd + wheel. |
| Bottom: marker table | Rename, retime or delete markers; click a row to jump to it. |
| Right: tool tabs | **Metadata** · **Trim** · **Volume** · **Speed** · **Integrations**. |

**Metadata tab** — Output, Volume, Pitch range, Spatial blend, Loop, Max instances, Cooldown, plus the clip's
import Load Type and Preload Audio Data. **Copy / Paste meta**, **Reset**, **Remove entries of deleted clips**.

**Markers** — **M** adds a marker at the playhead (also while playing); drag a flag to move it; snap is
**Off**, **Transient** (nearest onset) or **Grid**; **[** / **]** jump between markers; **Delete** removes one.

**Trim, Volume and Speed tabs** (edit the audio file):

| Tab | Options |
|---|---|
| Trim | Drag the handles, press **[** / **]** to set start / end to the playhead, or type times. Optional fade in / out. Markers outside the kept range are deleted; the others shift. |
| Volume | **Gain** (dB), **Normalize peak**, **Normalize LUFS** (needs FFmpeg). |
| Speed | **Follows speed (resample)** changes pitch with speed; **Keep pitch (time-stretch)** needs FFmpeg. Markers are rescaled. |

Edits stay **pending** until you apply them (order Trim → Speed → Volume, one write). **Play result**
previews them. **Apply to clip**:

- **Overwrite clip** keeps the GUID, so every reference stays valid. **Back up original** (on by default)
  copies the file to `Library/NIXAudioBackup/` first; **Restore latest backup** brings it back.
- **Save as new clip** writes a new asset next to the original.
- **Format**: *Same as source*, or WAV 16-bit, 24-bit or 32-bit float. Without FFmpeg, non-WAV sources are saved as WAV.

### Undo / Redo

Ctrl/Cmd + Z works for everything stored in assets: adding, moving (one step per drag), renaming and deleting
markers; every metadata field; Paste / Reset metadata; removing entries of deleted clips; adding and removing
sources (several dropped at once are one step).

Not on the Undo stack, by design:

- **Audio file edits** (Trim / Volume / Speed applied to the file) — use **Restore latest backup** instead.
- **Import settings** (Load Type, Preload) — they reimport the clip, like Unity's own importer inspector.
- **Creating a library, deleting a file** (moved to the OS trash) and view preferences such as snap mode or
  the library shown in the toolbar.

### Keyboard

| Key | Action |
|---|---|
| Space | Play / stop the preview |
| Home | Playhead to start |
| M | Add marker at the playhead |
| [ / ] | Previous / next marker; in the Trim tab: trim start / end to playhead |
| Delete / Backspace | Delete the selected marker |
| Ctrl/Cmd + S | Save library and settings |
| Ctrl/Cmd + wheel | Zoom the timeline around the cursor |

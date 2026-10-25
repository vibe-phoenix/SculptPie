# SculptPie: fast pie menus for ZBrush 2026.1 and newer

Twenty independently configured pie menus. Hold a shortcut and the menu appears at the cursor; move
toward an item and release the key (or click) to apply it. Brushes, alphas, materials and ZBrush buttons,
switches and sliders can all be items, organised in nested groups that open either as an outer ring
(**Expand**) or by replacing the ring (**Switch**, with the centre as the way back).

Written from scratch in native C++ (Win32, Direct2D, DirectWrite, DirectComposition), with no UI framework
and no managed runtime. Measured on this machine: a warm menu is on screen **≈1.8 ms** after ZBrush calls
the plugin (median; see *Validation*).

---

## Install

Requirements: Windows 10/11 x64 and **ZBrush 2026.1.0 or newer** (2026.1.x, 2027, ...).

SculptPie supports exactly the versions that load user plugins from the per-user asset folder. Maxon moved
plugins there in **ZBrush 2026.1.0** ("Important Changes to ZBrush File Directory and User Asset Structure
(2026.1 and Newer)"); up to 2026.0.x they lived in `<ZBrush install>\ZStartup\ZPlugs64`, and those older
versions are not supported.

1. Start each new ZBrush once (it creates its asset folder), then close it.
2. Extract `SculptPie-1.3.0.zip` and double-click **`Setup.exe`** (or `Install.bat`).
3. Setup lists every ZBrush it finds (Windows uninstall entries + `Program Files`, or **Add ZBrush folder...**),
   reads each `ZBrush.exe` version and installs into
   `%APPDATA%\Maxon\Maxon ZBrush 20xx_<id>\ZStartup\ZPlugs64` (Preferences > Asset Directory > Open Directory).
   No administrator rights are needed. Older versions are shown as not supported.
4. Start ZBrush. **ZPlugin > SculptPie** shows `PieMenu01` to `PieMenu20` and **Settings**.

Updating is the same: run Setup again (if ZBrush is running, restart it afterwards). Nothing else in ZPlugs64
is touched (Trigon Pie Menu and your other plugins are left alone). Your menus and styles live in
`Documents\ZBrush\SculptPie` and are never changed by Setup.

Command line: `SculptPieSetup.ps1 -List | -Install | -Uninstall [-ZBrushDir "<folder with ZBrush.exe>"]`.
### Uninstall
Run Setup and click **Uninstall** (or `Uninstall.bat`). Your menus and styles are kept in
`Documents\ZBrush\SculptPie`; delete that folder to remove them too.
## Assign shortcuts
1. Open **ZPlugin › SculptPie**.
2. Hold **Ctrl+Alt** and click **PieMenu01**, then press the key (or key combination) you want.
3. Repeat for any other menus.
4. **Preferences › Hotkeys › Store** saves the shortcuts permanently.

The buttons' paths (`ZPlugin:SculptPie:PieMenu01` … `PieMenu20`) never change, so stored shortcuts keep
working after restarts and SculptPie updates.

## Use
* **Hold** the shortcut: the menu opens at the cursor.
* **Move** toward an item: it highlights, and the centre ring points at it.
* **Release** the key to apply the highlighted item, or **click** an item at any time.
* Releasing in the centre, or over a group, does nothing (closes the menu).
* **Groups**: rest on a group for the *Group Enter Delay* (default 255 ms; a progress arc shows on the group).
  * **Expand**: the group's items appear in an outer ring next to it; move outward onto them.
  * **Switch**: the ring is replaced by the group's items; move back into the **centre (Parent Zone)**
    to return.
  * Clicking a group opens it immediately.
* **Escape** or right-click cancels (right-click goes back one level inside a group).
* Clicking a PieMenu button with the mouse (no key held) opens the menu in **click mode**: it stays open
  until you click an item or press Escape.
* Near a screen edge the menu moves inward so it is fully visible, and the cursor moves with it
  (Settings › Advanced › Screen Edges).

## Settings editor
**ZPlugin › SculptPie › Settings** opens the editor. It stays on top of ZBrush (as an owned window, not
always-on-top over other apps) and fills ZBrush's monitor with a margin. Esc or Close hides it.

**Style tab**: every visual property, grouped as Color Adjust, Menu Shape (centre ring, ring shadow, group
ring, spacing), Labels & Text, Icons & Alphas, Background & Underlay, Animation and Advanced (group delay,
default group mode, expand-ring distance and size, idle zone, click behaviour, screen edges). Changes apply
to the live menus instantly. Each card has a reset button; right-click a slider to reset it, and use the
mouse wheel to nudge (Ctrl ×10). Presets: pick one from the dropdown, then **Import, Export, New,
Duplicate, Rename, Delete**. Built-in presets: Azure (default), Graphite, Ember, Minimal, Compact (text
only). **Background** toggles a light preview backdrop. Undo/Redo: Ctrl+Z / Ctrl+Y.

**Build tab**: choose a menu (PieMenu01–20) at the top right.
* Library (left): ZBrush's brushes, alphas and materials, the folders configured in **SculptShelf**,
  folders you add (**Add Folder**), and common ZBrush interface items (or **Custom ZBrush Item…** for any
  `Palette:Subpalette:Item` path; hold Ctrl over a ZBrush button to see its path).
* **Double-click** a library item to append it, or **drag** it onto the menu: drop between items to insert,
  or onto a group to put it inside.
* In the menu: click to select, drag to reorder, drop onto a group to move into it, double-click a group
  to open it (**Up**, Backspace or right-click to go back), **Delete** removes, F2 renames.
* Properties panel: label, type, target (with Browse), slider value, custom icon (or automatic), group
  mode (**Default / Expand / Switch**, per group), Earlier/Later, Duplicate, Group It, Move Out, Open, Delete.
* Toolbar: Rename menu, Import/Export menu JSON, New Group, Clear, Undo/Redo.
* **Export With External Brushes (.zip)** (Menu Tools): one zip with the menu plus every brush, alpha,
  material and custom icon file it uses from outside ZBrush. **Import** accepts that zip: a progress bar shows
  while it unpacks to `Documents\ZBrush\SculptPie\Packs\<name>` and the menu is loaded pointing at those files.

Every change is saved automatically (≈0.35 s debounce, atomic writes).

### Icons
For each item: your custom icon if set → **SculptShelf's thumbnail cache** (read-only; shared with
SculptShelf) → the preview embedded in the `.zbp`/`.zmt` file (decoded by SculptPie) → the image file itself
for alphas (PNG/JPG/TIF/BMP/PSD) → a lettered glyph. Decoded icons are cached in
`%LOCALAPPDATA%\SculptPie\Cache\icons` and loaded in the background at startup, so opening a menu never waits
on disk.

## Files
| Path | Contents |
|---|---|
| `%APPDATA%\SculptPie\settings.json` | active style, editor state, extra library folders |
| `%APPDATA%\SculptPie\menus\menu_01.json` … `menu_20.json` | one file per menu |
| `%APPDATA%\SculptPie\styles\<name>.json` | style presets |
| `%LOCALAPPDATA%\SculptPie\Cache\icons` | decoded icon cache (safe to delete) |
| `%LOCALAPPDATA%\SculptPie\Logs` | `service.log` (with per-open latency), `bridge.log`, `plugin.log` |

All files are versioned JSON (`"version": 1`). Writes go to a temp file that atomically replaces the old one;
the previous version is kept as `.bak`. A corrupted file is preserved as `.corrupt` and the `.bak` (or the
defaults) is used instead. Unknown or out-of-range values fall back to defaults.

## How it works
```
ZBrush main thread                         SculptPie.exe (one per ZBrush process, persistent)
------------------                         -------------------------------------------------
hotkey -> SculptPie.py button callback      pipe thread: blocks in ConnectNamedPipe (no polling)
  -> SculptPieBridge.dll PF_Show(n)  --pipe-->  UI thread wakes, reads trigger keys from the request,
     (keyboard state of the hotkey)            draws frame 1 (Direct2D), Present, DComp uncloak
     waits; keeps ZBrush "responding"          4 ms waitable timer: cursor + trigger keys
  <- "brush\t<path>\t<label>"      <--pipe--   release/click/Esc/focus loss -> cloak, reply
  -> Python performs the ZBrush action on ZBrush's own thread (press / set_next_filename+Load Brush ...)
```
* **No process launch or framework start per press.** The service starts with ZBrush (`PF_Start`
  at plugin load), pre-builds the window, GPU device, swap chain, text layouts and icon bitmaps, and
  renders a hidden warm-up frame.
* **Never activated.** The overlay is a topmost, non-activating DirectComposition window, so ZBrush keeps
  keyboard focus and activation the whole time. Opening sends no activation messages to ZBrush's (blocked)
  thread, and there is nothing to restore afterwards. Between menus the window stays shown but **DWM-cloaked**:
  uncloak measured 0.46 ms vs 3.0 ms for `SetWindowPos(SHOW)`, and cloaked windows are not hit-tested, so
  clicks go to ZBrush.
* **Trigger keys** come from ZBrush's own keyboard state at the moment it ran the shortcut (one
  `GetKeyboardState`), so the service polls only those keys. (The reference scans all 254 keys with
  `GetAsyncKeyState`; we measured that scan at up to 13 ms under input load.) The release must be seen on 2
  consecutive 4 ms polls, as in the reference. Modifier keys are not trigger keys, so releasing Ctrl first
  in a Ctrl+key shortcut does not fire early.
* **Exactly once / no stuck keys.** Auto-repeat that reached ZBrush's queue is removed by the bridge after
  the menu closes. A trigger key still held after a click/Escape blocks reopening until it is released, and
  a stale repeat arriving just after a close is refused. The bridge then posts a button-less
  `WM_MOUSEMOVE`, so closing never sends a stroke.
* **Idle cost: zero.** The service sleeps in `MsgWaitForMultipleObjects`; the 4 ms timer only runs while a
  menu is open.
* **Recovery.** If the service is missing or was killed, the next press restarts it (≈90–150 ms) and opens
  the menu. The service exits by itself when its ZBrush process exits.
* **ZBrush operations** are performed only by `SculptPie.py` inside ZBrush (the documented
  `set_next_filename` + `Brush:Load Brush` / `Alpha:Import` / `Material:Load`, `press`, `toggle`, `set`).
  Missing files or interface items show a ZBrush note instead of failing silently. A brush SculptPie
  already loaded this session is just re-selected, so your tweaks are kept and there is no reload prompt.

## Build from source
Requirements: Visual Studio 2022+ with "Desktop development with C++" (MSVC v143+, Windows 10/11 SDK).
```
build.bat           -> build\SculptPie.exe, build\SculptPieBridge.dll, build\pf_harness.exe
package.bat         -> dist\SculptPie-1.3.0.zip (Setup, plugin, docs, source)
```
Source layout: `src/common` (JSON, config model, protocol, utilities), `src/bridge` (DLL), `src/app`
(service, overlay, pie engine, icons, library, editor, UI toolkit), `plugin/SculptPie.py`, `tests/`.

## Troubleshooting
| Symptom | Fix |
|---|---|
| No SculptPie entry in ZPlugin | Confirm `SculptPie.py` is in the ZPlugs64 folder printed by the installer and that ZBrush 2027's Python plugins load (another `.py` plugin shows up). See `%LOCALAPPDATA%\SculptPie\Logs\plugin.log`. |
| "SculptPie service unavailable" | Check `SculptPieData\bin\SculptPie.exe` exists and isn't blocked by antivirus; see `service.log` / `bridge.log`. The next press retries automatically. |
| Menu opens and closes immediately | The shortcut key was released before the menu appeared (that is click mode only when nothing was held), or another app took focus. |
| Item does nothing / shows "not found" | The file moved or the interface path differs in your ZBrush version. Fix the target in Settings › Build › properties. |
| Shortcut lost after restart | Store hotkeys: Preferences › Hotkeys › Store. |
| Brush/alpha icon missing | Icons load in the background; the lettered glyph is used when no preview exists. Delete `%LOCALAPPDATA%\SculptPie\Cache` to rebuild. |
| Menu too big or small | Settings › Style › Menu Shape (Item Distance, Min Item Spacing) and Icons & Alphas (Icon Size). DPI is handled per monitor. |
| Update fails with "ZBrush is running" | Close ZBrush: it keeps the bridge DLL loaded. |

## Validation
See [docs/VALIDATION.md](docs/VALIDATION.md) for what was tested, how, the measured numbers, and what still
needs a check inside ZBrush. The reverse-engineering notes are in
[docs/REVERSE_ENGINEERING.md](docs/REVERSE_ENGINEERING.md).

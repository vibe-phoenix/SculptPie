# SculptPie features

## Pie menus

- Twenty independent pie menus (`ZPlugin > SculptPie > PieMenu01` to `PieMenu20`), each on its own shortcut.
- Hold the shortcut, move toward an item and release (or click) to apply it.
- Items: brushes, alphas, materials, ZBrush buttons, switches and sliders (with a set value).
- Up to five rings per level, nested groups that open as an outer ring (**Expand**) or replace the ring (**Switch**).
- Opens in about 2 ms; smooth 90 % to 100 % grow animation, vsync-paced drawing.

## Editor

- Live preview: drag items from the library into the ring, reorder by dragging, multi-select.
- Library of ZBrush brushes, alphas, materials and common interface items, plus your own folders.
- Uses the brush and alpha folders saved in **SculptShelf** (and its thumbnails as icons).
- Easy Renamer for many items at once (find/replace, prefix, suffix).
- Per-menu and per-group ring count, spacing, distance, angles and icon size per ring.
- Undo / redo, autosave.

## Style

- One style editor for every menu: colours, centre ring, pointer, labels, icon look and shadow, screen dim, animation.
- Style presets with import / export.
- Optional AI icon upscaling (Real-ESRGAN, runs locally on the GPU) for crisp menu icons.

## Sharing

- Export a menu as JSON, or **Export With External Brushes (.zip)**: the menu plus every brush, alpha,
  material and custom icon file it uses from outside ZBrush.
- Import accepts that zip and shows a progress bar while it unpacks; the menu loads ready to use.

## Files

- Menus, styles and settings: `Documents\ZBrush\SculptPie` (kept across updates).
- Caches and logs: `%LOCALAPPDATA%\SculptPie`.

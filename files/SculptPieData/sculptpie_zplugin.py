"""SculptPie ZPlugin implementation (imported by ZPlugs64/SculptPie.py).

This lives in a real, importable module (registered in sys.modules) on purpose: ZBrush runs the .py files
in its plugin folder as scripts and does not keep a script's namespace usable for later callbacks, so
button callbacks defined directly in SculptPie.py failed when pressed. Everything a callback needs is held
here, and paths are resolved once at setup (never through __file__ at click time).
"""

import ctypes
import os
import sys
import time
import traceback

from zbrush import commands as zbc

VERSION = "1.0.1"
PALETTE = "ZPlugin:SculptPie"
MENU_COUNT = 20

_data_dir = None      # ...\ZPlugs64\SculptPieData
_log_path = None
_bridge = None
_loaded_brushes = set()
_loaded_alphas = {}


# ---------------------------------------------------------------------------------------------------
# Logging / notes
# ---------------------------------------------------------------------------------------------------
def _resolve_log_path():
    base = os.environ.get("SCULPTPIE_HOME")
    root = os.path.join(base, "Local") if base else os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "SculptPie")
    return os.path.join(root, "Logs", "plugin.log")


def log(msg):
    path = _log_path or _resolve_log_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path) and os.path.getsize(path) > 1024 * 1024:
            os.replace(path, path + ".1")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")
    except Exception:
        try:
            ctypes.windll.kernel32.OutputDebugStringW(f"SculptPie: {msg}\n")
        except Exception:
            pass


def note(text):
    log(text)
    try:
        zbc.show_note(text, "", 2.5)
    except Exception:
        log("show_note failed:\n" + traceback.format_exc())


# ---------------------------------------------------------------------------------------------------
# Native bridge (SculptPieBridge.dll, FileExecute-style exports)
# ---------------------------------------------------------------------------------------------------
_ARGS = [ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p]


class Bridge:
    NAMES = ("PF_Show", "PF_Start", "PF_Ping", "PF_Settings", "PF_Reload", "PF_Shutdown", "PF_LastTimings", "PF_Version")

    def __init__(self, path):
        self.dll = ctypes.CDLL(path)
        for name in self.NAMES:
            fn = getattr(self.dll, name)
            fn.restype = ctypes.c_float
            fn.argtypes = _ARGS
            setattr(self, name, fn)

    def call(self, name, number=0.0, size=8192):
        buf = ctypes.create_string_buffer(size)
        rc = getattr(self, name)(None, float(number), buf, size, None, 0, None)
        return int(rc), buf.value.decode("utf-8", "replace")


def bridge():
    global _bridge
    if _bridge is None:
        path = os.path.join(_data_dir, "bin", "SculptPieBridge.dll")
        if not os.path.isfile(path):
            raise RuntimeError(f"bridge not found: {path}")
        _bridge = Bridge(path)
    return _bridge


# ---------------------------------------------------------------------------------------------------
# Actions - run on ZBrush's main thread inside the button callback
# ---------------------------------------------------------------------------------------------------
def _zdata():
    return os.path.join(os.path.dirname(sys.executable), "ZData")


def _find_preset(subdir, name, exts):
    def norm(s):
        return "".join(c for c in s.lower() if c not in " _-")
    want = norm(name)
    for dirpath, _dirs, files in os.walk(os.path.join(_zdata(), subdir)):
        for f in files:
            stem, ext = os.path.splitext(f)
            if ext.lower() in exts and norm(stem) == want:
                return os.path.join(dirpath, f)
    return None


def _load_file(button, path, answer_reload=False):
    def do():
        zbc.set_next_filename(path)
        zbc.press(button)
    if answer_reload:
        try:
            zbc.press_key("Y", do)   # answers ZBrush's "reset the existing brush?" question
            return
        except Exception:
            log("press_key failed; loading normally:\n" + traceback.format_exc())
    do()


def _brush(target, label):
    if target.lower().startswith("brush:"):
        if zbc.exists(target):
            zbc.press(target)
            return
        path = _find_preset("BrushPresets", target.split(":", 1)[1], (".zbp",))
        if not path:
            note(f"SculptPie: brush '{label}' not found ({target})")
            return
        target = path
    if not os.path.isfile(target):
        note(f"SculptPie: brush file missing: {target}")
        return
    key = os.path.normcase(os.path.abspath(target))
    candidate = "Brush:" + os.path.splitext(os.path.basename(target))[0]
    if key in _loaded_brushes and zbc.exists(candidate):
        zbc.press(candidate)
        return
    _load_file("Brush:Load Brush", target, answer_reload=zbc.exists(candidate))
    _loaded_brushes.add(key)


def _alpha(target, label):
    if target.lower().startswith("alpha:"):
        if zbc.exists(target):
            zbc.press(target)
            return
        path = _find_preset("Alphas", target.split(":", 1)[1], (".psd", ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"))
        if not path:
            note(f"SculptPie: alpha '{label}' not found ({target})")
            return
        target = path
    if not os.path.isfile(target):
        note(f"SculptPie: alpha file missing: {target}")
        return
    key = os.path.normcase(os.path.abspath(target))
    try:
        info = os.stat(target)
        sig = (info.st_size, int(info.st_mtime))
    except OSError:
        sig = None
    known = _loaded_alphas.get(key)
    if known and known[1] == sig and zbc.exists(known[0]):
        zbc.press(known[0])
        return
    candidate = "Alpha:" + os.path.splitext(os.path.basename(target))[0]
    existed = zbc.exists(candidate)
    _load_file("Alpha:Import", target)
    if not existed and zbc.exists(candidate):
        _loaded_alphas[key] = (candidate, sig)


def _material(target, label):
    if target.lower().startswith("material:"):
        if zbc.exists(target):
            zbc.press(target)
            return
        path = _find_preset("Materials", target.split(":", 1)[1], (".zmt",))
        if path:
            _load_file("Material:Load", path)
        else:
            note(f"SculptPie: material '{label}' not found ({target})")
        return
    if not os.path.isfile(target):
        note(f"SculptPie: material file missing: {target}")
        return
    _load_file("Material:Load", target)


def _ui(kind, target, value):
    if not zbc.exists(target):
        note(f"SculptPie: interface item not found: {target}")
        return
    if kind == "button":
        zbc.press(target)
    elif kind == "switch":
        zbc.toggle(target)
    else:
        zbc.set(target, float(value))


def execute(action):
    parts = action.split("\t")
    if len(parts) < 3:
        return
    kind, target, label = parts[0], parts[1], parts[-1]
    value = parts[2] if kind == "slider" and len(parts) >= 4 else 0
    log(f"execute {kind} {target}")
    if kind == "brush":
        _brush(target, label)
    elif kind == "alpha":
        _alpha(target, label)
    elif kind == "material":
        _material(target, label)
    elif kind in ("button", "switch", "slider"):
        _ui(kind, target, value)
    else:
        log(f"unknown action type '{kind}'")


# ---------------------------------------------------------------------------------------------------
# Button callbacks
# ---------------------------------------------------------------------------------------------------
def _menu_index(sender):
    name = str(sender).replace("\\", ":").rsplit(":", 1)[-1].strip()
    digits = "".join(c for c in name if c.isdigit())
    return int(digits) if digits else 0


def make_menu_callback(index):
    # The index is bound per button, so the callback does not depend on how ZBrush formats `sender`.
    def on_menu(sender=None, *args):
        try:
            rc, text = bridge().call("PF_Show", index)
            if rc == 1:
                execute(text)
            elif rc == -1:
                note(f"SculptPie: {text}")
        except Exception as exc:
            log(f"PieMenu{index:02d} failed (sender={sender!r}):\n" + traceback.format_exc())
            note(f"SculptPie: menu {index} failed: {type(exc).__name__}: {exc}")
    return on_menu


def on_settings(sender=None, *args):
    try:
        rc, text = bridge().call("PF_Settings", 0)
        if rc == -1:
            note(f"SculptPie: {text}")
    except Exception as exc:
        log(f"Settings failed (sender={sender!r}):\n" + traceback.format_exc())
        note(f"SculptPie: settings failed: {type(exc).__name__}: {exc}")


# ---------------------------------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------------------------------
_built = False


def setup(data_dir):
    global _data_dir, _log_path, _built
    _data_dir = data_dir
    _log_path = _resolve_log_path()
    try:
        ver = zbc.zbrush_info(0)
    except Exception:
        ver = "?"
    log(f"SculptPie {VERSION} setup (ZBrush {ver}, Python {sys.version.split()[0]}) data={data_dir}")
    if not _built:
        # Callbacks are kept alive by this module (and passed by reference to ZBrush).
        global _callbacks
        _callbacks = [make_menu_callback(i) for i in range(1, MENU_COUNT + 1)]
        existed = zbc.exists(PALETTE)
        ok = zbc.add_subpalette(PALETTE, 0) if not existed else True
        log(f"subpalette {PALETTE}: existed={existed} add={ok}")
        for i in range(1, MENU_COUNT + 1):
            path = f"{PALETTE}:PieMenu{i:02d}"
            pre = zbc.exists(path)
            ok = zbc.add_button(path, f"Pie menu {i}: hold its shortcut, move to an item, release (or click).", _callbacks[i - 1], False, 0.5)
            log(f"button {path}: existed_before={pre} add_button={ok}")
        path = f"{PALETTE}:Settings"
        pre = zbc.exists(path)
        ok = zbc.add_button(path, "Open the SculptPie style and menu editor.", on_settings, False, 1.0)
        log(f"button {path}: existed_before={pre} add_button={ok}")
        _built = True
    try:
        rc, _ = bridge().call("PF_Start")
        log(f"PF_Start -> {rc}")
    except Exception:
        log("PF_Start failed:\n" + traceback.format_exc())


_callbacks = []

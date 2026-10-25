"""SculptPie - fast pie menus for ZBrush 2027. Loader for ZPlugin > SculptPie.

ZBrush runs this file at startup. All logic lives in SculptPieData/sculptpie_zplugin.py, imported as a
regular module so that button callbacks stay valid after this script finishes (see that file).
Assign shortcuts the usual way: Ctrl+Alt+click a PieMenu button, press a key, Preferences > Hotkeys > Store.
"""
import importlib
import os
import sys

_data = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SculptPieData")
if _data not in sys.path:
    sys.path.insert(0, _data)
_mod = sys.modules.get("sculptpie_zplugin") or importlib.import_module("sculptpie_zplugin")
_mod.setup(_data)

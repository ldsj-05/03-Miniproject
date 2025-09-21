import pathlib
import sys
import types
import time as _time
import asyncio as _asyncio

# Ensure src/ is on the path
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

# Provide MicroPython-like time helpers when running on CPython
if not hasattr(_time, "ticks_ms"):
    def _ticks_ms():
        return int(_time.time() * 1000)
    def _ticks_diff(a, b):
        return a - b
    def _sleep_ms(ms):
        _time.sleep(ms / 1000.0)
    _time.ticks_ms = _ticks_ms  # type: ignore[attr-defined]
    _time.ticks_diff = _ticks_diff  # type: ignore[attr-defined]
    _time.sleep_ms = _sleep_ms  # type: ignore[attr-defined]

if not hasattr(_asyncio, "sleep_ms"):
    async def _sleep_ms_async(ms):
        await _asyncio.sleep(ms / 1000.0)
    _asyncio.sleep_ms = _sleep_ms_async  # type: ignore[attr-defined]

# Stub the 'machine' module so we can import light_orchestra on CPython
class _DummyADC:
    def __init__(self, pin):
        self._pin = pin
    def read_u16(self):
        return 12345

class _DummyPWM:
    def __init__(self, pin):
        self._pin = pin
        self._freq = None
        self._duty = 0
    def freq(self, f):
        self._freq = f
    def duty_u16(self, v):
        self._duty = v
    def deinit(self):
        pass

class _DummyPin:
    def __init__(self, n):
        self._n = n

machine_stub = types.SimpleNamespace(ADC=_DummyADC, PWM=_DummyPWM, Pin=_DummyPin)
sys.modules.setdefault("machine", machine_stub)

import light_orchestra  # type: ignore


def test_map_value_linear_mapping():
    mv = light_orchestra.map_value
    assert mv(5, 0, 10, 0, 100) == 50
    assert mv(0, 0, 10, -100, 100) == -100
    assert mv(10, 0, 10, -100, 100) == 100


def test_nearest_white_note_indices():
    idx = light_orchestra.nearest_white_note(262)
    # 262 is in the NOTES_C3_C7 list; it should select that exact index
    assert light_orchestra.NOTES_C3_C7[idx] == 262

    # A frequency between two notes should choose the nearest
    idx2 = light_orchestra.nearest_white_note(300)
    nearest_val = light_orchestra.NOTES_C3_C7[idx2]
    assert abs(nearest_val - 300) <= min(
        abs(262 - 300), abs(294 - 300)
    ) 
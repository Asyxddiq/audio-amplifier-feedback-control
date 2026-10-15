"""
Automatic volume control for the audio amplifier (EE2073 Lab 9).

Runs in a Jupyter notebook on the laptop. Every 10 ms it:
  1. reads the VU meter's DC output (Vvolume) on the STM32's PC0 pin,
  2. compares it with the volume set on a slider,
  3. nudges the VCA control voltage Va up or down by a fixed step,
  4. writes the new Va out on waveform-generator channel W2 (as a DC offset).

Hardware access goes through `VScopeBoard`, the course-provided driver for the
VScope board on the STM32F4 (not included in this repo). Only three of its
methods are used:
    vscope.set_vdc(volts)                        # +/- supply rails
    vscope.generate_wave(ch, shape, amp, f, dc)  # W2 DC offset = Va
    vscope.measure_volt() -> (pc0, pc1)          # 0-3.3 V ADC reads
"""
import time

import numpy as np
from IPython.display import display
from ipywidgets import FloatSlider, ToggleButtons

from repeat_timer import RepeatTimer
from vscope_board import VScopeBoard     # course-provided, not in this repo

vscope = VScopeBoard()

# ---------------------------------------------------------------- UI
set = FloatSlider(description='Set', continuous_update=False, value=10)
vol = FloatSlider(description='Vol', disabled=True)
switch = ToggleButtons(options=['On', 'Off'], value='Off')

# ---------------------------------------------------------------- limits
# THAT 2180C accepts Vc from -0.15 V (loudest) to 0.50 V (softest).
# Va reaches the VCA through a 56k / 3.3k divider: Vc = 3.3/59.3 * Va,
# so Va must stay within about -2.7 V ... 9.0 V.
va_min = -2.7
va_max = 9.0
max_volume = 3.3          # highest voltage PC0 can read

# ---------------------------------------------------------------- controller
delta = 0.05              # Va step per iteration (V)
u = 0.0                   # current Va
vscope.generate_wave(2, None, 0, 1000, u)     # start with Va = 0 V


def control():
    """One step of the step-up-down controller (called every 10 ms)."""
    global u
    v_volume, _ = vscope.measure_volt()       # PC0 = VU meter output
    r0 = set.value                            # target, % of full scale
    z = v_volume / max_volume * 100           # measured, % of full scale
    if z < r0:            # too quiet -> lower Va -> lower Vc -> more gain
        u -= delta
    elif z > r0:          # too loud  -> raise Va -> less gain
        u += delta
    u = np.clip(u, va_min, va_max)
    vscope.generate_wave(2, None, 0, 1000, u)
    vol.value = z


auto = RepeatTimer(0.01, control)


def power_onoff(empty=None):
    """Toggle the amplifier supply and the control loop together."""
    if switch.value == 'On':
        vscope.set_vdc(13.5)          # amplifier on (+/-13.5 V rails)
        time.sleep(0.5)               # avoid serial-port congestion
        auto.start()
    else:
        auto.stop()
        time.sleep(0.5)
        vscope.set_vdc(5.5)           # amplifier off


switch.observe(power_onoff, 'value')
display(set, vol, switch)

"""
Lay out the real oscilloscope captures (VScope, Labs 7-8) as labelled panels.

Raw captures live in visuals/scope/. Usage: python analysis/scope_panels.py
"""
import matplotlib.pyplot as plt
from matplotlib.image import imread

from style import INK, INK2, VIS, note, save, title

SCOPE = VIS / "scope"


def panel(name, head, sub, items, foot):
    fig, axs = plt.subplots(1, len(items), figsize=(12, 7.4))
    fig.subplots_adjust(top=0.78, bottom=0.08, left=0.04, right=0.96,
                        wspace=0.08)
    title(fig, head, sub)
    for ax, (img, label, desc) in zip(axs, items):
        ax.imshow(imread(SCOPE / img))
        ax.axis("off")
        ax.set_title(label, loc="left", fontsize=13, fontweight="bold",
                     color=INK, pad=24)
        ax.text(0, 1.015, desc, transform=ax.transAxes, fontsize=10.5,
                color=INK2, va="bottom")
    note(fig, foot)
    save(fig, name)


panel("scope-vu-meter.png",
      "VU meter on the scope (Lab 7, 1 kHz)",
      "Blue = input Vin (7.8 Vpp). Red = the signal at each rectifier stage.",
      [("lab7-vout1.png", "Vout1: CA3140 output", "one half-cycle passes, "
        "3.46 Vpp"),
       ("lab7-vout2.png", "Vout2: after the 1N914 diodes", "unipolar, "
        "2.65 Vpp, ready for RC smoothing")],
      "Real captures from the VScope oscilloscope, 1 V/div, 500 µs/div.")

panel("scope-system.png",
      "Whole system on the scope (Lab 8, 302 Hz)",
      "Blue = Vsignal into the VCA. Red = Vaudio at the speaker "
      "(two rows of the Lab 8 test table).",
      [("lab8-unity.png", "Va = 3.6 V (Vc = 0.20 V)",
        "4.38 Vpp in -> 4.21 Vpp out, about 0 dB"),
       ("lab8-boost.png", "Va = 2.7 V (Vc = 0.15 V)",
        "2.21 Vpp in -> 5.47 Vpp out, about +8 dB")],
      "Real captures from the VScope oscilloscope, 500 µs/div. "
      "Check each trace's V/div label (top-left) before comparing heights.")

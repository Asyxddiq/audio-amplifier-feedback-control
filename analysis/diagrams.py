"""
Block diagrams and the simplified schematic for the README.

Usage: python analysis/diagrams.py  ->  PNGs in ./visuals
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (Arc, Circle, FancyArrowPatch, FancyBboxPatch,
                                Polygon, Rectangle)

from style import BLUE, INK, INK2, MUTED, PAPER, RED, TINT, note, save, title


# ----------------------------------------------------------------- helpers
def canvas(w, h, xlim, ylim):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.8])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, head, sub=None, color=INK, fs=12.5, fill=None):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                fc=fill or TINT.get(color, "#FBFAF6"),
                                ec=color, lw=1.8))
    dy = 0.17 if sub else 0
    ax.text(x, y + dy, head, ha="center", va="center", fontsize=fs,
            fontweight="bold", color=INK)
    if sub:
        ax.text(x, y - 0.24, sub, ha="center", va="center", fontsize=10,
                color=INK2)


def arrow(ax, p1, p2, color=INK, lw=1.8, ls="-", style="-|>", rad=0):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=15,
                                 color=color, lw=lw, linestyle=ls,
                                 shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def line(ax, pts, color=INK, lw=1.6, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round")


# ----------------------------------------------------------------- 1. architecture
def architecture():
    fig, ax = canvas(14, 6.4, (0, 14), (0, 6.4))
    title(fig, "System architecture",
          "Every block named by the part that does the job")
    y = 4.6
    box(ax, 1.25, y, 2.1, 1.15, "Audio in", "laptop audio out", INK)
    box(ax, 4.15, y, 2.5, 1.15, "VCA", "THAT 2180C + OP275", BLUE)
    box(ax, 7.25, y, 2.5, 1.15, "Power amp", "LM380N, 34 dB", BLUE)
    box(ax, 10.15, y, 2.1, 1.15, "Speaker", "Vaudio", BLUE)
    for a, b in [(2.3, 2.9), (5.4, 6.0), (8.5, 9.1)]:
        arrow(ax, (a, y), (b, y))
    box(ax, 10.15, 1.5, 2.3, 1.15, "VU meter", "CA3140 + 2x 1N914", RED)
    box(ax, 7.25, 1.5, 2.5, 1.15, "STM32 + VScope", "PC0 in, W2 out", RED)
    box(ax, 4.15, 1.5, 2.5, 1.15, "Python (Jupyter)", "step-up-down loop",
        RED)
    line(ax, [(10.15, y - 0.58), (10.15, 2.08)], RED)
    arrow(ax, (10.15, 2.6), (10.15, 2.08), RED)
    arrow(ax, (9.0, 1.5), (8.5, 1.5), RED)
    arrow(ax, (6.0, 1.75), (5.4, 1.75), RED)
    arrow(ax, (5.4, 1.25), (6.0, 1.25), RED)
    line(ax, [(7.25, 2.08), (7.25, 2.95), (4.15, 2.95)], RED)
    arrow(ax, (4.15, 2.95), (4.15, y - 0.58), RED)
    ax.text(10.3, 3.1, "Vaudio", fontsize=10, color=INK2)
    ax.text(8.75, 1.3, "Vvolume", fontsize=10, color=INK2, ha="center",
            va="top")
    ax.text(5.7, 2.0, "USB", fontsize=10, color=INK2, ha="center")
    ax.text(4.4, 3.05, "Va from W2  ->  56k/3.3k divider  ->  Vc", fontsize=10,
            color=INK2, ha="left", va="bottom")
    # legend
    for i, (c, lab) in enumerate([(BLUE, "Audio path (Labs 5-6)"),
                                  (RED, "Feedback path (Labs 7, 9)")]):
        ax.add_patch(Rectangle((11.75, 4.85 - i * 0.5), 0.3, 0.22, fc=c,
                               ec="none"))
        ax.text(12.15, 4.96 - i * 0.5, lab, fontsize=10.5, color=INK2,
                va="center")
    save(fig, "system-architecture.png")


# ----------------------------------------------------------------- 2. open vs closed
def open_vs_closed():
    fig = plt.figure(figsize=(14, 5.4))
    title(fig, "Lab 8 vs Lab 9: taking the person out of the loop")
    for k, (head, sub, nodes, col) in enumerate([
        ("Lab 8: manual (open loop)", "You set Va by hand",
         ["Input", "VCA + PA", "Speaker", "You read VU,\nchange Va"], INK2),
        ("Lab 9: automatic (closed loop)", "Python sets Va every 10 ms",
         ["Input", "VCA + PA", "Speaker", "VU -> PC0 ->\nPython -> W2"], RED),
    ]):
        ax = fig.add_axes([0.03 + k * 0.49, 0.04, 0.45, 0.76])
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 4.2)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.text(0.1, 4.0, head, fontsize=14, fontweight="bold", color=INK,
                va="top")
        ax.text(0.1, 3.45, sub, fontsize=11, color=INK2, va="top")
        xs = [0.8, 2.75, 4.7]
        for x, n in zip(xs, nodes[:3]):
            box(ax, x, 2.2, 1.45, 0.8, n, None, BLUE, fs=11)
        arrow(ax, (1.52, 2.2), (2.02, 2.2))
        arrow(ax, (3.48, 2.2), (3.97, 2.2))
        box(ax, 4.7, 0.55, 2.0, 0.85, nodes[3], None, col, fs=10.5)
        if k == 0:
            line(ax, [(4.7, 1.8), (4.7, 0.98)], INK2, ls="--")
            line(ax, [(3.7, 0.55), (2.75, 0.55), (2.75, 1.8)], INK2, ls="--")
            ax.text(5.85, 1.35, "by hand", color=INK2, fontsize=10)
        else:
            arrow(ax, (4.7, 1.8), (4.7, 0.98), RED)
            line(ax, [(3.7, 0.55), (2.75, 0.55)], RED)
            arrow(ax, (2.75, 0.55), (2.75, 1.8), RED)
            ax.text(5.85, 1.35, "automatic", color=RED, fontsize=10)
    save(fig, "manual-vs-automatic.png")


# ----------------------------------------------------------------- 3. controller
def controller():
    fig, ax = canvas(14, 6.6, (0, 14), (0, 6.6))
    title(fig, "The controller (Lab 9)",
          "A step-up-down loop: every tick, nudge Va by a fixed step towards "
          "the set volume")
    y = 4.4
    box(ax, 1.4, y, 2.4, 1.2, "Read VU", "v = PC0 voltage", RED)
    box(ax, 4.5, y, 2.6, 1.2, "Scale to %", "z = v / 3.3 V x 100", INK)
    ax.add_patch(Polygon([[6.6, y], [7.85, y + 0.9], [9.1, y],
                          [7.85, y - 0.9]], closed=True, fc=TINT[INK],
                         ec=INK, lw=1.8))
    ax.text(7.85, y, "z vs set\npoint r0", ha="center", va="center",
            fontsize=11.5, fontweight="bold")
    box(ax, 11.6, y + 0.95, 3.6, 0.85, "z < r0 (too quiet): Va -= 0.05 V",
        None, BLUE, fs=10.5)
    box(ax, 11.6, y - 0.4, 3.6, 0.85, "z > r0 (too loud): Va += 0.05 V",
        None, BLUE, fs=10.5)
    arrow(ax, (2.6, y), (3.2, y))
    arrow(ax, (5.8, y), (6.6, y))
    arrow(ax, (9.1, y), (9.8, y + 0.95), rad=-0.2)
    arrow(ax, (9.1, y), (9.8, y - 0.4), rad=0.15)
    box(ax, 9.9, 1.4, 3.5, 1.05, "Clip Va to -2.7 ... 9.0 V",
        "keeps Vc in -0.15 ... 0.5 V", INK)
    box(ax, 5.2, 1.4, 3.6, 1.05, "Write Va to W2", "then wait 10 ms", RED)
    line(ax, [(13.4, y + 0.95), (13.7, y + 0.95), (13.7, 1.4)], MUTED)
    line(ax, [(13.4, y - 0.4), (13.7, y - 0.4)], MUTED)
    arrow(ax, (13.7, 1.4), (11.65, 1.4), MUTED)
    arrow(ax, (8.15, 1.4), (7.0, 1.4), MUTED)
    line(ax, [(3.4, 1.4), (1.4, 1.4)], MUTED)
    arrow(ax, (1.4, 1.4), (1.4, y - 0.6), MUTED)
    ax.text(2.4, 1.6, "repeat", color=INK2, fontsize=10.5)
    ax.text(7.85, y + 1.15, "no tolerance band: it always moves",
            fontsize=10, color=RED, ha="center")
    note(fig, "Lower Va = lower Vc = more gain. Va is the W2 DC offset; "
         "a 56k/3.3k divider turns it into Vc for the THAT 2180C.")
    save(fig, "control-algorithm.png")


# ----------------------------------------------------------------- 4. schematic
def resistor(ax, p1, p2, label=None, lpos="above"):
    (x1, y1), (x2, y2) = p1, p2
    L = np.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    body = 0.6
    a = (L - body) / 2
    pts = [(x1, y1), (x1 + ux * a, y1 + uy * a)]
    for i in range(1, 7):
        t = a + body * i / 7
        s = 0.13 * (1 if i % 2 else -1)
        pts.append((x1 + ux * t + nx * s, y1 + uy * t + ny * s))
    pts += [(x1 + ux * (L - a), y1 + uy * (L - a)), (x2, y2)]
    line(ax, pts, lw=1.4)
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if abs(uy) > 0.5:
            ax.text(mx + 0.22, my, label, fontsize=9.5, va="center")
        else:
            ax.text(mx, my + (0.22 if lpos == "above" else -0.22), label,
                    fontsize=9.5, ha="center",
                    va="bottom" if lpos == "above" else "top")


def cap(ax, p1, p2, label=None, polar=False):
    (x1, y1), (x2, y2) = p1, p2
    vert = abs(x2 - x1) < 1e-6
    if vert:
        m = (y1 + y2) / 2
        line(ax, [(x1, y1), (x1, m + 0.08)], lw=1.4)
        line(ax, [(x1, m - 0.08), (x1, y2)], lw=1.4)
        line(ax, [(x1 - 0.22, m + 0.08), (x1 + 0.22, m + 0.08)], lw=2)
        line(ax, [(x1 - 0.22, m - 0.08), (x1 + 0.22, m - 0.08)], lw=2)
        if label:
            ax.text(x1 + 0.3, m, label, fontsize=9.5, va="center")
    else:
        m = (x1 + x2) / 2
        line(ax, [(x1, y1), (m - 0.08, y1)], lw=1.4)
        line(ax, [(m + 0.08, y1), (x2, y2)], lw=1.4)
        line(ax, [(m - 0.08, y1 - 0.22), (m - 0.08, y1 + 0.22)], lw=2)
        line(ax, [(m + 0.08, y1 - 0.22), (m + 0.08, y1 + 0.22)], lw=2)
        if label:
            ax.text(m, y1 + 0.3, label, fontsize=9.5, ha="center",
                    va="bottom")
        if polar:
            ax.text(m - 0.22, y1 + 0.05, "+", fontsize=8, ha="right")


def gnd(ax, x, y):
    line(ax, [(x, y), (x, y - 0.15)], lw=1.4)
    for i, w in enumerate((0.22, 0.14, 0.06)):
        line(ax, [(x - w, y - 0.15 - i * 0.07), (x + w, y - 0.15 - i * 0.07)],
             lw=1.4)


def amp(ax, x, y, label, w=1.4, h=1.3, color=INK, signs=True):
    ax.add_patch(Polygon([[x, y + h / 2], [x, y - h / 2], [x + w, y]],
                         closed=True, fc="#FBFAF6", ec=color, lw=1.8))
    ax.text(x + w * 0.38, y, label, fontsize=9.5, fontweight="bold",
            ha="center", va="center")
    if signs:
        ax.text(x + 0.08, y + h / 4, "–", fontsize=10, va="center")
        ax.text(x + 0.08, y - h / 4, "+", fontsize=10, va="center")


def diode(ax, x1, x2, y, label=None):
    m = (x1 + x2) / 2
    line(ax, [(x1, y), (m - 0.15, y)], lw=1.4)
    line(ax, [(m + 0.15, y), (x2, y)], lw=1.4)
    ax.add_patch(Polygon([[m - 0.15, y + 0.17], [m - 0.15, y - 0.17],
                          [m + 0.15, y]], closed=True, fc=INK, ec=INK))
    line(ax, [(m + 0.15, y + 0.17), (m + 0.15, y - 0.17)], lw=1.8)
    if label:
        ax.text(m, y + 0.28, label, fontsize=9.5, ha="center", va="bottom")


def dot(ax, x, y):
    ax.add_patch(Circle((x, y), 0.06, fc=INK, ec=INK, zorder=5))


def term(ax, x, y, label, right=False, color=INK):
    ax.add_patch(Circle((x, y), 0.09, fc=PAPER, ec=color, lw=1.6, zorder=5))
    ax.text(x + (0.2 if right else -0.2), y, label, fontsize=11,
            fontweight="bold", color=color, ha="left" if right else "right",
            va="center")


def schematic():
    fig, ax = canvas(18, 7.6, (-1.6, 23.8), (0.6, 10.6))
    title(fig, "Circuit schematic (simplified)",
          "Signal path of the full system; supply decoupling capacitors "
          "omitted for clarity")
    y = 5
    # zones
    for x0, x1, lab, c in [(-1.2, 8.75, "VCA", BLUE), (8.85, 15.0,
                           "Power amp", BLUE), (15.1, 23.3, "VU meter", RED)]:
        ax.add_patch(Rectangle((x0, 1.15), x1 - x0, 7.55, fc="none", ec=c,
                               lw=1.1, ls=(0, (4, 3))))
        ax.text(x0 + 0.15, 1.3, lab, fontsize=12.5, fontweight="bold",
                color=c, va="bottom")
    # input + VCA
    term(ax, 0, y, "Vsignal", color=BLUE)
    cap(ax, (0.09, y), (1.2, y), "10µ", polar=True)
    resistor(ax, (1.2, y), (2.9, y), "20k")
    amp(ax, 2.9, y, "2180C", signs=False)
    ax.text(3.0, y - 0.95, "THAT", fontsize=9, color=INK2)
    term(ax, 0, 8.0, "Va (W2)", color=RED)
    resistor(ax, (0.09, 8.0), (2.6, 8.0), "56k")
    dot(ax, 2.6, 8.0)
    resistor(ax, (2.6, 8.0), (4.4, 8.0), "3.3k")
    gnd(ax, 4.4, 8.0)
    line(ax, [(2.6, 8.0), (2.6, 6.4), (3.35, 6.4), (3.35, y + 0.43)])
    ax.text(2.7, 6.55, "Vc", fontsize=10.5, color=RED, fontweight="bold")
    # OP275 I-to-V
    line(ax, [(4.3, y), (5.6, y)])
    dot(ax, 5.2, y)
    amp(ax, 5.6, y - 0.33, "OP275", w=1.5)
    line(ax, [(5.6, y - 0.66), (5.3, y - 0.66), (5.3, y - 1.1)])
    gnd(ax, 5.3, y - 1.1)
    line(ax, [(5.2, y), (5.2, 6.6)])
    resistor(ax, (5.2, 6.6), (7.6, 6.6), "20k")
    line(ax, [(5.2, 6.6), (5.2, 7.4)])
    cap(ax, (5.2, 7.4), (7.6, 7.4), "22p")
    line(ax, [(7.6, 7.4), (7.6, y)])
    line(ax, [(7.1, y - 0.33), (7.6, y - 0.33), (7.6, y), (8.0, y)])
    dot(ax, 7.6, y)
    # PA
    cap(ax, (8.0, y), (9.4, y), "10µ", polar=True)
    dot(ax, 9.7, y)
    line(ax, [(9.4, y), (10.3, y)])
    resistor(ax, (9.7, y), (9.7, 2.7), "1M")
    gnd(ax, 9.7, 2.7)
    amp(ax, 10.3, y, "LM380N", w=1.7, h=1.5, color=BLUE, signs=False)
    line(ax, [(12.0, y), (12.4, y)])
    dot(ax, 12.4, y)
    resistor(ax, (12.4, y), (12.4, 3.4), "22")
    cap(ax, (12.4, 3.4), (12.4, 2.4), "0.1µ")
    gnd(ax, 12.4, 2.4)
    cap(ax, (12.4, y), (13.8, y), "100µ", polar=True)
    dot(ax, 14.2, y)
    line(ax, [(13.8, y), (15.6, y)])
    ax.text(14.2, y + 0.3, "Vaudio", fontsize=10.5, fontweight="bold",
            color=BLUE, ha="center", va="bottom")
    # speaker
    line(ax, [(14.2, y), (14.2, 3.6)])
    ax.add_patch(Rectangle((14.05, 3.0), 0.3, 0.6, fc=PAPER, ec=INK, lw=1.4))
    ax.add_patch(Polygon([[14.35, 3.6], [14.75, 3.9], [14.75, 2.7],
                          [14.35, 3.0]], closed=True, fc=PAPER, ec=INK,
                         lw=1.4))
    line(ax, [(14.2, 3.0), (14.2, 2.5)])
    gnd(ax, 14.2, 2.5)
    ax.text(14.45, 2.05, "Speaker", fontsize=9.5, ha="center", va="top",
            color=INK2)
    # VU meter
    resistor(ax, (15.6, y), (16.9, y), "4.7k")
    dot(ax, 16.9, y)
    line(ax, [(16.9, y), (16.9, y + 0.33), (17.3, y + 0.33)])
    amp(ax, 17.3, y, "CA3140", w=1.6, color=RED)
    line(ax, [(17.3, y - 0.33), (17.0, y - 0.33), (17.0, y - 0.9)])
    gnd(ax, 17.0, y - 0.9)
    line(ax, [(16.9, y + 0.33), (16.9, 6.6)])
    resistor(ax, (16.9, 6.6), (19.45, 6.6), "3.3k")
    line(ax, [(19.45, 6.6), (19.45, y)])
    diode(ax, 18.9, 19.45, y)
    diode(ax, 19.45, 20.6, y, "1N914 x2")
    dot(ax, 19.45, y)
    resistor(ax, (19.45, y), (19.45, 2.8), "18k")
    gnd(ax, 19.45, 2.8)
    dot(ax, 20.6, y)
    resistor(ax, (20.6, y), (20.6, 2.8), "56k")
    gnd(ax, 20.6, 2.8)
    line(ax, [(20.6, y), (21.7, y)])
    dot(ax, 21.5, y)
    cap(ax, (21.5, y), (21.5, 2.8), "10µ")
    gnd(ax, 21.5, 2.8)
    term(ax, 22.4, y, "", color=RED)
    line(ax, [(21.7, y), (22.31, y)])
    ax.text(22.4, y + 0.3, "Vvolume", fontsize=10.5, fontweight="bold",
            color=RED, ha="center", va="bottom")
    ax.text(22.4, y - 0.3, "-> PC0", fontsize=10, color=INK2, ha="center",
            va="top")
    # supply rail with inductor
    ry = 9.55
    line(ax, [(0.5, ry), (9.85, ry)], INK2, lw=1.4)
    for i in range(4):
        ax.add_patch(Arc((10.0 + i * 0.3, ry), 0.3, 0.4, theta1=0,
                         theta2=180, color=INK, lw=1.6))
    line(ax, [(11.05, ry), (22, ry)], INK2, lw=1.4)
    ax.text(10.45, ry + 0.3, "820 µH", fontsize=10, ha="center",
            va="bottom", fontweight="bold")
    ax.text(0.5, ry + 0.15, "+13.5 V  (VCA rail, with -13.5 V)", fontsize=9.5,
            color=INK2, va="bottom")
    ax.text(22, ry + 0.15, "+13.5 V  (PA + VU rail)", fontsize=9.5,
            color=INK2, va="bottom", ha="right")
    note(fig, "Redrawn from the EE2073 Lab 8 circuit. A 22 Ω resistor stood in "
         "for the speaker during measurements. LM380N pin 7 (input ground) "
         "has its own rail, GND1, apart from the output-stage grounds (GND2).")
    save(fig, "circuit-schematic.png")


# ----------------------------------------------------------------- 5. labs timeline
def timeline():
    fig, ax = canvas(14, 3.4, (0, 14), (1.0, 3.75))
    title(fig, "Nine lab sessions, one system")
    labs = [("1-2", "STM32 +\nMicroPython", INK2),
            ("3", "FFT and\nsampling", INK2),
            ("4", "Instrument\ncalibration", INK2),
            ("5", "VCA", BLUE), ("6", "Power amp", BLUE),
            ("7", "VU meter", RED), ("8", "Integrate\n+ speaker", BLUE),
            ("9", "Automatic\ncontrol", RED)]
    xs = np.linspace(0.9, 13.1, len(labs))
    line(ax, [(xs[0], 2.6), (xs[-1], 2.6)], "#D8D2C4", lw=4)
    for x, (n, lab, c) in zip(xs, labs):
        ax.add_patch(Circle((x, 2.6), 0.42, fc=c, ec=PAPER, lw=3, zorder=3))
        ax.text(x, 2.6, n, color="white", fontweight="bold", fontsize=12,
                ha="center", va="center", zorder=4)
        ax.text(x, 1.95, lab, ha="center", va="top", fontsize=11, color=INK)
    ax.text(xs[0] - 0.4, 3.35, "Foundations: controlling the hardware "
            "from Python", fontsize=10.5, color=INK2)
    ax.text(xs[3] - 0.4, 3.35, "Building the audio system", fontsize=10.5,
            color=INK2)
    save(fig, "lab-timeline.png")


# ----------------------------------------------------------------- 6. timer
def timer_timing():
    fig, ax = canvas(14, 4.4, (0, 14), (0, 4.0))
    title(fig, "Why the loop is not exactly every 10 ms",
          "RepeatTimer only schedules the next call after control() "
          "finishes")
    x = 0.6
    ax.text(0.6, 3.2, "time  ->", fontsize=10.5, color=INK2)
    for i in range(4):
        ax.add_patch(Rectangle((x, 1.8), 2.0, 0.7, fc=TINT[INK], ec=INK2,
                               lw=1.2))
        ax.text(x + 1.0, 2.15, "wait 10 ms", ha="center", va="center",
                fontsize=10.5)
        w = [0.55, 0.8, 0.5, 1.1][i]
        ax.add_patch(Rectangle((x + 2.0, 1.8), w, 0.7, fc=TINT[RED],
                               ec=RED, lw=1.2))
        ax.text(x + 2.0 + w / 2, 1.5, "run", ha="center", va="top",
                fontsize=9.5, color=RED)
        x += 2.0 + w + 0.12
    ax.text(0.6, 0.7, "Each cycle = 10 ms + the time control() takes "
            "(USB read, USB write, Python) + OS scheduling jitter.",
            fontsize=11, color=INK)
    note(fig, "Illustration (durations not to scale).")
    save(fig, "loop-timing.png")


if __name__ == "__main__":
    architecture()
    open_vs_closed()
    controller()
    schematic()
    timeline()
    timer_timing()

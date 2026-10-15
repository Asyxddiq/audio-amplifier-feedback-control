"""
Top-down drawing of the finished breadboard (Lab 8-9 build).

Parts and values follow the course circuit; exact hole positions are
simplified. Usage: python analysis/breadboard_topview.py
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

from style import BLUE, INK, INK2, PAPER, RED, save

BOARD = "#FBFAF6"
HOLE = "#CBC6BA"
W_YEL, W_ORG, W_BLU, W_GRN, W_GRY = ("#E3B21B", "#E07B28", "#2F5FB3",
                                      "#3C8A4A", "#8F8D88")
COLS = 63

fig = plt.figure(figsize=(16, 7.6))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(-7, 75)
ax.set_ylim(-8.2, 30.8)
ax.set_aspect("equal")
ax.axis("off")


# ------------------------------------------------------------- board
ax.add_patch(FancyBboxPatch((-1.4, -3.4), COLS + 1.8, 21.6,
                            boxstyle="round,pad=0,rounding_size=0.8",
                            fc=BOARD, ec=INK, lw=1.4, zorder=1))
for r in list(range(0, 5)) + list(range(7, 12)):
    ax.scatter(np.arange(COLS), np.full(COLS, r + 1), s=4, c=HOLE, zorder=2)
rail_x = [c for c in range(COLS) if c % 6 != 5]
for y in (14.3, 15.3, -1.3, -2.3):
    ax.scatter(rail_x, np.full(len(rail_x), y), s=4, c=HOLE, zorder=2)
ax.add_patch(Rectangle((-0.5, 6.2), COLS, 0.6, fc="#ECE8DD", ec="none",
                       zorder=2))
ax.plot([0, COLS - 1], [16.0, 16.0], color=RED, lw=1.1, zorder=2)
ax.plot([0, COLS - 1], [13.6, 13.6], color=W_BLU, lw=1.1, zorder=2)
ax.plot([0, COLS - 1], [-0.6, -0.6], color=RED, lw=1.1, zorder=2)
ax.plot([0, COLS - 1], [-3.0, -3.0], color=W_BLU, lw=1.1, zorder=2)
ax.text(-1.0, 15.3, "+13.5 V", fontsize=9, ha="right", va="center",
        color=RED)
ax.text(-1.0, 14.3, "GND", fontsize=9, ha="right", va="center", color=INK2)
ax.text(-1.0, -1.3, "-13.5 V", fontsize=9, ha="right", va="center",
        color=RED)
ax.text(-1.0, -2.3, "GND", fontsize=9, ha="right", va="center", color=INK2)


# ------------------------------------------------------------- parts
def dip(x, label, pins=8):
    n = pins // 2
    ax.add_patch(FancyBboxPatch((x - 0.4, 4.55), n - 0.2, 3.9,
                                boxstyle="round,pad=0,rounding_size=0.15",
                                fc="#262624", ec=INK, lw=1, zorder=5))
    ax.add_patch(Circle((x - 0.05, 6.5), 0.2, fc="#55534E", ec="none",
                        zorder=6))
    for i in range(n):
        for yy in (4.45, 8.55):
            ax.add_patch(Rectangle((x + i - 0.12, yy - 0.15), 0.24, 0.3,
                                   fc="#B9B5AA", ec="none", zorder=4))
    ax.text(x + (n - 1) / 2, 6.5, label, color="white", fontsize=8.5,
            ha="center", va="center", zorder=7, fontweight="bold")


def sip(x, y, n, label):
    ax.add_patch(Rectangle((x - 0.35, y - 0.45), n - 0.3, 0.9, fc="#262624",
                           ec=INK, lw=1, zorder=5))
    ax.text(x + (n - 1) / 2 - 0.15, y, label, color="white", fontsize=8.5,
            ha="center", va="center", zorder=6, fontweight="bold")


def res(x1, y1, x2, y2, bands=("#7A4A1E", INK, "#C23B2E")):
    ax.plot([x1, x2], [y1, y2], color="#9A968C", lw=1.2, zorder=5)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    vert = abs(x2 - x1) < abs(y2 - y1)
    w, h = (0.55, 1.5) if vert else (1.5, 0.55)
    ax.add_patch(FancyBboxPatch((mx - w / 2, my - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.22",
                                fc="#D9C08F", ec=INK2, lw=0.8, zorder=6))
    for k, c in enumerate(bands):
        o = -0.4 + k * 0.38
        if vert:
            ax.plot([mx - w / 2, mx + w / 2], [my + o] * 2, color=c, lw=1.6,
                    zorder=7)
        else:
            ax.plot([mx + o] * 2, [my - h / 2, my + h / 2], color=c, lw=1.6,
                    zorder=7)


def ecap(x, y, r=0.7):
    ax.add_patch(Circle((x, y), r, fc="#2C3E66", ec=INK, lw=1, zorder=6))
    ax.add_patch(Rectangle((x + r * 0.3, y - r * 0.85), r * 0.35, r * 1.7,
                           fc="#C8CEDB", ec="none", zorder=7))


def ccap(x, y):
    ax.add_patch(Circle((x, y), 0.4, fc="#D98A2B", ec=INK2, lw=0.8,
                        zorder=6))


def diode(x, y):
    ax.plot([x - 1.1, x + 1.1], [y, y], color="#9A968C", lw=1.2, zorder=5)
    ax.add_patch(Rectangle((x - 0.55, y - 0.22), 1.1, 0.44, fc="#C9452F",
                           ec=INK2, lw=0.6, zorder=6))
    ax.add_patch(Rectangle((x + 0.3, y - 0.22), 0.16, 0.44, fc="#222222",
                           ec="none", zorder=7))


def wire(pts, color, lw=2.6, z=8):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
            solid_joinstyle="round", zorder=z)
    for x, y in (pts[0], pts[-1]):
        ax.add_patch(Circle((x, y), 0.2, fc=INK, ec="none", zorder=z + 1))


def tag(x, y, text, color=INK, fs=10.5):
    ax.text(x, y, text, fontsize=fs, ha="center", va="center", color=color,
            fontweight="bold", zorder=12,
            bbox=dict(boxstyle="round,pad=0.25", fc=PAPER, ec=color, lw=1))


# ---- supply decoupling (100µ + 0.1µ on each rail)
ecap(1.0, 15.0, 0.75)
ccap(2.6, 14.8)
ecap(1.0, -1.8, 0.75)
ccap(2.6, -1.8)

# ---- VCA: Va divider, THAT 2180C (SIP), OP275
res(3, 11, 7, 11)                     # 56k
res(8, 10, 8, 14.3)                   # 3.3k to GND
sip(9, 2.5, 8, "THAT 2180C")
ecap(4.5, 2.5, 0.6)                   # 10µ input coupling
res(5.5, 2.5, 8.5, 2.5)               # 20k
res(10, 0, 10, -2.3)                  # 5.1k to -13.5
dip(19, "OP275", 8)
res(18, 10.5, 22, 10.5)               # 20k feedback
ccap(20, 11.6)                        # 22p
ccap(14.5, 10.5)                      # 0.1µ
wire([(14, 16.0), (14, 8.6)], RED, lw=2)
wire([(9, 2.9), (9, 7.0), (11, 7.0), (11, 9.4)], W_GRN, lw=2)
wire([(17, 2.5), (19, 4.4)], W_BLU)
wire([(20, 4.4), (20, -0.6)], RED, lw=2)

# ---- 820 µH inductor splitting the + rail
ax.add_patch(FancyBboxPatch((27.2, 15.75), 2.6, 0.5,
                            boxstyle="round,pad=0,rounding_size=0.24",
                            fc="#4E9A55", ec=INK2, lw=0.8, zorder=9))
for k in range(3):
    ax.plot([27.9 + k * 0.6] * 2, [15.75, 16.25], color="#C9A23A", lw=1.6,
            zorder=10)

# ---- PA: LM380N (14-pin)
ecap(24, 2.5, 0.6)                    # 10µ coupling
res(25.5, 0.2, 25.5, -2.3)            # 1M
dip(28, "LM380N", 14)
ecap(31.0, 11.5, 0.85)                # 100µ supply
ccap(33.0, 11.3)
ecap(37, 2.6, 0.85)                   # 100µ output coupling
res(35, 0.5, 35, -2.3)                # 22 ohm (with 0.1µ)
ccap(36.2, 0.6)
wire([(22, 4.4), (23.4, 2.5)], W_BLU)
wire([(32, 16.0), (32, 8.6)], RED, lw=2)
wire([(30.5, 14.3), (30.5, 8.6)], INK, lw=2)
wire([(33, 4.4), (36.2, 2.6)], W_ORG)

# ---- VU meter: CA3140, 2x 1N914, 18k, 56k, 10µ
res(39.5, 2.5, 43.5, 2.5)             # 4.7k
dip(45, "CA3140", 8)
res(44, 10.8, 49, 10.8)               # 3.3k feedback
diode(51, 3)
diode(54.5, 3)
res(52.8, 2.6, 52.8, -2.3)            # 18k
res(56.5, 2.6, 56.5, -2.3)            # 56k
ecap(58.5, 1.2, 0.7)                  # 10µ
ccap(48, 12.6)
wire([(37.85, 2.6), (39.5, 2.5)], W_ORG)
wire([(46, 16.0), (46, 8.6)], RED, lw=2)
wire([(47, 4.4), (47, -2.3)], INK, lw=2)

# ---- off-board: speaker, VScope/STM32
sx, sy = 37.5, 25.0
ax.add_patch(Circle((sx, sy), 2.8, fc="#3A3A38", ec=INK, lw=1.4, zorder=5))
for r in (2.0, 1.25):
    ax.add_patch(Circle((sx, sy), r, fc="none", ec="#77746C", lw=1,
                        zorder=6))
ax.add_patch(Circle((sx, sy), 0.6, fc="#55534E", ec="none", zorder=6))
wire([(38.5, 3.4), (38.5, 22.3)], W_GRY)
wire([(36.2, 14.3), (36.2, 22.3)], INK, lw=2)

bx, by = 50, 20.5
ax.add_patch(FancyBboxPatch((bx, by), 15, 8.2,
                            boxstyle="round,pad=0,rounding_size=0.4",
                            fc="#2F7A4C", ec=INK, lw=1.2, zorder=5))
for i in range(13):
    ax.add_patch(Rectangle((bx + 0.9 + i * 1.03, by + 7.1), 0.5, 0.5,
                           fc="#D7C27A", ec="none", zorder=6))
ax.add_patch(Rectangle((bx + 5.0, by + 2.2), 4.8, 3.0, fc="#1E1E1C",
                       ec="none", zorder=6))
ax.text(bx + 7.4, by + 3.7, "STM32", color="#E8E5DC", fontsize=9,
        ha="center", va="center", zorder=7, fontweight="bold")
wire([(59.2, 1.2), (66.6, 1.2), (66.6, 23.0), (65, 23.0)], RED)
wire([(52, 20.5), (52, 19.2), (3, 19.2), (3, 11)], RED)
wire([(55, 20.5), (55, 18.0), (1.5, 18.0), (1.5, 2.5), (3.9, 2.5)], W_YEL)
ax.text(20, 19.5, "W2 -> Va (control voltage)", fontsize=10, color=RED,
        ha="center", va="bottom")
ax.text(20, 17.7, "audio in (Vsignal)", fontsize=10, color="#9A7A10",
        ha="center", va="top")
ax.text(67.2, 12, "Vvolume\n-> PC0", fontsize=10, color=RED, va="center")

# ---- labels
tag(11.5, -5.3, "VCA", BLUE)
ax.text(11.5, -6.8, "THAT 2180C + OP275", fontsize=10, color=INK2,
        ha="center")
tag(31, -5.3, "Power amp", BLUE)
ax.text(31, -6.8, "LM380N, 34 dB spec", fontsize=10, color=INK2,
        ha="center")
tag(51, -5.3, "VU meter", RED)
ax.text(51, -6.8, "CA3140 + 1N914 x2", fontsize=10, color=INK2,
        ha="center")
for x0, x1 in ((-0.8, 23.2), (23.6, 38.6), (39, 62.4)):
    ax.plot([x0, x1], [-4.35, -4.35], color=INK2, lw=1)
ax.text(28.5, 16.5, "820 µH", fontsize=9, ha="center", va="bottom",
        fontweight="bold", color=INK)
ax.text(sx + 3.3, sy + 0.7, "Speaker", fontsize=13, fontweight="bold",
        color=INK, va="center")
ax.text(sx + 3.3, sy - 0.8, "replaced the 22 Ω\ntest load in Lab 8",
        fontsize=10, color=INK2, va="center")
ax.text(bx + 7.5, by + 6.2, "VScope board on STM32F4", fontsize=12,
        fontweight="bold", color="white", ha="center", va="center",
        zorder=12)
ax.text(bx + 7.5, by + 1.1, "USB to the laptop running Jupyter",
        fontsize=9.5, color="#E8E5DC", ha="center", va="center", zorder=12)

ax.text(-6.5, 30.2, "Finished circuit, top view", fontsize=22,
        fontweight="bold", color=INK, va="top")
ax.text(-6.5, 28.0, "Real parts and values; hole positions simplified",
        fontsize=11.5, color=INK2, va="top", style="italic")

save(fig, "circuit-top-view.png")

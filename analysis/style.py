"""Shared look for every figure in the repo (engineering-sheet style)."""
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VIS = ROOT / "visuals"
VIS.mkdir(exist_ok=True)

PAPER = "#F5F2EA"
INK = "#1D1D1B"
INK2 = "#5B5852"
MUTED = "#8C887E"
GRID = "#E2DDD1"
RED = "#C23B2E"     # accent / feedback / second series
BLUE = "#2F5FB3"    # first series
TINT = {RED: "#F6E2DE", BLUE: "#E1E8F5", INK: "#ECE8DE"}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.stretch": "condensed",
    "font.size": 11.5,
    "figure.facecolor": PAPER,
    "axes.facecolor": PAPER,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 2,
    "lines.markersize": 7,
    "legend.frameon": False,
    "savefig.dpi": 180,
    "savefig.facecolor": PAPER,
})


def title(fig, text, sub=None, y=0.965):
    fig.text(0.035, y, text, fontsize=18, fontweight="bold", color=INK,
             ha="left", va="top")
    if sub:
        fig.text(0.035, y - 0.065, sub, fontsize=12, color=INK2, ha="left",
                 va="top")


def note(fig, text):
    fig.text(0.035, 0.02, text, fontsize=9.5, color=MUTED, style="italic",
             ha="left", va="bottom")


def save(fig, name):
    fig.savefig(VIS / name)
    plt.close(fig)
    print("wrote", VIS / name)

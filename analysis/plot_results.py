"""
Charts from the measured lab data in ./data (Labs 5-8).

Usage: python analysis/plot_results.py   ->  PNGs in ./visuals
"""
import csv

import matplotlib.pyplot as plt
import numpy as np

from style import (BLUE, DATA, INK, INK2, MUTED, RED, note, save, title)


def load(name):
    rows = list(csv.DictReader(open(DATA / name)))
    return {k: np.array([float(r[k]) for r in rows]) for k in rows[0]}


def vc_from_va(va):
    return 3.3 / (56 + 3.3) * va          # voltage divider into the VCA


# ------------------------------------------------------------- Lab 5: VCA
def vca():
    d = load("lab5_vca.csv")
    vc = vc_from_va(d["Va_V"])
    g = 20 * np.log10(d["Vout_pp_V"] / d["Vin_pp_V"])
    slope, icpt = np.polyfit(vc, g, 1)
    xs = np.linspace(vc.min(), vc.max(), 50)
    fig, ax = plt.subplots(figsize=(12, 5.6))
    fig.subplots_adjust(top=0.8, bottom=0.14, left=0.08, right=0.8)
    title(fig, "VCA gain vs control voltage (Lab 5)",
          f"Measured sensitivity {1000 / slope:.1f} mV/dB vs THAT 2180C "
          "spec of -6 mV/dB")
    ax.plot(xs, -xs / 0.006, color=INK2, ls=":", lw=1.8)
    ax.plot(xs, slope * xs + icpt, color=RED, ls="--", lw=1.8)
    ax.plot(vc, g, "o", color=BLUE, mec="#F5F2EA", mew=1.5)
    ax.text(xs[-1] + 0.006, -xs[-1] / 0.006, "Datasheet\n(-6 mV/dB)",
            color=INK, fontsize=10.5, va="center")
    ax.text(xs[-1] + 0.006, slope * xs[-1] + icpt, "Best fit\n"
            f"({1000 / slope:.1f} mV/dB)", color=INK, fontsize=10.5,
            va="center")
    ax.set_xlabel("Control voltage Vc (V)")
    ax.set_ylabel("Gain (dB)")
    ax.legend(handles=[
        plt.Line2D([], [], color=BLUE, marker="o", ls="", label="Measured"),
        plt.Line2D([], [], color=RED, ls="--", label="Best fit"),
        plt.Line2D([], [], color=INK2, ls=":", label="Datasheet")],
        loc="upper right", ncol=3)
    note(fig, "Gain falls as Vc rises, as expected, but more gently than "
         "specified. Likely causes: a suspect OP275 and loose breadboard "
         "contacts.")
    save(fig, "vca-gain-vs-vc.png")


# ------------------------------------------------------------- Lab 6: PA
def pa():
    d = load("lab6_pa.csv")
    f = d["freq_Hz"]
    g1 = 20 * np.log10(d["Vout_pp_0p1V"] / d["Vin_pp_0p1V"])
    g2 = 20 * np.log10(d["Vout_pp_0p2V"] / d["Vin_pp_0p2V"])
    fig, ax = plt.subplots(figsize=(12, 5.4))
    fig.subplots_adjust(top=0.8, bottom=0.15, left=0.08, right=0.82)
    title(fig, "Power amp frequency response (Lab 6)",
          "LM380N stays within about 2 dB from 100 Hz to 10 kHz")
    ax.axhline(34, color=INK2, ls=":", lw=1.6)
    ax.plot(f, g1, "-o", color=BLUE, mec="#F5F2EA", mew=1.5)
    ax.plot(f, g2, "-o", color=RED, mec="#F5F2EA", mew=1.5)
    ax.text(105, 34.25, "Datasheet: 34 dB", va="bottom", fontsize=10.5,
            color=INK)
    ax.text(10800, g1[-1], "0.1 V input", va="center", fontsize=10.5,
            color=INK)
    ax.text(10800, g2[-1], "0.2 V input", va="center", fontsize=10.5,
            color=INK)
    ax.set_xscale("log")
    ax.set_xticks([100, 200, 500, 1000, 2000, 5000, 10000])
    ax.set_xticklabels(["100", "200", "500", "1k", "2k", "5k", "10k"])
    ax.set_ylim(26, 35)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Gain (dB)")
    ax.legend(handles=[
        plt.Line2D([], [], color=BLUE, marker="o", label="0.1 V input"),
        plt.Line2D([], [], color=RED, marker="o", label="0.2 V input"),
        plt.Line2D([], [], color=INK2, ls=":", label="Datasheet")],
        loc="lower left", ncol=3)
    note(fig, "Measured with a 22 ohm load in place of the speaker. "
         "20 kHz and 50 kHz points omitted (values cut off in the exported "
         "notebook).")
    save(fig, "pa-frequency-response.png")


# ------------------------------------------------------------- Lab 7: VU
def vu():
    d = load("lab7_vu.csv")
    fig, ax = plt.subplots(figsize=(12, 5.4))
    fig.subplots_adjust(top=0.8, bottom=0.15, left=0.08, right=0.95)
    title(fig, "VU meter output vs input level (Lab 7)",
          "The smoothed DC output rises steadily with signal amplitude, "
          "which is what the feedback loop needs")
    ax.axvspan(0, 1.3, color="#ECE8DE", zorder=0)
    ax.text(0.08, 2.05, "dead zone:\ndiodes not\nyet conducting", fontsize=10,
            color=INK2, va="top")
    ax.plot(d["Vin_pp_V"], d["Vout3_rms_V"], "-o", color=BLUE,
            mec="#F5F2EA", mew=1.5)
    ax.set_xlim(0, 8.3)
    ax.set_xlabel("Input amplitude Vin (V peak-to-peak)")
    ax.set_ylabel("VU output Vout3 (V RMS)")
    note(fig, "Rectifier stage gain measured at about 0.67-0.69 "
         "(theory: R2/R1 = 3.3k/4.7k = 0.70) for inputs of 3 Vpp and above.")
    save(fig, "vu-meter-response.png")


# ------------------------------------------------------------- Lab 8: system
def system():
    d = load("lab8_system.csv")
    vc = vc_from_va(d["Va_V"])
    g = 20 * np.log10(d["Vaudio_pp_V"] / d["Vsignal_pp_V"])
    slope, icpt = np.polyfit(vc, g, 1)
    r2 = np.corrcoef(vc, g)[0, 1] ** 2
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.6))
    fig.subplots_adjust(top=0.78, bottom=0.15, left=0.07, right=0.97,
                        wspace=0.25)
    title(fig, "Integrated system: gain is set by Vc (Lab 8)",
          f"{g.max() - g.min():.0f} dB of control range; "
          f"{1000 / slope:.2f} mV/dB, close to the -6 mV/dB spec "
          f"(R² = {r2:.4f})")
    xs = np.linspace(vc.min(), vc.max(), 50)
    a1.plot(xs, slope * xs + icpt, color=RED, ls="--", lw=1.6)
    a1.plot(vc, g, "o", color=BLUE, mec="#F5F2EA", mew=1.5)
    a1.set_title("System gain (VCA + PA)", loc="left", fontsize=12.5,
                 fontweight="bold")
    a1.set_xlabel("Control voltage Vc (V)")
    a1.set_ylabel("Gain Vaudio / Vsignal (dB)")
    a1.text(vc[0], g[0] + 4, "softest", ha="center", fontsize=10, color=INK2)
    a1.text(vc[-1] + 0.02, g[-1], "loudest", ha="left", fontsize=10,
            color=INK2, va="center")
    a2.plot(d["Vaudio_pp_V"], d["Vvolume_rms_V"], "o", color=BLUE,
            mec="#F5F2EA", mew=1.5)
    a2.set_title("VU reading tracks the speaker signal", loc="left",
                 fontsize=12.5, fontweight="bold")
    a2.set_xlabel("Vaudio (V peak-to-peak)")
    a2.set_ylabel("Vvolume (V RMS) -> controller")
    a2.set_xlim(0, 9.5)
    a2.text(0.3, 2.6, "loudest point: 8.96 Vpp at the speaker\n-> 2.66 V RMS at the VU output",
            ha="left", va="top", fontsize=10.5, color=INK2)
    a2.set_ylim(0, 2.9)
    note(fig, "Input amplitude was varied together with Va, so this "
         "characterises gain, not loudness.")
    save(fig, "system-gain-vs-vc.png")


if __name__ == "__main__":
    vca()
    pa()
    vu()
    system()

# Lab notes and measurements

Raw data is in [`../data`](../data). Every chart in the README comes from these numbers via [`../analysis/plot_results.py`](../analysis/plot_results.py).

## Hardware setup
| Item | Detail |
| :--- | :--- |
| Controller | STM32F4 board with the VScope interface board (MicroPython firmware), USB to laptop |
| Instruments | VScope: 2-channel waveform generator (W1, W2), 2-channel oscilloscope (CH1, CH2), ADC inputs (PC0, PC1), programmable ±DC supply |
| Supply | ±13.5 V for the VCA; +13.5 V for the PA and VU meter through an 820 µH inductor |
| VCA | THAT 2180C VCA + OP275 op-amp; Va → 56k/3.3k divider → Vc |
| Power amp | LM380N (34 dB fixed gain); 22 Ω test load, later the speaker; separate input (GND1) and output (GND2) grounds |
| VU meter | CA3140 inverting stage (4.7k in, 3.3k feedback), 2× 1N914 rectifier, 18k / 56k / 10 µF smoothing |

## Lab 5: VCA gain (1 kHz)
`Vc = 3.3/(56+3.3) × Va`, `Gain = 20·log10(Vout/Vin)`

| Amplitude (V) | Va (V) | Vc (V) | Vin (Vpp) | Vout (Vpp) | Gain (dB) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3.0 | 5.4 | 0.300 | 5.62 | 0.283 | −26.0 |
| 2.2 | 4.5 | 0.250 | 4.00 | 0.448 | −19.0 |
| 2.4 | 3.6 | 0.200 | 4.34 | 1.133 | −11.7 |
| 2.6 | 2.7 | 0.150 | 4.70 | 2.942 | −4.1 |
| 1.1 | 1.8 | 0.100 | 2.03 | 3.175 | +3.9 |
| 1.4 | 0.9 | 0.050 | 2.57 | 1.050 | −7.8 |
| 1.8 | 0.0 | 0.000 | 3.42 | 3.250 | −0.4 |
| 0.93 | −0.9 | −0.050 | 1.71 | 4.380 | +8.2 |
| 0.82 | −1.8 | −0.100 | 1.54 | 9.090 | +15.4 |
| 0.84 | −2.7 | −0.150 | 1.65 | 22.98 | +22.9 |

- Linear fit: −94.3 dB/V, so **−10.6 mV/dB**, against the datasheet's −6 mV/dB.
- The trend is right (more Vc, less gain), but the slope is too shallow and the 0.05–0.10 V points scatter. After a TA check, the likely causes were a suspect OP275 and poor breadboard contacts. We re-seated wires and checked grounds.
- Small inputs plus high gain gave noisy outputs. Large inputs plus high gain clipped against the ±13.5 V rails.

## Lab 6: Power amp frequency response
| f (Hz) | Vin (Vpp) @0.1 V | Vout (Vpp) | Gain (dB) | Vin (Vpp) @0.2 V | Vout (Vpp) | Gain (dB) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 0.248 | 7.45 | 29.6 | 0.429 | 11.59 | 28.6 |
| 200 | 0.251 | 8.87 | 31.0 | 0.460 | 11.49 | 28.0 |
| 500 | 0.253 | 8.89 | 30.9 | 0.440 | 10.41 | 27.5 |
| 1k | 0.204 | 7.86 | 31.7 | 0.388 | 10.20 | 28.4 |
| 2k | 0.214 | 8.19 | 31.6 | 0.401 | 10.14 | 28.1 |
| 5k | 0.229 | 8.19 | 31.1 | 0.405 | 10.14 | 28.0 |
| 10k | 0.245 | 8.20 | 30.5 | 0.426 | 10.47 | 27.8 |

- Flat to within about 2 dB over 100 Hz–10 kHz, but 2–6 dB under the 34 dB spec. The 0.2 V set sits about 3 dB lower than the 0.1 V set.
- The 20 kHz and 50 kHz rows were cut off in the exported notebook. The original plot shows the 0.1 V gain falling to about 28 dB by 50 kHz.
- Loudest case: 11.6 Vpp across 22 Ω ≈ **0.53 A peak-to-peak through GND2**. This is why the output-stage ground is kept off the input-stage ground.

## Lab 7: VU meter (1 kHz)
| Amplitude (V) | Vin (Vpp) | Vout1 (Vpp) | Vout2 (Vpp) | Vout3 (V RMS) | Gain 2·Vout2/Vin |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4.2 | 7.84 | 3.48 | 2.64 | 2.16 | 0.67 |
| 3.4 | 6.33 | 2.95 | 2.12 | 1.66 | 0.67 |
| 3.2 | 6.02 | 2.82 | 2.02 | 1.54 | 0.67 |
| 2.1 | 3.95 | 2.08 | 1.36 | 0.861 | 0.69 |
| 1.8 | 3.38 | 1.84 | 1.14 | 0.682 | 0.67 |
| 1.3 | 2.38 | 1.53 | 0.884 | 0.394 | 0.74 |
| 0.6 | 1.19 | 1.02 | 0.469 | 0.065 | 0.79 |
| 0.2 | 0.379 | 0.696 | 0.252 | 0.031 | 1.33 |

- Theory: R2/R1 = 3.3k/4.7k = 0.70. Measured 0.67–0.69 for inputs of 3 Vpp and up.
- Below about 1.2 Vpp the diodes barely conduct and Vout3 is close to zero (dead zone). A DC offset at the input would inflate the reading.

## Lab 8: Integrated system, manual control (302 Hz)
| Amplitude (V) | Va (V) | Vc (V) | Vsignal (Vpp) | Vaudio (Vpp) | Vvolume (V RMS) | Gain (dB) |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 4.2 | 5.4 | 0.300 | 7.87 | 1.27 | 0.071 | −15.8 |
| 3.2 | 4.5 | 0.250 | 6.02 | 2.29 | 0.376 | −8.4 |
| 2.4 | 3.6 | 0.200 | 4.51 | 4.31 | 0.997 | −0.4 |
| 1.2 | 2.7 | 0.150 | 2.23 | 5.41 | 1.36 | +7.7 |
| 0.8 | 1.8 | 0.100 | 1.52 | 8.91 | 2.56 | +15.4 |
| 0.3 | 0.9 | 0.050 | 0.600 | 8.85 | 2.52 | +23.4 |
| 0.09 | 0.0 | 0.000 | 0.203 | 7.17 | 1.92 | +31.0 |
| 0.04 | −0.9 | −0.050 | 0.116 | 8.96 | 2.66 | +37.8 |

- Gain vs Vc is almost perfectly linear: **−6.46 mV/dB (R² = 0.9996)**, close to the −6 mV/dB spec. The full system behaved better than the Lab 5 VCA bench test.
- Maximum Vaudio 8.96 Vpp gives Vvolume 2.66 V RMS, inside the 3.3 V that PC0 can read.
- Speaker swapped in for the 22 Ω load, with music from the laptop's audio out.
- First power-up screeched and distorted. The cause was the ground on the wrong side of the breadboard. Moving it fixed the audio.

## Lab 9: Automatic control
- Step-up-down controller, Δ = 0.05 V per 10 ms, Va clipped to −2.7…9.0 V. Code: [`../code/auto_volume_control.py`](../code/auto_volume_control.py).
- Small Δ: smooth but slow to reach the set level. Large Δ: fast, but it overshoots and keeps oscillating around the set point. There is no tolerance band, so the loop never stops adjusting.
- `RepeatTimer` re-arms only after `control()` returns, so the real period is 10 ms plus execution time, USB I/O and OS scheduling. It is only approximately periodic.

## Demo
- Played music through the speaker for the examiner: clear and stable audio.
- First attempt: our explanation of the 820 µH inductor didn't convince the examiner. We regrouped and explained it fully. It isolates the PA's current surges from the VCA supply and blocks high-frequency noise from travelling round the loop. We passed on the second attempt.

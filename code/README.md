# Code

| File | What it is |
| :--- | :--- |
| `auto_volume_control.py` | The Lab 9 closed-loop controller: reads the VU meter, steps Va, writes it to the VCA. |
| `repeat_timer.py` | The timer that calls `control()` every ~10 ms (course-provided). |

## How it runs
1. The STM32F4 + VScope board connects to the laptop over USB and runs the course's MicroPython firmware.
2. In Jupyter, the course-provided `VScopeBoard` driver opens the serial link. This driver is **not** included here.
3. Run `auto_volume_control.py` in a notebook cell. Use **Set** to choose the target loudness and **On** to start. **Vol** shows the measured level.

## Wiring the loop needs
| VScope pin | Circuit node | Role |
| :--- | :--- | :--- |
| W2 (DC offset) | Va | Control voltage, via the 56k/3.3k divider to Vc |
| PC0 (ADC) | Vvolume | VU meter output, 0 to 3.3 V |
| VDCP / VDCN / GND | Breadboard rails | ±13.5 V supply |
| Laptop audio out | Vsignal | Music or a test tone |

## Requirements
`numpy`, `ipywidgets`, `pyserial`, Jupyter. For the charts in `analysis/`: `numpy`, `matplotlib`.

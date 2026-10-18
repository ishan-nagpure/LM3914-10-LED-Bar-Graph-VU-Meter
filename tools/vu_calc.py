#!/usr/bin/env python3
"""LM3914 VU meter calculator.

Works out the reference voltage, LED current, per-LED signal requirements and
low-pass filter cutoff for the circuit in this repository. Standard library only.

Examples
--------
  python tools/vu_calc.py                          # defaults = the circuit in the README
  python tools/vu_calc.py --diode 0.3              # Schottky / germanium diode
  python tools/vu_calc.py --rhi-series 4700        # lower full scale (4.7k from Pin 7 to Pin 6)
  python tools/vu_calc.py --filter-r 2000          # add a 2k + 0.1uF low-pass filter

These are datasheet-style estimates, not measurements. Real chips and diodes vary.
"""
import argparse
import math

V_INTERNAL = 1.25      # V held between REF OUT (Pin 7) and REF ADJ (Pin 8)
I_ADJ = 75e-6          # A, typical REF ADJ pin current
PHONE_PEAK_V = 1.4     # V, rough peak level of a phone at full volume


def parallel(a, b):
    return a * b / (a + b)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--r1", type=float, default=1430.0, help="R1, Pin 7 to Pin 8, ohms (default 1430)")
    p.add_argument("--r2", type=float, default=0.0, help="R2, Pin 8 to GND, ohms (0 = Pin 8 tied to GND)")
    p.add_argument("--rhi-series", type=float, default=0.0,
                   help="resistor from Pin 7 to Pin 6 (RHI), ohms; 0 = Pin 6 tied to Pin 7")
    p.add_argument("--ladder", type=float, default=10000.0,
                   help="internal divider resistance RLO-RHI, ohms (about 10k, varies 8k-17k)")
    p.add_argument("--diode", type=float, default=0.6, help="diode forward drop in volts (default 0.6)")
    p.add_argument("--pot", type=float, default=10000.0, help="potentiometer value, ohms")
    p.add_argument("--filter-r", type=float, default=0.0, help="low-pass series resistor, ohms (0 = no filter)")
    p.add_argument("--filter-c", type=float, default=0.1e-6, help="low-pass capacitor, farads")
    p.add_argument("--bleed", type=float, default=100e3, help="bleed resistor on Pin 5, ohms")
    p.add_argument("--smooth-c", type=float, default=1e-6, help="smoothing capacitor on Pin 5, farads")
    a = p.parse_args()

    vref = V_INTERNAL * (1 + a.r2 / a.r1) + I_ADJ * a.r2
    if a.rhi_series > 0:
        full_scale = vref * a.ladder / (a.ladder + a.rhi_series)
    else:
        full_scale = vref
    step = full_scale / 10
    i_led_ma = 12.5 / a.r1 * 1000

    if a.filter_r > 0:
        gain = a.pot / (a.pot + a.filter_r)
        r_eff = parallel(a.filter_r, a.pot)
        fc = 1 / (2 * math.pi * r_eff * a.filter_c)
    else:
        gain, fc = 1.0, None

    tau = a.bleed * a.smooth_c

    print("LM3914 VU meter - calculated values")
    print("-" * 52)
    print(f"Reference voltage (Pin 7)    : {vref:6.2f} V")
    print(f"Full scale at RHI (Pin 6)    : {full_scale:6.2f} V")
    print(f"Voltage per LED step         : {step * 1000:6.0f} mV")
    print(f"LED current (12.5 / R1)      : {i_led_ma:6.1f} mA each")
    print(f"All 10 LEDs on (from battery): {i_led_ma * 10:6.0f} mA")
    print(f"Peak-detector decay (R*C)    : {tau * 1000:6.0f} ms")
    if fc:
        print(f"Low-pass cutoff              : {fc:6.0f} Hz  (signal passed at bass: {gain * 100:.0f}%)")
    else:
        print("Low-pass filter              : none")
    print()
    print("Peak voltage needed from the audio source (pot at maximum):")
    print(f"{'LED':>4} {'at Pin 5':>10} {'at source':>11}")
    for n in range(1, 11):
        at_pin5 = n * step
        at_source = (at_pin5 + a.diode) / gain
        flag = "" if at_source <= PHONE_PEAK_V else "  (above ~1.4 V phone peak)"
        print(f"{n:>4} {at_pin5:>9.2f}V {at_source:>10.2f}V{flag}")


if __name__ == "__main__":
    main()

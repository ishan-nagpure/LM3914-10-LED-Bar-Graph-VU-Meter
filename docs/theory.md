# Theory of Operation

## From analog to LEDs

This project converts a smooth **analog** audio voltage into strict, stepped **digital** light levels. It does this with **comparators**, circuits that turn on when an input voltage rises above a set threshold. The LM3914 contains ten of them, each with a slightly higher threshold than the last, and each drives one LED.

Inside the chip, ten equal 1 kOhm resistors form a ladder between **RLO** (the bottom, 0 V here) and **RHI** (the top, the full-scale voltage). Each rung feeds one comparator, so the thresholds are evenly spaced at roughly 10%, 20%, 30% ... 100% of full scale.

The LM3914 is **linear**: every step is the same number of volts. Human hearing is logarithmic, so for a more natural audio display the **LM3915** (3 dB per step) or **LM3916** (VU scale) is a better fit. They share the same pinout, so this circuit works with either.

## Signal path

```
audio jack -> volume pot -> diode D1 -> Pin 5 (SIG)
                                         |-- C2 1 uF to GND   (holds the peak)
                                         '-- R2 100k to GND   (lets it fall)
```

- **Volume pot (RV1):** a variable voltage divider. It can only turn the signal down, never up.
- **Diode (D1):** audio swings positive and negative, and the chip wants a positive voltage, so the diode passes only the positive half (half-wave rectifier). It also costs about 0.6 V for a 1N4148.
- **C2 and R2:** together they form a simple **peak detector**. C2 charges quickly to each peak and R2 discharges it slowly. The time constant is R2 x C2 = 100 kOhm x 1 uF = 0.1 s, so the bar jumps up on a beat and falls smoothly. Without R2, Pin 5 has no way to come back down. Without C2, the LEDs follow the raw wave and flicker.

## LM3914 pin-by-pin

The LM3914 comes in an 18-pin DIP.

### Power pins

| Pin | Name | Function |
|----:|------|----------|
| 3 | V+ | Positive supply, about 3 V to 25 V. It powers the chip and is the usual supply for the LEDs. At 9 V with all 10 LEDs on, the chip drops roughly 7 V while sinking about 87 mA, so it dissipates around 0.6 W and may feel warm. |
| 2 | V- | Negative supply and the chip's 0 V reference. Goes to GND on a single battery. |

### Signal and divider pins

| Pin | Name | Function |
|----:|------|----------|
| 5 | SIG | Signal input, wired to all 10 comparators at once. It is **very high impedance** (tens of nanoamps of bias current), which is good because it does not load the source, but it will float to a random voltage if nothing pulls it down. That is why R2 is part of the circuit. The input should stay between V- and about 1.5 V below V+. The pin tolerates up to about 35 V without damage. |
| 4 | RLO | Bottom of the internal divider. Sets the 0% point. Tied to GND here. |
| 6 | RHI | Top of the internal divider. Sets the 100% (full-scale) point. LED 10 turns on when SIG reaches about this voltage. Tied to Pin 7 here. |

### Reference pins

| Pin | Name | Function |
|----:|------|----------|
| 7 | REF OUT | An internal reference holds **1.25 V between Pin 7 and Pin 8**. Pin 7 feeds the divider and also sets the LED current: each LED output sinks about **10 times the current drawn from this pin**, so `I_LED = 12.5 V / R1`. |
| 8 | REF ADJ | Lets you raise the reference above 1.25 V by adding a resistor R2' from Pin 8 to ground: `V_ref = 1.25 V x (1 + R2' / R1)` plus a small extra from about 75 uA of adjust current through R2'. Tied straight to GND here, so V_ref = 1.25 V. |

### Mode pin

| Pin | Name | Function |
|----:|------|----------|
| 9 | MODE | Left open = **dot mode** (only the LED for the current level lights). Tied to V+ = **bar mode** (all LEDs up to the current level light). Bar mode with every LED lit is also the worst case for current and heat. |

### LED output pins

| Pin | LED |
|----:|-----|
| 1 | LED 1 (lowest level) |
| 18 | LED 2 |
| 17 | LED 3 |
| 16 | LED 4 |
| 15 | LED 5 |
| 14 | LED 6 |
| 13 | LED 7 |
| 12 | LED 8 |
| 11 | LED 9 |
| 10 | LED 10 (highest level) |

Each output is an **open-collector, current-regulated sink**. When a comparator trips, the chip pulls that LED's cathode toward ground and regulates the current to the value set by R1 (programmable from roughly 2 to 30 mA). That is why the LED anodes go straight to +9 V with no resistors.

The numbering is not sequential: LED 1 is Pin 1, but LED 2 is Pin 18, counting down to LED 10 on Pin 10.

## Setting the reference and LED current

With Pin 8 tied to GND and R1 = 1.43 kOhm:

- Full scale = 1.25 V, so each LED step is about 125 mV.
- LED current is about 12.5 / 1.43 kOhm = 8.7 mA.
- Total with all LEDs on is about 87 mA.

Adding a resistor R2' from Pin 8 to GND raises full scale:

| R2' (Pin 8 to GND) | Full scale | Per LED step |
|---|---|---|
| 0 Ohm (wire) | 1.25 V | 0.125 V |
| 1 kOhm | about 2.1 V | about 0.21 V |
| 3 kOhm | about 3.9 V | about 0.39 V |

A higher full scale needs a louder signal to light the top LEDs, so for phone audio the 1.25 V setting is the best starting point.

## References

- LM3914 datasheet: <https://www.ti.com/product/LM3914>

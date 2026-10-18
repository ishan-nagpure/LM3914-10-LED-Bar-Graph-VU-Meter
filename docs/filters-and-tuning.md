# Filters and Sensitivity Tuning

Optional improvements for the basic circuit. Build and test the basic meter first, then add these one at a time so you can see what each change does. The numbers here are calculated estimates; you can recompute them with [`tools/vu_calc.py`](../tools/vu_calc.py).

## 1. Sensitivity budget

LED *n* lights when the voltage on Pin 5 reaches about *n*/10 of full scale. The diode costs a fixed drop on the way, and any filter or pot loses some signal. So the peak voltage needed from the audio source (pot at maximum, no filter) is roughly:

```
V_source = (n x V_step + V_diode) / gain
```

With full scale = 1.25 V (V_step = 125 mV) and a 1N4148 (0.6 V drop):

| LED | Needed at Pin 5 | Needed at source |
|----:|----------------:|-----------------:|
| 1 | 0.12 V | 0.72 V |
| 5 | 0.62 V | 1.23 V |
| 10 | 1.25 V | 1.85 V |

A phone at full volume produces roughly **1 to 1.4 V peak**, so the top LEDs are out of reach with the basic circuit. The options below reduce what is needed.

## 2. Use a lower-drop diode

Replace the 1N4148 with a **Schottky (1N5819)** or **germanium (1N34A)** diode. The drop falls from about 0.6 V to about 0.3 V. This is the biggest easy improvement. LED 10 then needs about 1.55 V at the source instead of 1.85 V.

## 3. Lower the full-scale voltage

Remove the wire between Pin 6 and Pin 7 and fit a **4.7 kOhm resistor from Pin 7 to Pin 6**. The chip's internal 10 kOhm ladder (to RLO at GND) then divides the 1.25 V down to roughly:

```
1.25 V x 10k / (10k + 4.7k) = about 0.85 V
```

Every LED now needs less signal. The internal ladder resistance varies between chips (about 8k to 17k), so treat 0.85 V as approximate. LED brightness changes only slightly.

| Setup | LED 10 needs at the source |
|-------|---------------------------:|
| Basic (1N4148, 1.25 V full scale) | about 1.85 V |
| Schottky diode only | about 1.55 V |
| 1N4148 + 4.7 kOhm on Pin 6 | about 1.45 V |
| Schottky + 4.7 kOhm on Pin 6 | about 1.15 V |

Most phones can reach 1.15 V at full volume.

## 4. Op-amp gain stage (the proper fix)

A small op-amp amplifier before the diode multiplies the signal and removes the sensitivity problem entirely, and it also makes the volume control work in both directions. This is the route to take if you want a full-range display together with a filter.

## 5. Low-pass filter (bass-focused display)

A low-pass filter lets bass and kick drums through and weakens treble, so the bar follows the beat instead of jittering on hi-hats.

Put a resistor and a 0.1 uF capacitor between the jack tip and the pot:

```
Jack TIP --[ Rf ]--+-------- top of pot
                   |
                 0.1 uF
                   |
                  GND
```

The pot loads the filter, so the cutoff is `fc = 1 / (2 x pi x R_eff x C)` where `R_eff` is Rf in parallel with 10 kOhm. The cutoff does not change when you turn the volume knob.

| Rf | Cutoff (0.1 uF) | Signal passed at bass | Character |
|----|----------------:|----------------------:|-----------|
| 1 kOhm | about 1750 Hz | 91% | Mild, lets in many mids |
| 2 kOhm | about 950 Hz | 83% | Tames treble, vocals still react |
| 2.2 kOhm | about 880 Hz | 82% | Similar to 2 kOhm |
| **4.7 kOhm** | **about 500 Hz** | **68%** | **Good bass-focused balance** |
| 10 kOhm | about 320 Hz | 50% | Strongly bass-focused, weak signal |
| 22 kOhm | about 230 Hz | 31% | Too much signal lost |

Response with 4.7 kOhm and 0.1 uF:

| Frequency | Level vs bass |
|----------:|--------------:|
| 100 Hz | no change |
| 500 Hz | -3 dB (70%) |
| 1 kHz | -7 dB (45%) |
| 2 kHz | -12 dB (24%) |
| 5 kHz | -20 dB (10%) |
| 10 kHz | -26 dB (5%) |

This is a gentle first-order filter (6 dB per octave), so it softens the highs rather than removing them.

**Cost:** the filter reduces the signal, so fewer LEDs light. Combine it with the Schottky diode and the lower full scale (sections 2 and 3). For example, a 2 kOhm filter with both of those brings LED 10's requirement to roughly 1.4 V at the source.

## 6. High-pass filter (snares and vocals)

Put a 0.1 uF capacitor in series between the jack tip and the pot. With the 10 kOhm pot the cutoff is about 160 Hz. Replacing it with 10 nF raises the cutoff to about 1.6 kHz. The meter then reacts less to boomy bass and more to snares and vocals.

## 7. Changing the fall speed

The 100 kOhm and 1 uF on Pin 5 set the fall time constant to about 0.1 s. This is not an audio filter; it only smooths the bar.

| R2 (with 1 uF) | Fall time (about) | Notes |
|---|---|---|
| 22 kOhm to 47 kOhm | 0.02 to 0.05 s | Twitchy bar, loads the signal more |
| 100 kOhm | 0.1 s | Good balance |
| 220 kOhm to 470 kOhm | 0.2 to 0.5 s | Slow, smooth fall |

Avoid going above about 470 kOhm (the chip's input bias current can then light the first LED with no music) or below about 10 kOhm (it drains too much signal).

## 8. Testing a filter

Play a 100 Hz tone and then a 5 kHz tone at the same phone volume. Without the filter the meter reads about the same for both. With a 4.7 kOhm filter, the 5 kHz tone should read roughly a tenth as large. Use tones between 60 and 200 Hz for bass tests: phones barely reproduce anything below about 20-30 Hz.

# Build Guide

Step-by-step instructions for building the LM3914 VU meter on a solderless breadboard. See the [schematic](schematic.svg) alongside this guide.

*Tip: your breadboard has a positive (+) rail (usually red) and a negative (-) rail (usually blue or black). This guide calls them the **+9V rail** and the **GND rail**.*

## Before you start

You need the parts in [BOM.csv](../BOM.csv). Do **not** connect the battery until the wiring is finished and double-checked.

## Phase 1: Power and ground

1. Connect the **red** wire of the 9 V battery clip to the +9V rail.
2. Connect the **black** wire to the GND rail.
3. Plug the LM3914 into the middle of the breadboard across the centre trench. Pin 1 is marked by a dot or notch. Pins count up one side (1-9) and continue back down the other side (10-18), so Pin 10 is directly opposite Pin 9 and Pin 18 directly opposite Pin 1.
4. Connect **Pin 3 (V+)** to the +9V rail.
5. Connect **Pin 9 (MODE)** to the +9V rail. This gives a solid bar graph. Leaving it open gives dot mode, where only one LED lights at a time.
6. Connect **Pin 2 (V-)** to the GND rail.
7. Connect **Pin 4 (RLO)** to the GND rail.
8. Connect the **0.1 uF capacitor (C1)** between the +9V rail and the GND rail, as close to the chip as you can. It has no polarity.

## Phase 2: Reference resistor

1. Bridge **Pin 6** to **Pin 7** with a short wire.
2. Build **R1 (1.43 kOhm)** by chaining a 1 kOhm, a 330 Ohm, and a 100 Ohm resistor in series. Connect one end to **Pin 7** and the other end to **Pin 8**.
3. Connect **Pin 8** to the GND rail with a jumper wire.

The chip keeps 1.25 V across R1. That sets the full-scale voltage to 1.25 V (about 125 mV per LED step) and the LED current to roughly 12.5 / 1.43 kOhm = 8.7 mA.

## Phase 3: Audio input

1. Plug the **10 kOhm potentiometer (RV1)** into the board.
2. Connect the **SLEEVE** pin of the audio jack to the GND rail.
3. Connect the **TIP** pin of the jack to one outer leg of the pot.
4. Connect the other outer leg of the pot to the GND rail.
5. Connect the **anode** of the **1N4148 (D1)**, the end *without* the black stripe, to the **middle leg (wiper)** of the pot.
6. Connect the **cathode**, the end *with* the black stripe, to **Pin 5 (SIG)**.
7. Connect the **100 kOhm resistor (R2)** from **Pin 5** to the GND rail.
8. Connect the **1 uF capacitor (C2)** from **Pin 5** to the GND rail. If it is an electrolytic, the **+** leg goes to Pin 5.

The jack's **RING** pin (right channel) is left unconnected.

## Phase 4: LEDs

LEDs have polarity: the **long leg is the anode (+)** and the **short leg is the cathode (-)**.

1. Plug all 10 LEDs into the breadboard.
2. Connect the **anodes** of all 10 LEDs to the +9V rail. No series resistors are needed.
3. Connect the **cathodes** to the LM3914 in this exact order, from quietest to loudest:

| LED | Pin |
|----:|----:|
| 1 | 1 |
| 2 | 18 |
| 3 | 17 |
| 4 | 16 |
| 5 | 15 |
| 6 | 14 |
| 7 | 13 |
| 8 | 12 |
| 9 | 11 |
| 10 | 10 |

## Phase 5: Test

1. Check Pin 1 orientation, the +9V and GND rails, and LED polarity.
2. Connect the 9 V battery.
3. Plug in an aux cable and play a bass-heavy song at 75-100% phone volume.
4. Slowly turn the pot until the LEDs start to move.

### Testing without audio

You can check the chip and LED wiring using the 1.25 V reference as a test voltage:

1. With power on, touch a jumper from **Pin 5 to GND**. All LEDs should be off.
2. Move the jumper from GND to **Pin 7** (1.25 V). All LEDs should light.
3. To see the bar climb, temporarily feed Pin 5 from the wiper of a 10 kOhm pot whose outer legs go to Pin 7 and GND. Turning the knob should light the LEDs one by one, starting with LED 1 on Pin 1.

If that works, the power, reference, mode, and LED wiring are correct.

If something does not work, see [troubleshooting.md](troubleshooting.md). To improve sensitivity or add a filter, see [filters-and-tuning.md](filters-and-tuning.md).

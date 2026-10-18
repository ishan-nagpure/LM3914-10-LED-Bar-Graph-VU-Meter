# Troubleshooting

Work through the symptom that matches. Always disconnect the battery before rewiring.

## Nothing lights up

- Check the battery connections and that the LEDs are not backward (long leg to +9V).
- Pin 9 must be on +9V, and Pin 8 must be on GND with R1 between Pins 7 and 8.
- Confirm the diode stripe faces Pin 5.
- Turn the pot the other way and raise the phone volume.
- Run the no-audio test in the [build guide](build-guide.md#testing-without-audio). If that works, the problem is in the audio input.

## Only one or two LEDs light, even when loud

The signal is too weak for the diode drop. See [filters-and-tuning.md](filters-and-tuning.md):

1. Make sure Pin 8 goes straight to GND.
2. Swap the 1N4148 for a Schottky (1N5819) or germanium (1N34A) diode.
3. Lower full scale with a 4.7 kOhm resistor from Pin 7 to Pin 6.
4. Remove or reduce any low-pass filter resistor.
5. For a full-range display, add an op-amp gain stage.

## The top LED (LED 10) never lights

This is expected with the basic circuit and a phone. LED 10 needs about 1.85 V peak at the source, and a phone gives roughly 1 to 1.4 V. Use the same fixes as above.

## All LEDs are lit

Pin 5 is above full scale, or the reference pins are wrong.

1. Touch a jumper from **Pin 5 to GND**. If all LEDs go off, the problem is at Pin 5: add the 100 kOhm resistor (R2) if it is missing, or turn the pot down if audio is playing.
2. If the LEDs stay on with Pin 5 grounded, check the reference and ground pins:
   - Pin 4 (RLO) must be on GND. If it floats, the thresholds collapse and everything lights.
   - Pin 2 (V-) must be on GND.
   - Pin 6 must be connected to Pin 7 (or to the 4.7 kOhm resistor if you lowered full scale).
   - Pin 8 must be on GND, with R1 between Pins 7 and 8.
3. Confirm Pin 9 is on +9V, and that no test jumper is still on Pin 7.

## LEDs stay on when the music is paused

Pin 5 is floating. Check that the 100 kOhm resistor runs from Pin 5 to GND and that the diode faces the right way.

## LEDs flicker instead of holding a smooth bar

The 1 uF capacitor on Pin 5 is missing or loose.

## LEDs are very dim or flash randomly

The reference connections are likely loose. Make sure R1 is firmly seated between Pins 7 and 8, Pin 6 is securely connected to Pin 7, and Pin 8 is firmly on GND.

## The bar drops or bounces on very low-frequency tones (0-30 Hz)

This is normal. Phones and their amplifiers barely reproduce anything below about 20-30 Hz, so the signal is small. Also, the peak detector lets go with a time constant of about 0.1 s, so at 5-10 Hz the bar falls between peaks. Test with 60-200 Hz tones or bass-heavy music instead.

## The chip gets hot

All 10 LEDs on draws about 87 mA, so warm is normal. If it is too hot to touch, disconnect the battery and recheck the wiring.

## LEDs buzz or oscillate when many are lit

The supply is sagging. Move the 0.1 uF capacitor closer to Pins 2 and 3 and add a 10 uF electrolytic across the supply rails (+ leg to +9V).

## LEDs light out of order

The LED pin order is not sequential. LED 1 is Pin 1, LED 2 is Pin **18**, and the numbers count down to LED 10 on Pin **10**.

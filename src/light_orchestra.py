# main.py for Raspberry Pi Pico W
# Title: Pico Light Orchestra Instrument Code

import machine
import time
import json
import asyncio

# --- Pin Configuration ---
# The photosensor is connected to an Analog-to-Digital Converter (ADC) pin.
# We will read the voltage, which changes based on light.
photo_sensor_pin = machine.ADC(26)

# The buzzer is connected to a GPIO pin that supports Pulse Width Modulation (PWM).
# PWM allows us to create a square wave at a specific frequency to make a sound.
buzzer_pin = machine.PWM(machine.Pin(18))


# --- Core Functions ---


def play_tone(frequency: int, duration_ms: int) -> None:
    """Plays a tone on the buzzer for a given duration."""
    if frequency > 0:
        buzzer_pin.freq(int(frequency))
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        time.sleep_ms(duration_ms)  # type: ignore[attr-defined]
        stop_tone()
    else:
        time.sleep_ms(duration_ms)  # type: ignore[attr-defined]


def stop_tone():
    """Stops any sound from playing."""
    buzzer_pin.duty_u16(0)  # 0% duty cycle means silence


def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


async def main():
    """Main execution loop."""

    # This loop runs the "default" behavior: playing sound based on light
    while True:
          # Read the sensor. Values range from ~500 (dark) to ~65535 (bright)
          light_value = photo_sensor_pin.read_u16()

          # Map the light value to a frequency range (e.g., C4 to C6)
          # Adjust the input range based on your room's lighting
          min_light = 1000
          max_light = 65000
          min_freq = 261  # C4
          max_freq = 1046  # C6

          # Clamp the light value to the expected range
          clamped_light = max(min_light, min(light_value, max_light))

          if clamped_light > min_light:
              frequency = map_value(
                  clamped_light, min_light, max_light, min_freq, max_freq
              )
              buzzer_pin.freq(frequency)
              buzzer_pin.duty_u16(32768)  # 50% duty cycle
          else:
              stop_tone()  # If it's very dark, be quiet

        await asyncio.sleep_ms(50)  # type: ignore[attr-defined]


# Run the main event loop
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped.")
        stop_tone()

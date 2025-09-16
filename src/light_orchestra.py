# main.py for Raspberry Pi Pico W
# Title: Pico Light Orchestra Instrument Code

import machine
import time
import json
import asyncio

# --- Pin Configuration ---
photo_sensor_pin = machine.ADC(26)
buzzer_pin = machine.PWM(machine.Pin(18))

# --- Global Variables for Replay ---
# This list will store tuples of (timestamp_ms, light_value)
recorded_data = []
recording_active = False
replay_active = False
replay_index = 0

start_time = time.ticks_ms()
NOTES_C3_C7 = [
    131,147,165,175,196,220,247,         # C3..B3
    262,294,330,349,392,440,494,         # C4..B4
    523,587,659,698,784,880,988,         # C5..B5
    1047,1175,1319,1397,1568,1760,1976,  # C6..B6
    2093
]
bpm = 120
BEAT_MS = int(60000 / bpm)
frequency = 262
dur_ms   = int(BEAT_MS * 4)
chord = [7,2,4,2]


# --- Core Functions ---
def Play_Chord(base_frequency : int, time : int, light_00 : int, light_0 : int):
    global chord
    
    
    if (light_0-light_00) >= 2*light_00:
        chord[0] = 4
        if (light_0-light_00) < 3*light_00:
            chord[1] = 2
            chord[2] = 0
            chord[3] = 7
        elif (light_0-light_00) < 4*light_00:
            chord[1] = 7
            chord[2] = 0
            chord[3] = 4
        else:
            chord[1] = 0
            chord[2] = 7
            chord[3] = 4
    else:
        chord[0] = 0
        if (light_0-light_00) < 0:
            if base_frequency >= 262:
                chord[1] = -3
                chord[2] = -5
                chord[3] = -7
            else:
                chord[1] = 4
                chord[2] = 2
                chord[3] = 0
        elif (light_0-light_00) < 0.25*light_00:
            chord[1] = 4
            chord[2] = 7
            chord[3] = 4
        else:
            chord[1] = 2
            chord[2] = 4
            chord[3] = 7
        
    
    
    note_0 = NOTES_C3_C7[nearest_white_note(frequency)+chord[0]]
    note_1 = NOTES_C3_C7[nearest_white_note(frequency)+chord[1]]
    note_2 = NOTES_C3_C7[nearest_white_note(frequency)+chord[2]]
    note_3 = NOTES_C3_C7[nearest_white_note(frequency)+chord[3]]
    
    #print(chord[0],chord[1],chord[2],chord[3])
    #print(light_0,light_00)
    #print(base_frequency)
    if time < 500:
        buzzer_pin.freq(note_0)

    elif time < 1000:
        buzzer_pin.freq(note_1)

    elif time < 1500:
        buzzer_pin.freq(note_2)

    else:
        buzzer_pin.freq(note_3)
    buzzer_pin.duty_u16(32768)


def play_tone(frequency: int, duration_ms: int) -> None:
    """Plays a tone on the buzzer for a given duration."""
    if frequency > 0:
        buzzer_pin.freq(int(frequency))
        buzzer_pin.duty_u16(32768)  # 50% duty cycle
        time.sleep_ms(duration_ms)
        stop_tone()
    else:
        time.sleep_ms(duration_ms)


def stop_tone():
    """Stops any sound from playing."""
    buzzer_pin.duty_u16(0)


def map_value(x, in_min, in_max, out_min, out_max):
    """Maps a value from one range to another."""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def save_recording(filename="recording.json"):
    """Saves the recorded_data to a JSON file."""
    global recorded_data
    try:
        with open(filename, "w") as f:
            json.dump(recorded_data, f)
        print(f"Recording saved to {filename}")
    except OSError as e:
        print(f"Error saving recording: {e}")

def load_recording(filename="recording.json"):
    """Loads recorded_data from a JSON file."""
    global recorded_data, replay_index
    try:
        with open(filename, "r") as f:
            recorded_data = json.load(f)
        print(f"Recording loaded from {filename}")
        replay_index = 0 # Reset replay index when loading
        return True
    except OSError as e:
        print(f"Error loading recording: {e}. File might not exist or be corrupt.")
        recorded_data = [] # Clear data if load fails
        return False
    except ValueError as e:
        print(f"Error parsing recording data: {e}. File might be corrupt.")
        recorded_data = []
        return False

# --- Control Functions for Recording/Replay ---
def start_recording():
    global recording_active, recorded_data, replay_active
    if not replay_active:
        recording_active = True
        recorded_data = [] # Clear previous recording
        print("Recording started...")
    else:
        print("Cannot start recording while replay is active.")

def stop_recording():
    global recording_active
    if recording_active:
        recording_active = False
        print("Recording stopped.")
        save_recording()
    else:
        print("No recording active.")

def start_replay():
    global replay_active, replay_index, recording_active
    if not recording_active and len(recorded_data) > 0:
        replay_active = True
        replay_index = 0
        print("Replay started...")
    elif recording_active:
        print("Cannot start replay while recording is active.")
    else:
        print("No data to replay. Record something first or load a recording.")

def stop_replay():
    global replay_active
    if replay_active:
        replay_active = False
        stop_tone()
        print("Replay stopped.")
    else:
        print("No replay active.")

def nearest_white_note(freq_hz: int):
    """Return (name, freq) for nearest white-key note between C3 and B6."""
    idx = min(range(len(NOTES_C3_C7)), key=lambda k: abs(NOTES_C3_C7[k] - freq_hz))
    return idx

async def main():
    """Main execution loop."""

    # These ranges define how light maps to frequency
    min_light = 1000
    max_light = 65000
    min_freq = 130  # C3
    max_freq = 1046 # C6

    last_timestamp = time.ticks_ms()
    frequency_refresh = 1
    last_rel_time = 0
    light_0 = 0
    light_00 = 0
    
    
    
    while True:
        current_timestamp = time.ticks_ms()
        delta_time = time.ticks_diff(current_timestamp, last_timestamp)
        last_timestamp = current_timestamp
        current_rel_time = current_timestamp - start_time
        last_rel_time
        
        
        light_value = 0 # Initialize light_value
        global frequency 

        #print(current_rel_time%dur_ms ,"            ", last_rel_time%dur_ms)
        if current_rel_time%dur_ms <= last_rel_time%dur_ms:
            last_rel_time = current_rel_time
            frequency_refresh = 1
            light_00 = light_0
            light_0 = clamped_light

        if recording_active:
            # Read sensor and record
            light_value = photo_sensor_pin.read_u16()
            recorded_data.append((current_timestamp, light_value))
            # print(f"Recording: {current_timestamp}, {light_value}") # Uncomment for debugging

        elif replay_active:
            # Replay stored data
            if replay_index < len(recorded_data):
                replayed_timestamp, replayed_light_value = recorded_data[replay_index]

                # We'll use the current_timestamp here as a reference,
                # but for accurate replay, you might want to use the delta
                # between recorded timestamps to control sleep.
                # For simplicity, we'll just process the next value.
                light_value = replayed_light_value
                replay_index += 1
                # print(f"Replaying: {replayed_timestamp}, {light_value}") # Uncomment for debugging

                # To make replay duration match recording, calculate sleep based on next data point
                if replay_index < len(recorded_data):
                    next_timestamp = recorded_data[replay_index][0]
                    sleep_duration = time.ticks_diff(next_timestamp, replayed_timestamp)
                    if sleep_duration > 0:
                        await asyncio.sleep_ms(sleep_duration) # type: ignore[attr-defined]
            else:
                print("Replay finished.")
                stop_replay()
                stop_tone()
                await asyncio.sleep_ms(500) # Give it a moment before potentially looping or going idle
                continue # Skip processing audio if replay just finished

        else:
            # Default behavior: play sound based on live light
            light_value = photo_sensor_pin.read_u16()


        # Process the light_value (either live, recorded, or replayed)
        if not replay_active or (replay_active and light_value is not None):
            clamped_light = max(min_light, min(light_value, max_light))

            if clamped_light > min_light:
                if frequency_refresh == 1:
                    frequency = map_value(
                        clamped_light, min_light, max_light, min_freq, max_freq
                    )
                    frequency_refresh = 0
                print(frequency)
                Play_Chord(frequency, current_rel_time%dur_ms, light_00, light_0)
                #buzzer_pin.freq(frequency)
                #buzzer_pin.duty_u16(32768)  # 50% duty cycle
            else:
                stop_tone()  # If it's very dark, be quiet
        
        last_rel_time = current_rel_time
        
        
        # Only sleep if not actively in replay managing its own sleep
        if not replay_active or replay_index >= len(recorded_data):
            await asyncio.sleep_ms(50) # type: ignore[attr-defined]
            

##########################################################################################
# Run the main event loop
if __name__ == "__main__":
    print("Pico Light Orchestra Instrument Code")
    print("Available functions: start_recording(), stop_recording(), start_replay(), stop_replay(), save_recording(), load_recording()")
    print("To start, type 'start_recording()' in the REPL, then 'stop_recording()' to save.")
    print("Then 'start_replay()' to play it back.")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram stopped.")
        stop_recording() # Ensure recording is saved if stopped mid-recording
        stop_replay()
        stop_tone()
    finally:
        buzzer_pin.deinit() # Clean up PWM to stop any residual noise

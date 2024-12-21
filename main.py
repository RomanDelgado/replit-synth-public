
import asyncio
import numpy as np
import sounddevice as sd
from audio import Synth
from midi import MidiHandler

SAMPLE_RATE = 44100

async def audio_output_loop(synth):
    try:
        stream = sd.OutputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype=np.float32,
            callback=lambda outdata, frames, time, status: outdata.fill(0) if status else outdata[:] = synth.mix_notes().reshape(-1, 1)
        )
        
        print("Audio stream created successfully")
        with stream:
            print("Audio stream started")
            while True:
                await asyncio.sleep(0.1)
    except Exception as e:
        print(f"Audio error: {e}")

async def midi_listener(synth):
    midi_handler = MidiHandler()
    try:
        while True:
            midi_events = midi_handler.read_midi_events()
            for status, note, velocity in midi_events:
                if status == 144 and velocity > 0:  # Note On
                    frequency = 440 * (2 ** ((note - 69) / 12))
                    synth.add_note(note, frequency, 1.0, velocity)
                elif status == 128 or (status == 144 and velocity == 0):  # Note Off
                    synth.remove_note(note)
            await asyncio.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting MIDI listener.")
    finally:
        midi_handler.close()

def main():
    try:
        print("Creating Synth instance...")
        synth = Synth()
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        print("Starting audio and MIDI processing...")
        loop.run_until_complete(asyncio.gather(
            audio_output_loop(synth),
            midi_listener(synth)
        ))
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()

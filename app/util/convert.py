import os
import asyncio
import subprocess
from pydub import AudioSegment

def midi_to_mp3(midi_file, soundfont, mp3_file):
    # Convert MIDI to WAV using fluidsynth
    wav_file = mp3_file.replace('.mp3', '.wav')
    print(wav_file)

    subprocess.run(
        f'fluidsynth -ni {soundfont} {midi_file} -F - -r 44100 -o audio.file.type=au -q | ffmpeg -i - -b:a 192K {mp3_file}',
        shell=True,
        check=True,
    )

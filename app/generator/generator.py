from selectors import DefaultSelector
import pretty_midi
import numpy as np
import random
from typing import Union
from pychord import Chord
from .module.chord import *
from .module.melody import *
from .module.drum import *
from .util.music.util import *

class NoteWrapper:
    def __init__(
        self, 
        notes, 
        division, 
        is_drum = False
    ):
        self.notes = notes
        self.division = division
        self.is_drum = is_drum

    def __str__(self):
        return f'notes: {self.notes}\ndivision: {self.division}'


def apply_midi(
    instrument,
    start_base,
    duration,
    notes
):
    for (n, d) in notes:
        note = pretty_midi.Note(
            velocity=100, 
            pitch=n,
            start=start_base, 
            end=start_base + d*duration
        )
        instrument.notes.append(note)
        start_base += d*duration

    return start_base

def apply_drum(
    drum_instrument,
    start_base,
    duration,
    drum_notes,
):
    for n in drum_notes:
        for drum_each in n:
            note = pretty_midi.Note(
                velocity=100,
                pitch=drum_each,
                start=start_base,
                end=start_base + duration
            )
            drum_instrument.notes.append(note)
        start_base += duration

    return start_base

def create_part(
    scale: Scale,
    chord_pattern: ChordWithPattern,
    drum_pattern: DrumPattern,
    randomness: int,
    bar_part: int=8,
    measure=(4,4),
    fill_in_pattern: DrumPattern | None=None,   # 없으면 걍 empty 로
):  
    bar_per_cp = chord_pattern.cp.bar_length

    if (bar_part < bar_per_cp):
        raise Exception('Song length is smaller than chord length!')
   
    melody_primary = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division=16
    )
    melody_diff = melody_primary.get_differ_melody(melody_randomness=0.5)
    melody_b = Melody(
        scale=scale,
        randomness=randomness,
        chord_progression=chord_pattern.cp,
        measure=measure,
        division=16
    )

    # 기본적으로 AA'BA 형식을 따름
    if (bar_part == bar_per_cp):
        melodies = [melody_primary]
    elif (bar_part == 2 * bar_per_cp):
        melodies = [melody_primary, melody_diff]
    elif (bar_part == 4 * bar_per_cp):
        melodies = [melody_primary, melody_diff, melody_b, melody_primary]
    elif (bar_part == 8 * bar_per_cp):
        melodies = [melody_primary, melody_diff, melody_b, melody_primary] * 2
    else:
        raise Exception('Unsupported bar length.')

    melody_note_total = []
    for melody in melodies:
        if (melody.notes is None):
            raise Exception('Empty melody notes')

        melody_note_total.extend(melody.notes)
    melody_wrapper = NoteWrapper(melody_note_total, melody_primary.division)

    chords = [chord_pattern] * (bar_part // bar_per_cp)
    chord_note_total = []
    for chord in chords:
        chord_note_total.extend(chord.notes)
    chord_wrapper = NoteWrapper(chord_note_total, chord_pattern.division)

    if fill_in_pattern is not None:
        real_division = max(drum_pattern.division, fill_in_pattern.division)
        real_drum_pattern = multiplyDivision(drum_pattern, real_division / drum_pattern.division) if real_division > drum_pattern.division else drum_pattern
        real_fill_in_pattern = multiplyDivision(fill_in_pattern, real_division / fill_in_pattern.division) if real_division > fill_in_pattern.division else fill_in_pattern
    else:
        real_division = drum_pattern.division
        real_drum_pattern = drum_pattern

    drum_note_total = []
    for _ in range(bar_part // real_drum_pattern.bar_length):
        drum_note_total.extend(real_drum_pattern.pattern)
    
    if fill_in_pattern is not None:
        start_index = real_drum_pattern.division * fill_in_pattern.bar_length
        drum_note_total[-start_index:] = fill_in_pattern.pattern

    drum_wrapper = NoteWrapper(drum_note_total, real_drum_pattern.division, is_drum=True)

    return [melody_wrapper, chord_wrapper, drum_wrapper]

def merge_part(
    part_list: list[list[NoteWrapper]],
    instrument_list: list[pretty_midi.Instrument],
    bpm: int,
):
    start_base = 0

    for part in part_list:
        if len(part) != len(instrument_list):
            raise Exception(f'Must contain {len(instrument_list)} instruments.')

        start_base_each = 0
        for (note_wrapper, instrument) in zip(part, instrument_list):
            duration = (1/note_wrapper.division) * (240/bpm)
            if (note_wrapper.is_drum):
                start_base_each = apply_drum(instrument, start_base, duration, note_wrapper.notes)
            else:
                start_base_each = apply_midi(instrument, start_base, duration, note_wrapper.notes)
            start_base_each = np.round(start_base_each, decimals=4)

        start_base = start_base_each

def make_song(
    genre: str,
    mood: str,
    music_path: str,
    tempo: str,
    bpm: Union[int, None]=None,
    max_randomness: float=0.7,
):
    if genre not in ['newage', 'retro']:
        raise Exception('Unsupported genre.')

    if mood not in ['happy', 'sad', 'grand']:
        raise Exception('Unsupported mood.')

    if tempo not in ['slow', 'moderate', 'fast']:
        raise Exception('Unsupported tempo.')

    quant_size = 0.1
    limitations = {
        'newage': {
            'bpm': set(range(60, 120 + 1)),
            'randomness': set(np.arange(0.2, 0.6, quant_size)),
        },
        'retro': {
            'bpm': set(range(80, 160 + 1)),
            'randomness': set(np.arange(0.2, 0.9, quant_size)),
        },
        'happy': {
            'bpm': set(range(80, 160 + 1)),
            'randomness': set(np.arange(0.1, 0.9, quant_size)),
        },
        'sad': {
            'bpm': set(range(60, 100 + 1)),
            'randomness': set(np.arange(0.1, 0.8, quant_size)),
        },
        'grand': {
            'bpm': set(range(60, 90 + 1)),
            'randomness': set(np.arange(0.1, 0.8, quant_size)),
        },
    }

    if bpm is None:
        # 장르와 무드에 따라 bpm 설정
        bpm_list: list[int] = list(limitations[genre]['bpm'].intersection(limitations[mood]['bpm']))
        cropped_bpm_list: list[list[int]] = divide_chunk_into(bpm_list, 3)

        if (tempo == 'slow'):
            bpm = random.choice(cropped_bpm_list[0])
        elif (tempo == 'moderate'):
            bpm = random.choice(cropped_bpm_list[1])
        else:
            bpm = random.choice(cropped_bpm_list[2])

    randomness_list = list(limitations[genre]['randomness'].intersection(limitations[mood]['randomness']))

    rand_limit_high = min(max_randomness, randomness_list[-1])
    randomness_list = np.linspace(randomness_list[0], rand_limit_high, 50)

    randomness_selection = sorted([
        random.choice(randomness_list),
        random.choice(randomness_list),
        random.choice(randomness_list),
        random.choice(randomness_list),
    ])

    print(randomness_selection, bpm)

    instruments = {
        'piano_acoustic': pretty_midi.Instrument(program=0),
        'lead_square': pretty_midi.Instrument(program=80),
        'lead_sawtooth': pretty_midi.Instrument(program=81),
        'drum_acoustic': pretty_midi.Instrument(program=0, is_drum=True),
    }
    instruments_set = {
        'newage': [instruments['piano_acoustic'], instruments['piano_acoustic'], instruments['drum_acoustic']],
        'retro': [instruments['lead_square'], instruments['lead_sawtooth'], instruments['drum_acoustic']],
    }

    # song making start
    output_midi = pretty_midi.PrettyMIDI()
    [main_instrument, sub_instrument, drum_instrument] = instruments_set[genre]

    deviation = random.randint(0, 11)
    default_scale = MajorScale(get_transposed_root('C', deviation))

    chords_selection = []
    for _ in range(4):
        random_chords = random.choice(chord_progressions)
        cp = ChordProgression(list(random_chords))
        chords_selection.append(get_transposed_cp(cp, deviation))

    inoutro = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[0], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        drum_pattern=drum_patterns['newage']['intro'][0],
        randomness=randomness_selection[0],
        bar_part=4,
        measure=(4, 4),
    )
    verse = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[1], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        drum_pattern=drum_patterns['newage']['verse'][0],
        randomness=randomness_selection[1],
        bar_part=8,
        measure=(4, 4),
        fill_in_pattern=drum_patterns['newage']['fill_in'][0],
    )
    chorus = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[2], len(chords_selection[2]) // 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        drum_pattern=drum_patterns['newage']['verse'][1],
        randomness=randomness_selection[2],
        bar_part=8,
        measure=(4, 4),
    )
    bridge = create_part(
        scale=default_scale,
        chord_pattern=ChordWithPattern(
            cp=Chords(chords_selection[3], 2),
            pattern=ArpeggioPattern(pat_method='one-five', dur_method='stacato'),
            division=8,
        ),
        drum_pattern=drum_patterns['newage']['verse'][0],
        randomness=randomness_selection[3],
        bar_part=8,
        measure=(4, 4),
        fill_in_pattern=drum_patterns['newage']['fill_in'][0],
    )

    merge_part(
        part_list=[inoutro, verse, chorus, verse, chorus, bridge, chorus, inoutro],
        instrument_list=[main_instrument, sub_instrument, drum_instrument],
        bpm=bpm,
    )

    output_midi.instruments.append(main_instrument)
    output_midi.instruments.append(sub_instrument)
    output_midi.instruments.append(drum_instrument)
    output_midi.write(music_path)

if __name__ == '__main__':
    make_song(
        genre='retro',
        mood='happy',
        tempo='slow',
        music_path='./test/output.mid'
    )

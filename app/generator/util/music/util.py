from pychord import Chord, ChordProgression

def get_transposed_root(root: str, amount: int) -> str:
    __notes_with_sharp = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    __notes_with_flat = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

    idx = 0
    is_sharp = True
    if (root in __notes_with_sharp):
        idx = __notes_with_sharp.index(root)
        is_sharp = True
    else:
        idx = __notes_with_flat.index(root)
        is_sharp = False
    
    idx = idx + amount
    idx = idx % 12

    scale = __notes_with_sharp if is_sharp else __notes_with_flat
    return scale[idx]

def get_transposed_chord(chord: Chord, amount: int):
    c = Chord(chord.chord)
    c.transpose(amount)
    return c

def get_transposed_cp(cp: ChordProgression, amount: int):
    c = ChordProgression([*cp.chords]) # type: ignore
    c.transpose(amount)
    return c

def calc_scale_from_chord(original_scale, chord):
    pass

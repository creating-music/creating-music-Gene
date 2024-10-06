from typing import Union
from pychord import Chord
import pretty_midi
import numpy as np

class Scale:
    __notes_with_sharp = ['A', 'A#', 'B', 'C',
                          'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    __notes_with_flat = ['A', 'Bb', 'B', 'C',
                         'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
    OCTAVE = 12

    def __init__(
        self,
        root,
        scale,
        mode
    ):
        self.root = root                    # 근음. ex) 'C'
        self.default_scale = scale          # 스케일의 음 간격. ex) [0, 2, 4, 5, 7, 9, 11]
        self.scale: Union[set[int], None] = None                   # 실제 스케일의 음.
        self.mode = mode                    # 몇 번째 모드인지. 1 이면 원래 스케일과 동일.
        self.scale_name = None              # 스케일의 이름 (Major, Minor...)
        self.build_scale(scale)

    @staticmethod
    def estimate_scale(chord: Chord):
        quality_string = str(chord.quality)
        if (quality_string.isdigit()):
            return MajorScale(chord.root, 5)        # Dominant 7
        if ('m' in quality_string and 'b5' in quality_string):
            return MajorScale(chord.root, 7)        # Half-diminished
        if ('mM' in quality_string):
            return MelodicMinorScale(chord.root)
        if (quality_string == '' or 'M' in quality_string):
            return MajorScale(chord.root)
        if ('m' in quality_string):
            return MajorScale(chord.root, 6)        # Natural minor
        if ('dim' in quality_string):
            return DiminishedScale(chord.root)
        return AlteredScale(chord.root)

    def build_scale(self, scale):
        # A4 = 440Hz. 높은 음자리표에 맞춤.

        if (self.mode != 1):
            self.root = self.unmoded_root()

        root_as_number = pretty_midi.note_name_to_number(f'{self.root}4')
        weight = np.arange(-3, 5) * Scale.OCTAVE
        main_scale = np.array(scale)
        result_scale = []
        for w in weight:
            result_scale.extend(main_scale + root_as_number - w)
        self.scale = set(result_scale)

    def has_note(self, note_name):
        '''
        스케일에 해당 음이 있는지 확인.
        '''

        if (note_name in Scale.__notes_with_sharp):
            idx = Scale.__notes_with_sharp.index(note_name)
        else:
            idx = Scale.__notes_with_flat.index(note_name)

        if (self.root in Scale.__notes_with_sharp):
            root_idx = Scale.__notes_with_sharp.index(self.root)
        else:
            root_idx = Scale.__notes_with_flat.index(self.root)

        diff = idx - root_idx
        if (diff < 0):
            diff += Scale.OCTAVE

        return diff in self.default_scale

    def has_chord(self, chord: Chord):
        '''
        주어진 코드가 스케일 내에 있는지 확인.
        '''

        res = True
        for note in chord.components():
            res = res and self.has_note(note)

        return res

    def unmoded_root(self):
        '''
        모드에 의해 변경되기 전의 근음 반환.
        ex) Major scale에서 주어진 root가 A이고, mode가 6이면 C를 반환.
        '''

        if (self.root in Scale.__notes_with_sharp):
            idx = Scale.__notes_with_sharp.index(self.root)
            is_sharp = True
        else:
            idx = Scale.__notes_with_flat.index(self.root)
            is_sharp = False

        offset = self.default_scale[self.mode - 1]
        idx = (idx - offset) % Scale.OCTAVE

        notes = Scale.__notes_with_sharp if is_sharp else Scale.__notes_with_flat
        return notes[idx]

    def print_scale(self):
        print(f'{self.root} {self.scale_name}')

    def __str__(self):
        return f'{self.root} {self.scale_name}'


class MajorScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 5, 7, 9, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Major'

    @property
    def moded_scale_name(self):
        scale_name = ['Ionian', 'Dorian', 'Phrygian',
                      'Lydian', 'Mixolydian', 'Aeolian', 'Locrian']
        return scale_name[self.mode - 1]


class MelodicMinorScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 3, 5, 7, 9, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Melodic minor'


class PentatonicScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 7, 9]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Pentatonic'


class BluesScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 3, 5, 6, 7, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Blues'


class WholeToneScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 2, 4, 6, 8, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Whole tone'


class ChromaticScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Chromatic'


class DiminishedScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 3, 4, 6, 7, 9, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Diminished'


class AlteredScale(Scale):
    def __init__(
            self,
            root,
            mode=1
    ):
        default_scale = [0, 1, 3, 4, 6, 8, 10]
        super().__init__(root, default_scale, mode)
        self.scale_name = 'Altered'

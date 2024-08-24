import numpy as np
import copy
from typing import Sequence


class DrumPattern():
    KEYMAP = {
        'bass_drum': 36,
        'snare_rim': 37,
        'snare_drum': 38,
        'hihat_closed': 42,
        'hihat_opened': 46,
        'cymbals_crash': 49,
        'ride': 51,
    }
    def __init__(
        self, 
        name: str,
        input_patterns: dict[str, list[int]],
        toms_pattern: list[int],
        division: int = 8,
        bar_length: int = 1,
    ):        
        self.name = name

        # 각각 midi mapping
        drums = [
            np.array(part_pattern) * DrumPattern.KEYMAP[part_key] 
            for part_key, part_pattern 
            in input_patterns.items()
        ]
        if (toms_pattern_mapped):
            toms_pattern_mapped = np.array(toms_pattern)
            drums.append(toms_pattern_mapped)

        pattern_lengths = set(map(len, drums))

        # 모든 패턴들의 길이가 같아야 함.
        if len(pattern_lengths) != 1:
            raise Exception("Length of patterns don't match!")


        self.pattern = list(zip(*drums))
        self.division = division
        self.bar_length = bar_length

def multiplyDivision(drum_pattern: DrumPattern, ratio: float) -> DrumPattern:
    intRatio = int(ratio)

    new_pattern = copy.copy(drum_pattern)
    new_pattern.division *= intRatio
    
    temp_pattern = []
    for p in drum_pattern.pattern:
        for i in range(intRatio):
            if i == 0: 
                temp_pattern.append(p)
            else:
                temp_tuple = tuple(0 for x in p)
                temp_pattern.append(temp_tuple)
            
    new_pattern.pattern = temp_pattern
    return new_pattern


drum_patterns = {
    'common': {
        'empty': [
            DrumPattern(
                name = "newage_intro",
                input_pattern = {
                    'bass_drum': [0],
                },
                division=1,
                bar_length=1,
            ),
        ]
    },
    'newage': {
        'intro': [
            DrumPattern(
                name = "newage_intro",
                input_pattern = {
                    'bass_drum': [0],
                },
                division=1,
                bar_length=1,
            ),
        ],
        'fill_in': [
            DrumPattern(
                name = "newage_fill_in",
                input_pattern = {
                    'bass_drum': [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
                    'snare_drum': [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,],
                    'hihat_closed': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                    'hihat_open': [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,],
                    'cymbals_crash': [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
                },
                toms_pattern= [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 48, 47, 45,],
                division=16,
                bar_length=1,
            ),
        ],
        'verse': [
            DrumPattern(
                name = "8bit_default",
                input_pattern = {
                    'bass_drum'  : [1, 0, 0, 0, 0, 1, 0, 0] * 4,
                    'snare_drum' : [0, 0, 1, 0, 0, 0, 1, 0] * 4,
                    'hihat_closed' : [1, 1, 1, 1, 1, 1, 1, 1] * 4,
                    'cymbals_crash': [1, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] * 3,
                    'hihat_opened' : [0] * 8 * 4,
                },
                toms_pattern = [0] * 8 * 4,
                division=8,
                bar_length=4,
            ),
            DrumPattern(
                name = "16bit_slow",
                input_pattern = {
                    'bass_drum'  : [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,] * 4,
                    'snare_drum' : [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1,] * 4,
                    'hihat_closed' : [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,] * 4,
                    'cymbals_crash': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,] + [0] * 16 * 3,
                    'hihat_opened' : [0] * 16 * 4,
                },
                toms_pattern = [0] * 16 * 4,
                division=16,
                bar_length=4,
            ),
        ]
    },
    'jazz': {
        'intro': [
            DrumPattern(
                name= "bossanova",
                input_pattern = {
                    'bass_drum': [1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0,] * 2,
                    'snare_rim': [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,] * 2,
                    'ride':      [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0,] * 2,
                },
                division=8,
                bar_length=4,
            )
        ]
    }
}


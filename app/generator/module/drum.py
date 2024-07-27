import numpy as np
import copy

class DrumPattern():
    KEYMAP = {
        'base_drum': 36,
        'snare_drum': 38,
        'hihat_closed': 42,
        'hihat_opened': 46,
        'cymbals_crash': 49,
    }
    def __init__(
        self, 
        name: str,
        kick_pattern: list[int], 
        hihat_pattern: list[int], 
        ohihat_pattern: list[int],
        snare_pattern: list[int], 
        toms_pattern: list[int],
        cymbals_pattern: list[int],
        division: int = 8,
        bar_length: int = 1,
    ):        
        self.name = name

        # 각각 midi mapping
        kick_pattern_mapped = np.array(kick_pattern) * DrumPattern.KEYMAP['base_drum']
        snare_pattern_mapped = np.array(snare_pattern) * DrumPattern.KEYMAP['snare_drum']
        hihat_pattern_mapped = np.array(hihat_pattern) * DrumPattern.KEYMAP['hihat_closed']
        ohihat_pattern_mapped = np.array(ohihat_pattern) * DrumPattern.KEYMAP['hihat_opened']
        cymbals_pattern_mapped = np.array(cymbals_pattern) * DrumPattern.KEYMAP['cymbals_crash']
        toms_pattern_mapped = np.array(toms_pattern)

        drums = [
            kick_pattern_mapped, 
            snare_pattern_mapped, 
            hihat_pattern_mapped, 
            ohihat_pattern_mapped,
            toms_pattern_mapped,
            cymbals_pattern_mapped
        ]
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
                kick_pattern    = [0],
                snare_pattern   = [0],
                hihat_pattern   = [0],
                ohihat_pattern  = [0],
                cymbals_pattern = [0],
                toms_pattern    = [0],
                division=1,
                bar_length=1,
            ),
        ]
    },
    'newage': {
        'intro': [
            DrumPattern(
                name = "newage_intro",
                kick_pattern    = [0],
                snare_pattern   = [0],
                hihat_pattern   = [0],
                ohihat_pattern  = [0],
                cymbals_pattern = [0],
                toms_pattern    = [0],
                division=1,
                bar_length=1,
            ),
        ],
        'fill_in': [
            DrumPattern(
                name = "newage_fill_in",
                kick_pattern    = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0,],
                snare_pattern   = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0,],
                hihat_pattern   = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
                ohihat_pattern  = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,],
                cymbals_pattern = [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
                toms_pattern    = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 48, 47, 45,],
                division=16,
                bar_length=1,
            ),
        ],
        'verse': [
            DrumPattern(
                name = "8bit_default",
                kick_pattern  = [1, 0, 0, 0, 0, 1, 0, 0] * 4,
                snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0] * 4,
                hihat_pattern = [1, 1, 1, 1, 1, 1, 1, 1] * 4,
                cymbals_pattern=[1, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] * 3,
                ohihat_pattern = [0] * 8 * 4,
                toms_pattern = [0] * 8 * 4,
                division=8,
                bar_length=4,
            ),
            DrumPattern(
                name = "16bit_slow",
                kick_pattern  = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,] * 4,
                snare_pattern = [0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1,] * 4,
                hihat_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,] * 4,
                cymbals_pattern=[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,] 
                              + [0] * 16 * 3,
                ohihat_pattern = [0] * 16 * 4,
                toms_pattern = [0] * 16 * 4,
                division=16,
                bar_length=4,
            ),
        ]
    }
}


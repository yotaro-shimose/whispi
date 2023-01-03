from dataclasses import dataclass
from pathlib import Path

import numpy as np
from typing_extensions import Self
from whisper import load_audio


@dataclass
class WaveForm:
    """Numpy wrapper containing Waveform Audio File Format
    """

    wave: np.ndarray

    @classmethod
    def load_file(cls, path: Path) -> Self:
        return cls(load_audio(str(path)))

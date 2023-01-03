from typing import Optional

import torch
import whisper

from whispi.core.audio import WaveForm
from whispi.core.subtitle import Subtitle

SAMPLING_RATE = 16000


class WhisperExtractor:
    def __init__(self, device: Optional[torch.device] = None):
        if device is None:
            device = torch.device("cuda") if torch.cuda.is_available() else None
        self._model = whisper.load_model("large", device=device)

    def extract_subtitles(self, wave: WaveForm) -> list[Subtitle]:
        # audio: np.ndarray = whisper.load_audio(str(mp4_path), SAMPLING_RATE)
        length_sec = len(wave.wave) / SAMPLING_RATE
        result = self._model.transcribe(wave.wave)
        segments: dict = result["segments"]  # type: ignore
        return [
            Subtitle(segment["text"], segment["start"], min(segment["end"], length_sec))
            for segment in segments
        ]


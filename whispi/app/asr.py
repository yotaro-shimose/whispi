from whispi.core.audio import WaveForm
from whispi.core.extractor import WhisperExtractor
from whispi.core.subtitle import Subtitle


def recognize(extractor: WhisperExtractor, wave: WaveForm) -> list[Subtitle]:
    return extractor.extract_subtitles(wave)

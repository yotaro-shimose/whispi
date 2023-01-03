from whispi.app.asr import recognize
from whispi.constant import PROJECT_ROOT
from whispi.core.audio import WaveForm
from whispi.core.extractor import WhisperExtractor


def test_not_empty():
    # Init extractor
    extractor = WhisperExtractor()

    # Load sample wave
    sample_path = PROJECT_ROOT / "sample" / "sample.wav"
    wave = WaveForm.load_file(sample_path)

    subtitles = recognize(extractor, wave)
    assert len(subtitles) > 0

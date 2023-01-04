import os
import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile

from whispi.app.asr import recognize
from whispi.constant import PROJECT_ROOT
from whispi.core.audio import WaveForm
from whispi.core.extractor import WhisperExtractor
from whispi.core.subtitle import Subtitle

router = APIRouter()
extractor = WhisperExtractor()
SAMPLE_RATE = 16000


def sec2vtt_exp(time: float) -> str:
    hour = int(time // 3600)
    minute = int((time % 3600) // 60)
    sec = int((time) - (hour * 3600 + minute * 60))
    rem = str(time - sec)[2:5]
    return f"{hour:0>2}:{minute:0>2}:{sec:0>2}.{int(rem):0>3}"


def subtitle2vtt_item(subtitle: Subtitle) -> str:
    ARROW = "-->"
    time_str = (
        f"{sec2vtt_exp(subtitle.start_sec)} {ARROW} {sec2vtt_exp(subtitle.end_sec)}"
    )
    return f"{time_str}{os.linesep}{subtitle.text}{os.linesep}{os.linesep}"


def create_vtt_string(subtitles: list[Subtitle]) -> str:
    VTT_HEADER = f"WEBVTT{os.linesep}{os.linesep}"
    return VTT_HEADER + "".join([subtitle2vtt_item(subtitle) for subtitle in subtitles])


@router.post("/vtt")
async def auto_subtitle(video: UploadFile) -> dict:
    out_path = get_temporary_filepath()
    with out_path.open("wb") as out_io:
        out_io.write(video.file.read())
    wave = WaveForm.load_file(out_path)
    out_path.unlink()
    subtitles = recognize(extractor, wave)
    return {"vtt": create_vtt_string(subtitles)}


def get_temporary_filepath() -> Path:
    connection_idx = str(uuid.uuid4())
    out_path = PROJECT_ROOT / f"{connection_idx}.mp4"
    return out_path
